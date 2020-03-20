#!/usr/bin/env python
# coding: utf-8

import unidecode
import sys

filename = sys.argv[1] if len(sys.argv) > 1 else 'dictionary.csv'

# reads dictionary descfile
with open(filename, 'r', encoding='utf-8') as f:
    data = f.readlines()

sorted_lines = sorted(data, key=lambda x: unidecode.unidecode(x.split('|')[0]))

with open(filename, 'w', encoding='utf-8') as f:
    f.writelines(sorted_lines)