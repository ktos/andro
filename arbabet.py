#!/usr/bin/env python
# coding: utf-8

import pyandro.dictionary
import pyandro.phonemizer
import sys

if __name__ == "__main__":
    p = pyandro.phonemizer.AndroPhonemizer()

    if len(sys.argv) == 1:
        text = sys.stdin.readline()
        print(p.sentence_arpabet(text))
    elif len(sys.argv) == 2:
        text = sys.argv[1]
        print(p.sentence_arpabet(text))
    else:
        print(f"Usage: {sys.argv[0]} [word]")
