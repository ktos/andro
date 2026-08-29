#!/usr/bin/env python
# coding: utf-8

import argparse
import re
import sys

import unidecode

import pyandro.dictionary

TAG_RE = re.compile(r'</?(?:see|phrase|em|alt|sc)>')

FORMS = [
    ('pl', 'pl'),
    ('fem', 'fem'),
    ('pst', 'pst'),
    ('comp', 'comp'),
    ('supl', 'supl'),
]


def strip_tags(text):
    """Removes pseudo-HTML markup tags, keeping their content."""
    return TAG_RE.sub('', text)


def normalize_word(text):
    """Normalizes a word for matching: unidecode, drop [?], lowercase."""
    return unidecode.unidecode(text).replace('[?]', '').lower()


def entry_forms(x):
    """Returns the word and all its inflected forms (excluding FEM placeholder)."""
    forms = [x['word']]
    for key, _label in FORMS:
        value = x.get(key)
        if value is not None and value != 'FEM':
            forms.append(value)
    return forms


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(
        description='Search for a phrase in words (and their inflected '
                    'forms) or in English or Polish descriptions and print '
                    'all matching dictionary entries.')
    parser.add_argument('phrase', nargs='?', default=None,
                        help='phrase to search for (reads stdin if omitted)')
    parser.add_argument('-l', '--lang', choices=['en', 'pl'], default='en',
                        help='language of the descriptions to search (default: en)')
    args = parser.parse_args()

    phrase = args.phrase
    if phrase is None:
        line = sys.stdin.readline()
        if not line.strip():
            parser.error('no input provided (pass a phrase or pipe it via stdin)')
        phrase = line.strip()

    entries = pyandro.dictionary.read_dictionary('dictionary.csv')
    entries += pyandro.dictionary.read_dictionary('names.csv', type='names')

    field = 'english_description' if args.lang == 'en' else 'description'
    notes_field = 'english_notes' if args.lang == 'en' else 'notes'
    needle = phrase.lower()
    word_needle = normalize_word(phrase)

    found = 0
    for x in entries:
        desc = x.get(field, '')
        matched_desc = bool(desc) and needle in desc.lower()
        if not matched_desc and not any(
                word_needle in normalize_word(form)
                for form in entry_forms(x)):
            continue
        found += 1

        line = f"{x['word']} ({x['type']})"
        for key, label in FORMS:
            value = x.get(key)
            if value is None:
                continue
            if value == 'FEM':
                line += f" ({label})"
            else:
                line += f" ({label}:{value})"
        line += f": {strip_tags(desc)}"
        for note in x.get(notes_field, []):
            line += f": Note: {strip_tags(note)}"
        print(line)

    if not found:
        print(f"no entries found for '{phrase}'", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
