#!/usr/bin/env python
# coding: utf-8

import andro.dictionary
import andro.phonemizer
import sys

if __name__ == "__main__":
    p = andro.phonemizer.AndroPhonemizer()
    text = ""

    if len(sys.argv) == 1:
        text = sys.stdin.readline()
    elif len(sys.argv) == 2:
        text = sys.argv[1]
    else:
        print(f"Usage: {sys.argv[0]} [word]")
        sys.exit(1)

    is_single_word = text.find(' ') == -1
    print(p.sentence(text, include_front_accent=is_single_word))
