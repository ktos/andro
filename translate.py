#!/usr/bin/env python
# coding: utf-8

import argparse
import re
import sys

import pyandro.dictionary

LEADING_WORDS = {'the', 'a', 'an', 'to'}


def normalize(text):
    """Normalizes an English description part for matching."""
    text = text.lower()
    for tag in ('<sc>', '</sc>', '<phrase>', '</phrase>', '<see>', '</see>'):
        text = text.replace(tag, '')
    text = re.sub(r'\([^)]*\)', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = text.strip('.,;:!?')

    words = text.split(' ')
    if len(words) > 1 and words[0] in LEADING_WORDS:
        text = ' '.join(words[1:])

    return text


def build_index(entries):
    """Builds a map from normalized English description parts to Andro words."""
    index = {}

    for x in entries:
        en = x.get('english_description', '')
        if not en:
            continue

        for part in en.split(','):
            key = normalize(part)
            if not key:
                continue
            index.setdefault(key, []).append(x['word'])

    return index


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(
        description='Translate a single English word to Andro '
                    'using the dictionary data.')
    parser.add_argument('word', nargs='?', default=None,
                        help='English word to translate (reads stdin if omitted)')
    args = parser.parse_args()

    word = args.word
    if word is None:
        line = sys.stdin.readline()
        if not line.strip():
            parser.error('no input provided (pass a word or pipe it via stdin)')
        word = line.strip()

    entries = pyandro.dictionary.read_dictionary('dictionary.csv')
    entries += pyandro.dictionary.read_dictionary('names.csv', type='names')
    index = build_index(entries)

    results = index.get(normalize(word), [])

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
