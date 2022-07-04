#!/usr/bin/env python
# coding: utf-8

import pyandro.dictionary
import pyandro.glosser
import sys

if __name__ == "__main__":
    p = pyandro.glosser.AndroGlosser()
    text = ""

    if len(sys.argv) == 1:
        text = sys.stdin.readline()
    elif len(sys.argv) == 2:
        text = sys.argv[1]
    else:
        print(f"Usage: {sys.argv[0]} [sentence]")
        sys.exit(1)

    print(p.sentence(text))
