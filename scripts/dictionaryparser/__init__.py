import unidecode

def parse_descfile_word(worddesc):
    """Parses dictionary description file into objects"""
    x = { 'description': '' }

    # try:
    x['word'] = worddesc[0]  # słowo
    x['noaccent_word'] = unidecode.unidecode(
        worddesc[0]).replace('[?]', '')
    x['speech'] = worddesc[1]  # wymowa
    if not 'ˈ' in x['speech'] and x['speech'] != '':
        x['speech'] = 'ˈ' + x['speech']

    x['type'] = worddesc[2]  # część mowy
    x['notes'] = []
    x['examples'] = []

    x['english_notes'] = []
    x['english_examples'] = []

    for i in worddesc[3:]:
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
        elif i.startswith("example:"):
            ennote = i[8:]
            x['examples'].append(ennote)
        elif i.startswith("en:"):
            en = i[3:]
            x['english_description'] = en
        elif i.startswith("ennote:"):
            ennote = i[7:]
            x['english_notes'].append(ennote)
        elif i.startswith("enexample:"):
            ennote = i[10:]
            x['english_examples'].append(ennote)
        else:
            x['description'] = i

    if len(x['description']) == 0 and 'redirect' not in x and x['type'] != 'name':
        print("WARNING: EMPTY DESCRIPTION in " + str(worddesc))

    return x

def read_dictionary(path):
    # reads dictionary descfile
    with open(path, 'r', encoding='utf-8') as f:
        data = f.readlines()    

    words = []

    # parse words in descfile
    for i in data:
        words.append(parse_descfile_word(i.strip().split("|")))

    return words