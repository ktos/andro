#!/usr/bin/env python
# coding: utf-8

import unidecode
import sys

# output
output = []

# all syllabes
alls = [line.rstrip() for line in open('./syllabes.txt', encoding='utf-8')]


def print_output(str=""):
    """Prints to output"""
    output.append(str)


def check_syllabes(speech):
    l = speech.strip().replace("ˈ", "")
    for i in l.split('.'):
        if i not in alls:
            print(f"SYLLABLE WARN: {l} (because of {i})")


def parse_descfile(worddesc):
    """Parses dictionary description file into objects"""
    x = {}    

    try:
        x['word'] = worddesc[0]  # słowo
        x['noaccent_word'] = unidecode.unidecode(worddesc[0]).replace('[?]', '')
        x['speech'] = worddesc[1]  # wymowa
        if not 'ˈ' in x['speech']:
            x['speech'] = 'ˈ' + x['speech']

        check_syllabes(x['speech'])

        x['type'] = worddesc[2]  # część mowy
        x['notes'] = []

        for i in worddesc[2:]:
            if i.startswith("note:"):
                x['notes'].append(i[5:])
            elif i == "fem":
                x['fem'] = "FEM"
            elif i.startswith("fem:") and x['type'] == "n":
                fem = i[4:].split(" ")
                x['fem'] = fem[0]
                x['fem_speech'] = fem[1]
                if not 'ˈ' in x['fem_speech']:
                    x['fem_speech'] = 'ˈ' + x['fem_speech']
            elif i.startswith("pst:") and x['type'] == "v":
                pst = i[4:].split(" ")
                x['pst'] = pst[0]
                x['pst_speech'] = pst[1]
                if not 'ˈ' in x['pst_speech']:
                    x['pst_speech'] = 'ˈ' + x['pst_speech']
            elif i.startswith("pl:") and x['type'] == "n":
                pst = i[3:].split(" ")
                x['pl'] = pst[0]
                x['pl_speech'] = pst[1]
                if not 'ˈ' in x['pl_speech']:
                    x['pl_speech'] = 'ˈ' + x['pl_speech']
            elif i.startswith("comp:") and x['type'] == "adj":
                pst = i[5:].split(" ")
                x['comp'] = pst[0]
                x['comp_speech'] = pst[1]
                if not 'ˈ' in x['comp_speech']:
                    x['comp_speech'] = 'ˈ' + x['comp_speech']
            elif i.startswith("supl:") and x['type'] == "adj":
                pst = i[5:].split(" ")
                x['supl'] = pst[0]
                x['supl_speech'] = pst[1]
                if not 'ˈ' in x['supl_speech']:
                    x['supl_speech'] = 'ˈ' + x['supl_speech']
            elif i.startswith("red:"):
                pst = i[4:]
                x['redirect'] = pst
            else:
                x['description'] = i

        if (len(x['description']) == 0):
            raise "description"
    
    except:
        print("ERROR WORDDESC: " + str(worddesc))

    return x


def generate_tex_dictionary_entry(w):
    """Generates TeX dictionary entry based on an parsed descfile object"""
    output = []

    if not 'redirect' in w:
        description = w['description'].replace("{", "\\emph{")

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
        note = note.replace("{", "\\emph{")

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


# reads dictionary descfile
with open('../dictionary.csv', 'r', encoding='utf-8') as f:
    data = f.readlines()

words = []

# parse words in descfile
for i in data:
    words.append(parse_descfile(i.strip().split("|")))

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
    f.writelines(y['word'] + '\n' for y in sorted_words)

# save list of all words forms to file
with open('./words-all.txt', 'w', encoding='utf-8') as f:

    basic = (x['word'] for x in words)
    pl = (x['pl'] for x in filter(lambda x: 'pl' in x, words))
    pst = (x['pst'] for x in filter(lambda x: 'pst' in x, words))
    fem = (x['fem'] for x in filter(lambda x: 'fem' in x and x['fem'] != 'FEM', words))
    supl = (x['supl'] for x in filter(lambda x: 'supl' in x, words))
    comp = (x['comp'] for x in filter(lambda x: 'comp' in x, words))

    f.writelines((y + '\n' for y in sorted(list(basic) + list(pl) + list(pst) + list(fem) + list(supl) + list(comp), key=lambda x: unidecode.unidecode(x).replace('[?]', ''))))
