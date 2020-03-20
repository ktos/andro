#!/usr/bin/env python
# coding: utf-8

import unidecode
import dictionaryparser
import sys

# output
output = []

def format_description(desc):
    desc = desc.replace("<see>", "\\emph{")
    desc = desc.replace("</see>", "}")

    desc = desc.replace("<phrase>", "\\emph{")
    desc = desc.replace("</phrase>", "}")

    desc = desc.replace("<em>", "\\emph{")
    desc = desc.replace("</em>", "}")

    desc = desc.replace("<alt>", "\\emph{")
    desc = desc.replace("</alt>", "}")

    desc = desc.replace("<sc>", "\\textsc{")
    desc = desc.replace("</sc>", "}")

    return desc

def print_output(str=""):
    """Prints to output"""
    output.append(str)

def generate_tex_dictionary_entry(w):
    """Generates TeX dictionary entry based on an parsed descfile object"""
    output = []

    # ignore names and phraseology
    if w['type'] in ['name', 'phraseology']:
        return

    if not 'redirect' in w:
        description = format_description(w['description'])

    if w['type'] == 'n':
        if 'fem' in w:
            if w['fem'] == "FEM":
                description = f"(\\textsc{{fem}}) " + description
            else:
                description = f"(\\textsc{{fem}} {w['fem']} [{w['fem_speech']}]) " + description

        if 'pl' in w:
            description = f"(\\textsc{{pl}} {w['pl']} [{w['pl_speech']}]) " + description

    if w['type'] == 'adj':
        if 'supl' in w and 'comp' in w:
            description = f"(\\textsc{{comp}} {w['comp']} [{w['comp_speech']}], \\textsc{{supl}} {w['supl']} [{w['supl_speech']}]) " + description
        
        elif 'supl' in w:
            description = f"(\\textsc{{supl}} {w['supl']} [{w['supl_speech']}]) " + description

        elif 'comp' in w:
            description = f"(\\textsc{{comp}} {w['comp']} [{w['comp_speech']}]) " + description

    if w['type'] == 'v':
        if 'pst' in w:
            description = f"(\\textsc{{pst}} {w['pst']} [{w['pst_speech']}]) " + description

    if 'redirect' in w:
        print_output(
            f"\\dictword{{{w['word']}}}[{w['speech']}]\n\\dictred{{{w['redirect']}}}")
    else:
        print_output(
            f"\\dictword{{{w['word']}}}[{w['speech']}]\n\\dictterm{{{w['type']}}}{{{description.strip()}}}")

    for i in w['notes']:
        note = i
        note = format_description(note)

        print_output(f"\\note{{{note}}}")

    print_output()


def generate_tex_reversedictionary_entry(w):
    """Generates TeX reversed dictionary (pl-and) entry for a parsed descfile object"""
    print_output(f"\\dictwordd{{{w['rev']}}}\\dicttermd{{{w['and']}}}")
    print_output()


def generate_reverse_items(words):
    """Generate all possible items which will go into reversed dictionary"""
    reverse_words = []

    for i in words:
        if 'description' in i and 'redirect' not in i:
            for j in i['description'].split(','):
                if not '"' in j and not ',,' in j and not "''" in j and not '(' in j and not ')' in j and len(j.strip().split(' ')) < 3:
                    rev = j.strip().replace("\\-", "").replace("~", " ")
                    if rev != '':

                    # longer than 3 words and containing " or ,, are not real terms
                        reverse_words.append({'rev': rev, 'and': i['word']})

    return reverse_words


def generate_tex_dictionary_section_start(section):
    """Generates TeX dictionary section start markings"""
    print_output("\\newpage")
    print_output(f"\\section{{{section}}}")
    print_output("\\begin{multicols}{2}")
    print_output()


def generate_tex_dictionary_section_end(section):
    """Generates TeX dictionary section ending markings"""
    print_output("\\end{multicols}")

# read and parse dictionary file
words = dictionaryparser.read_dictionary('../dictionary.csv')

# sort words without accents
sorted_words = sorted(words, key=lambda x: x['noaccent_word'].lower())

# sections for forward dictionary
sections = ['A', 'B', 'CH', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
            'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'Y', 'Z']

# generate all sections and all definitions for dictionary
for i in sections:
    thissection = list(filter(lambda x: x['word'].lower().startswith(i.lower()), sorted_words))

    if len(thissection) > 0:
        generate_tex_dictionary_section_start(i)

        for j in thissection:
            generate_tex_dictionary_entry(j)
        generate_tex_dictionary_section_end(i)

# save forward dictionary to file
with open('../ap.tex', 'w', encoding='utf-8') as f:
    f.writelines((x + '\n' for x in output))

# clear output
output = []

reverse_words = generate_reverse_items(words)
reverse_words_sorted = sorted(
    reverse_words, key=lambda x: unidecode.unidecode(x['rev']).lower())

sections = ['A', 'B', 'C', 'Ć', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
            'Ł', 'M', 'N', 'O', 'Ó', 'P', 'R', 'S', 'Ś', 'T', 'U', 'W', 'Y', 'Z', 'Ż', 'Ź']

for i in sections:
    thissection = list(filter(lambda x: i.lower() == x['rev'][0], reverse_words_sorted))

    if len(thissection) > 0:
        generate_tex_dictionary_section_start(i)

        for j in thissection:
            generate_tex_reversedictionary_entry(j)
        generate_tex_dictionary_section_end(i)

# save reverse dictionary to file
with open('../pa.tex', 'w', encoding='utf-8') as f:
    f.writelines((x + '\n' for x in output))

# save list of all basic forms of words to file
with open('./words-basic.txt', 'w', encoding='utf-8') as f:
    f.writelines(y['word'] + '\n' for y in filter(lambda x: x['type'] not in ['name', 'phraseology', 'proper'], sorted_words))

# save list of all words forms to file
with open('./words-all.txt', 'w', encoding='utf-8') as f:

    basic = (x['word'] for x in filter(lambda x: x['type'] not in ['name', 'phraseology', 'proper'], words))
    pl = (x['pl'] for x in filter(lambda x: 'pl' in x, words))
    pst = (x['pst'] for x in filter(lambda x: 'pst' in x, words))
    fem = (x['fem'] for x in filter(lambda x: 'fem' in x and x['fem'] != 'FEM', words))
    supl = (x['supl'] for x in filter(lambda x: 'supl' in x, words))
    comp = (x['comp'] for x in filter(lambda x: 'comp' in x, words))

    f.writelines((y + '\n' for y in sorted(list(basic) + list(pl) + list(pst) + list(fem) + list(supl) + list(comp), key=lambda x: unidecode.unidecode(x).replace('[?]', ''))))
