import unidecode
import pyandro.dictionary as dictionary

# read and parse dictionary file
words = dictionary.read_dictionary('dictionary.csv')

# sort words without accents
sorted_words = sorted(words, key=lambda x: x['noaccent_word'].lower())

# save list of all basic forms of words to file
with open('./final/words-basic.txt', 'w', encoding='utf-8') as f:
    f.writelines(y['word'] + '\n' for y in filter(lambda x: x['type']
                 not in ['name', 'phraseology', 'proper'], sorted_words))

# save list of all words forms to file
with open('./final/words-all.txt', 'w', encoding='utf-8') as f:

    basic = (x['word'] for x in filter(lambda x: x['type']
             not in ['name', 'phraseology', 'proper'], words))
    pl = (x['pl'] for x in filter(lambda x: 'pl' in x, words))
    pst = (x['pst'] for x in filter(lambda x: 'pst' in x, words))
    fem = (x['fem']
           for x in filter(lambda x: 'fem' in x and x['fem'] != 'FEM', words))
    supl = (x['supl'] for x in filter(lambda x: 'supl' in x, words))
    comp = (x['comp'] for x in filter(lambda x: 'comp' in x, words))

    f.writelines((y + '\n' for y in sorted(list(basic) + list(pl) + list(pst) + list(fem) +
                 list(supl) + list(comp), key=lambda x: unidecode.unidecode(x).replace('[?]', ''))))
