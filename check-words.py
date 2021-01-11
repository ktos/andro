#!/usr/bin/env python
# coding: utf-8

import dictionaryparser
import sys

# read and parse dictionary file
words = dictionaryparser.read_dictionary('./dictionary.csv')

# all syllabes
alls = [line.rstrip() for line in open('./syllabes.txt', encoding='utf-8')]

# strict mode: fail on first problem and return exitcode 1 so CI will know
# about it
strict = True if len(sys.argv) > 1 and sys.argv[1] == "strict" else False

def check_syllabes(speech, org):
    if speech == "FEM": return # ignore "FEM" syllabes, as it is only placeholder
    l = speech.strip().replace("ˈ", "")
    for i in l.split('.'):
        if i not in alls:
            print(f"SYLLABLE WARN: {l} (because of {i}); WORD: {org}")
            if strict: exit(1)

# check all words except empty speech and names for proper syllabes
for i in filter(lambda x: x['speech'] != '' and x['type'] != 'name', words):
    check_syllabes(i['speech'], i['word'])

for i in filter(lambda x: 'pst_speech' in x, words):
    check_syllabes(i['pst_speech'], i['word'])

for i in filter(lambda x: 'pl_speech' in x, words):
    check_syllabes(i['pl_speech'], i['word'])

for i in filter(lambda x: 'fem_speech' in x, words):
    check_syllabes(i['fem_speech'], i['word'])

for i in filter(lambda x: 'comp_speech' in x, words):
    check_syllabes(i['comp_speech'], i['word'])

for i in filter(lambda x: 'supl_speech' in x, words):
    check_syllabes(i['supl_speech'], i['word'])