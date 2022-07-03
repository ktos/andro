#!/usr/bin/env python
# coding: utf-8

import andro.dictionary
import andro.phonemizer
import andro.glosser
import sys

if __name__ == "__main__":
    p = andro.phonemizer.AndroPhonemizer()
    g = andro.glosser.AndroGlosser()
    text = ""

    if len(sys.argv) == 1:
        text = sys.stdin.readline().strip()
    elif len(sys.argv) == 2:
        text = sys.argv[1]
    else:
        print(f"Usage: {sys.argv[0]} [sentence]")
        sys.exit(1)

    print(f"**{text}**")
    print()
    print(p.sentence(text))
    print()

    print("    " + text.lower())
    print("    " + g.sentence(text))
    print()
    print(f"*TRANSLATION HERE*\n")
