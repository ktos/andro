#!/usr/bin/env python
# coding: utf-8

import pyandro.dictionary as dictionary
import pyandro.phonemizer as phonemizer
import sys

# all syllabes
alls = [line.rstrip() for line in open('./syllabes.txt', encoding='utf-8')]

p = phonemizer.AndroPhonemizer()


def check_syllabes(speech, org, strict=False):
    if speech == "FEM":
        return  # ignore "FEM" syllabes, as it is only placeholder

    global p
    h = p.romanization(org, remove_accents=True).replace(
        '.', '').replace("ˈ", "").strip()
    s = speech.replace('.', '').replace("ˈ", "").strip()

    # romanization does not play nicely with ŋ, so let's workaround this
    s = s.replace('ŋ', 'n')

    lprefix = "FAIL" if strict else "WARN"

    if h != s:
        print(
            f"{lprefix}: speech {s} does not match romanization IPA {h} for {org}")
        if strict:
            exit(1)

    l = speech.strip().replace("ˈ", "")
    for i in l.split('.'):
        if i not in alls:
            print(f"{lprefix}: syllable {l} (because of {i}); word: {org}")
            if strict:
                exit(1)


def check_dictionary(strict=False):
    # read and parse dictionary file
    words = dictionary.read_dictionary('./dictionary.csv')

    words = list(filter(lambda x: not x['ignore_err'], words))

    # check all words except empty speech and names for proper syllabes
    for i in filter(lambda x: x['speech'] != '' and x['type'] != 'name', words):
        check_syllabes(i['speech'], i['word'], strict)

    for i in filter(lambda x: 'pst_speech' in x, words):
        check_syllabes(i['pst_speech'], i['pst'], strict)

    for i in filter(lambda x: 'pl_speech' in x, words):
        check_syllabes(i['pl_speech'], i['pl'], strict)

    for i in filter(lambda x: 'fem_speech' in x, words):
        check_syllabes(i['fem_speech'], i['fem'], strict)

    for i in filter(lambda x: 'comp_speech' in x, words):
        check_syllabes(i['comp_speech'], i['comp'], strict)

    for i in filter(lambda x: 'supl_speech' in x, words):
        check_syllabes(i['supl_speech'], i['supl'], strict)

    lprefix = "FAIL" if strict else "WARN"

    # check for empty descriptions
    for x in words:
        if x['ignore_err']:
            continue

        if len(x['description']) == 0 and 'redirect' not in x and x['type'] != 'name':
            print("{lprefix}: EMPTY DESCRIPTION in " + x['word'])
            if strict:
                exit(1)

        if len(x['english_description']) == 0 and 'redirect' not in x and x['type'] != 'name':
            print("{lprefix}: EMPTY ENGLISH DESCRIPTION in " + x['word'])
            if strict:
                exit(1)

        # check for two-way derivational morphology
        if 'morph' in x:
            if len(x['morph'].split(' ')) != 2:
                print(
                    f"{lprefix}: derivational morphology not written correctly in {x['word']}")
                if strict:
                    exit(1)

    # check if last line is empty
    with open("./dictionary.csv", 'r', encoding='utf-8') as f:
        data = f.read()
        if data[-1] != "\n":
            print("{lprefix}: Last character is not a newline, sorting will fail!")
            if strict:
                exit(1)


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
