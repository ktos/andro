#!/usr/bin/env python
# coding: utf-8

import unidecode

# reads dictionary descfile
with open('../dictionary.csv', 'r', encoding='utf-8') as f:
    data = f.readlines()

sorted_lines = sorted(data, key=lambda x: unidecode.unidecode(x))

with open('../dictionary.csv', 'w', encoding='utf-8') as f:
    f.writelines(sorted_lines)