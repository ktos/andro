#!/usr/bin/env python
# coding: utf-8

import dictionaryparser

# read and parse dictionary file
words = dictionaryparser.read_dictionary('../dictionary.csv')

# all syllabes
alls = [line.rstrip() for line in open('./syllabes.txt', encoding='utf-8')]

def check_syllabes(speech):
    l = speech.strip().replace("ˈ", "")
    for i in l.split('.'):
        if i not in alls:
            print(f"SYLLABLE WARN: {l} (because of {i})")

# check all words except empty speech and names for proper syllabes
for i in filter(lambda x: x['speech'] != '' and x['type'] != 'name', words):
    check_syllabes(i['speech'])
