#!/usr/bin/env python
# coding: utf-8

import argparse
import sys


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(
        description="Check whether words exist in final/words-all.txt and "
                    "print those that do not.")
    parser.add_argument('source', nargs='?', default=None,
                        help="file to check, or '-' for stdin")
    parser.add_argument('word', nargs='?', default=None,
                        help="single word to check (only with source 'p')")
    args = parser.parse_args()

    if args.source is None:
        parser.error(
            "no input provided (pass a filename, '-', or 'p <word>')")
    if args.source == 'p' and args.word is None:
        parser.error("source 'p' requires a word")
    if args.word is not None and args.source != 'p':
        parser.error("'word' can only be used with source 'p'")

    with open('./final/words-all.txt', encoding='utf-8') as f:
        alls = [line.rstrip() for line in f]

    if args.source == '-':
        content = sys.stdin.readlines()
    elif args.source == 'p':
        content = [args.word]
    else:
        with open(args.source, encoding='utf-8') as f:
            content = f.readlines()

    for line in content:
        l = line.lower().split(' ')
        for i in l:
            x = i.strip(',. :\n\r!?')

            if x not in alls:
                print(f"BAD: {x}")


if __name__ == "__main__":
    main()
