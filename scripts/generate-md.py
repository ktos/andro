#!/usr/bin/env python
# coding: utf-8

import sys
import dictionaryparser

# output
output = []


def print_output(str=""):
    """Prints to output"""
    output.append(str)


def generate_md_dictionary_entry(w, lang='pl'):
    """Generates Markdown dictionary entry based on an parsed descfile object"""
    output = []

    desckey = 'description' if lang == 'pl' else 'english_description'    

    if 'redirect' in w:
        return

    if not desckey in w:
        print("ERROR, NO DESCRIPTION FOR " + w['word'])
        return

    if w['type'] == 'n':
        pl = w['pl'] if 'pl' in w else '-'
        fem = w['fem'] if 'fem' in w else '-'
        if fem == "FEM":
            fem = '!!'

        s = f"{w['word']}|{pl}|{fem}|{w[desckey]}"    

    elif w['type'] == 'v':
        pst = w['pst'] if 'pst' in w else ''
        s = f"{i['word']}|{pst}|{i[desckey]}"

    elif w['type'] == 'adj':
        comp = w['comp'] if 'comp' in w else '-'
        supl = w['supl'] if 'supl' in w else '-'

        s = f"{i['word']}|{comp}|{supl}|{i[desckey]}"

    elif w['type'] == 'name':
        s = f"{i['word']}|{i['speech']}|{i[desckey]}"

    else:
        s = f"{i['word']}|{i[desckey]}"

    print_output(s)

# read and parse dictionary file
words = dictionaryparser.read_dictionary('../dictionary.csv')

lang = 'en' if len(sys.argv) > 1 and sys.argv[1] == 'en' else 'pl'

if lang == 'en':
    print_output("# Pronouns")
    print_output("Pronoun|Translation")
elif lang == 'pl':
    print_output("# Zaimki")
    print_output("Zaimek|Tłum")

print_output("--- | ---")

for i in filter(lambda x: x['type'] == 'pro', words):
    generate_md_dictionary_entry(i, lang)

if lang == 'en':
    print_output("# Nouns")
    print_output("Singular|Plural|Female|Translation")
elif lang == 'pl':
    print_output("# Rzeczowniki")
    print_output("Lp|Lm|Rodzaj żeński|Tłum")

print_output("--- | --- | --- | --- ")

for i in filter(lambda x: x['type'] == 'n', words):
    generate_md_dictionary_entry(i, lang)

if lang == 'en':
    print_output("# Verbs")
    print_output("Present|Past|Translation")
elif lang == 'pl':
    print_output("# Czasowniki")
    print_output("Teraźniejszy|Przeszły|Tłum")

print_output("--- | --- | ---")

for i in filter(lambda x: x['type'] == 'v', words):
    generate_md_dictionary_entry(i, lang)

if lang == 'en':
    print_output("# Adjectives")
    print_output("Base form|Comparative|Superlative|Translation")
elif lang == 'pl':
    print_output("# Przymiotniki")
    print_output("I stopień|II stopień|III stopień|Tłum")


print_output("--- | --- | --- | ---")

for i in filter(lambda x: x['type'] == 'adj', words):
    generate_md_dictionary_entry(i, lang)

if lang == 'en':
    print_output("# Particles")
    print_output("Particle|Translation")
elif lang == 'pl':
    print_output("# Partykuły")
    print_output("Partykuła|Tłum")
print_output("--- | ---")

for i in filter(lambda x: x['type'] == 'part', words):
    generate_md_dictionary_entry(i, lang)

if lang == 'en':
    print_output("# Idioms")
    print_output("Idiom|Translation")
elif lang == 'pl':
    print_output("# Idiomy i związki frazeologiczne")
    print_output("Idiom|Tłum")
print_output("--- | ---")

words = dictionaryparser.read_dictionary('../phraseology.csv', type='phraseology')
for i in filter(lambda x: x['type'] == 'phraseology', words):
    generate_md_dictionary_entry(i, lang)

if lang == 'en':
    print_output("# Names")
    print_output("Name|IPA|Meaning, notes")
elif lang == 'pl':
    print_output("# Imiona")
    print_output("Imię|Wymowa|Znaczenie, uwagi")

print_output("--- | --- | ---")

words = dictionaryparser.read_dictionary('../names.csv', type='names')
for i in filter(lambda x: x['type'] == 'name', words):
    generate_md_dictionary_entry(i, lang)

# save all tables to Markdown file
with open('./tables.md', 'w', encoding='utf-8') as f:
    f.writelines((x + '\n' for x in output))
