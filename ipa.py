#!/usr/bin/env python
# coding: utf-8

import argparse
import sys

import pyandro.phonemizer


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(
        description='Phonemize a word or sentence to IPA.')
    parser.add_argument('word', nargs='?', default=None,
                        help='word or sentence to phonemize (reads stdin if omitted)')
    args = parser.parse_args()

    text = args.word
    if text is None or text.strip() == '-':
        line = sys.stdin.readline()
        if not line.strip():
            parser.error(
                'no input provided (pass a word or pipe it via stdin)')
        text = line.strip()

    p = pyandro.phonemizer.AndroPhonemizer()
    is_single_word = ' ' not in text
    print(p.sentence(text, include_front_accent=is_single_word))


if __name__ == "__main__":
    main()
