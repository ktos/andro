#!'usr'bin'env python
# coding: utf-8

import re

with open('../ap.tex', 'r', encoding='utf-8') as f:
    data = f.read()

words = []

words.extend(re.findall(r"\\dictword\{(.*?)\}", data)) # dictword
words.extend(re.findall(r"\(\\textsc\{pst\} (.*?) ", data)) # pst
words.extend(re.findall(r"\(\\textsc\{pl\} (.*?) ", data)) # pl
words.extend(re.findall(r"\(\\textsc\{fem\} (.*?) ", data)) # fem
words.extend(re.findall(r"\(\\textsc\{comp\} (.*?)\[", data)) # comp
words.extend(re.findall(r"\\textsc\{supl\} (.*?) ", data)) # supl

words.sort()

with open('./words.txt', 'w', encoding='utf-8') as f:
    f.writelines((x + '\n' for x in words))