#!/usr/bin/env python
# coding: utf-8

import argparse
import re
import sys

import pyandro.dictionary

LEADING_WORDS = {'the', 'a', 'an', 'to'}


def normalize(text, lang):
    """Normalizes a description part for matching."""
    text = text.lower()
    for tag in ('<sc>', '</sc>', '<phrase>', '</phrase>', '<see>', '</see>'):
        text = text.replace(tag, '')
    text = re.sub(r'\([^)]*\)', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = text.strip('.,;:!?')

    if lang == 'en':
        words = text.split(' ')
        if len(words) > 1 and words[0] in LEADING_WORDS:
            text = ' '.join(words[1:])

    return text


def build_index(entries, lang):
    """Builds a map from normalized description parts to Andro words."""
    field = 'english_description' if lang == 'en' else 'description'
    index = {}

    for x in entries:
        desc = x.get(field, '')
        if not desc:
            continue

        for part in re.split(r'[,;]', desc):
            key = normalize(part, lang)
            if not key:
                continue
            index.setdefault(key, []).append(x['word'])

    return index


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(
        description='Translate a single word from English or Polish to Andro '
                    'using the dictionary data.')
    parser.add_argument('word', nargs='?', default=None,
                        help='word to translate (reads stdin if omitted)')
    parser.add_argument('-l', '--lang', choices=['en', 'pl'], default='en',
                        help='source language of the word (default: en)')
    args = parser.parse_args()

    word = args.word
    if word is None:
        line = sys.stdin.readline()
        if not line.strip():
            parser.error('no input provided (pass a word or pipe it via stdin)')
        word = line.strip()

    entries = pyandro.dictionary.read_dictionary('dictionary.csv')
    entries += pyandro.dictionary.read_dictionary('names.csv', type='names')
    index = build_index(entries, args.lang)

    results = index.get(normalize(word, args.lang), [])

    seen = set()
    for r in results:
        if r not in seen:
            seen.add(r)
            print(r)

    if not results:
        print(f"no Andro translation found for '{word}'", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
