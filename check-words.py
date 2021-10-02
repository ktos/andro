#!/usr/bin/env python
# coding: utf-8

import dictionaryparser
import sys

# all syllabes
alls = [line.rstrip() for line in open('./syllabes.txt', encoding='utf-8')]

def check_syllabes(speech, org, strict=False):
    if speech == "FEM": return # ignore "FEM" syllabes, as it is only placeholder
    l = speech.strip().replace("ˈ", "")
    for i in l.split('.'):
        if i not in alls:
            print(f"SYLLABLE WARN: {l} (because of {i}); WORD: {org}")
            if strict: exit(1)

def check_dictionary(strict=False):
    # read and parse dictionary file
    words = dictionaryparser.read_dictionary('./dictionary.csv')

    # check all words except empty speech and names for proper syllabes
    for i in filter(lambda x: x['speech'] != '' and x['type'] != 'name', words):
        check_syllabes(i['speech'], i['word'], strict)

    for i in filter(lambda x: 'pst_speech' in x, words):
        check_syllabes(i['pst_speech'], i['word'], strict)

    for i in filter(lambda x: 'pl_speech' in x, words):
        check_syllabes(i['pl_speech'], i['word'], strict)

    for i in filter(lambda x: 'fem_speech' in x, words):
        check_syllabes(i['fem_speech'], i['word'], strict)

    for i in filter(lambda x: 'comp_speech' in x, words):
        check_syllabes(i['comp_speech'], i['word'], strict)

    for i in filter(lambda x: 'supl_speech' in x, words):
        check_syllabes(i['supl_speech'], i['word'], strict)


if __name__ == "__main__":
    # strict mode: fail on first problem and return exitcode 1 so CI will know
    # about it
    strict = True if len(sys.argv) == 2 and sys.argv[1] == "strict" else False
    
    # single mode: check the syllabes given as the second argument
    single = True if len(sys.argv) == 3 and sys.argv[1] == "single" else False    

    if not single:
        check_dictionary(strict)
    else:
        check_syllabes(sys.argv[2], "stdin")