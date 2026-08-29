#!/usr/bin/env python
# coding: utf-8

import argparse
import sys

import pyandro.glosser


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')  # type: ignore

    parser = argparse.ArgumentParser(
        description='Gloss a word or sentence.')
    parser.add_argument('sentence', nargs='?', default=None,
                        help='word or sentence to gloss (reads stdin if omitted)')
    args = parser.parse_args()

    text = args.sentence
    if text is None or text.strip() == '-':
        line = sys.stdin.readline()
        if not line.strip():
            parser.error(
                'no input provided (pass a sentence or pipe it via stdin)')
        text = line.strip()

    p = pyandro.glosser.AndroGlosser()
    print(p.sentence(text))


if __name__ == "__main__":
    main()
