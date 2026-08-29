#!/usr/bin/env python
# coding: utf-8

import argparse
import re
import sys

import pyandro.dictionary

TAG_RE = re.compile(r'</?(?:see|phrase|em|alt|sc)>')


def strip_tags(text):
    """Removes pseudo-HTML markup tags, keeping their content."""
    return TAG_RE.sub('', text)


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(
        description='Search for a phrase in English or Polish descriptions '
                    'and print all matching dictionary entries.')
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

    found = 0
    for x in entries:
        desc = x.get(field, '')
        if not desc or needle not in desc.lower():
            continue
        found += 1

        line = f"{x['word']}: {strip_tags(desc)}"
        for note in x.get(notes_field, []):
            line += f": Note: {strip_tags(note)}"
        print(line)

    if not found:
        print(f"no entries found for '{phrase}'", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
