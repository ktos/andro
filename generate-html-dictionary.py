import csv
import ntpath
import json
import os.path
import shutil
import sys
import dictionaryparser

def format_description(desc):
    desc = desc.replace("<see>", '<a class="see" href="#">')
    desc = desc.replace("</see>", '</a>')

    desc = desc.replace("<phrase>", "<em>")
    desc = desc.replace("</phrase>", "</em>")

    desc = desc.replace("<em>", "<em>")
    desc = desc.replace("</em>", "</em>")

    desc = desc.replace("<alt>", "<em>")
    desc = desc.replace("</alt>", "</em>")

    desc = desc.replace("<sc>", '<span class="sc">')
    desc = desc.replace("</sc>", "</span>")

    desc = desc.replace("--", "—")
    desc = desc.replace(",,", "„")
    desc = desc.replace("''", "”")
    desc = desc.replace("~", "&nbsp;")
    desc = desc.replace("\-", "")

    return desc

def copy_template():
    name = f"final/html/"
    template = f"html-template"

    if not os.path.exists(name):
        os.makedirs(name)
    for filename in os.listdir(template):
        target = name + filename
        templateFile = template + "/" + filename
        if os.path.isdir(templateFile):
            if os.path.exists(target):
                shutil.rmtree(target)
            shutil.copytree(templateFile, target)  # copy template
        else:
            if os.path.exists(target):
                os.remove(target)
            shutil.copy(templateFile, target)  # copy template


def generate_words(rows, lang):
    words = []

    for i, row in enumerate(rows):
        if lang == 'pl':
            word = {
                "id": i,
                "word": row['word'],
                "translation": format_description(row['description']),
                "type": row['type'],
                "ipa": row['speech'],
                "notes": [],
                "examples": row['examples']
            }

            for j in row['notes']:
                word['notes'].append(format_description(j))
        elif lang == 'en':
            word = {
                "id": i,
                "word": row['word'],
                "translation": format_description(row['english_description']),
                "type": row['type'],
                "ipa": row['speech'],
                "notes": [],
                "examples": row['english_examples']
            }

            for j in row['english_notes']:
                word['notes'].append(format_description(j))

        for j in ['pl', 'fem', 'pst', 'comp', 'supl']:
            if j in row:
                word[j] = row[j]
                word[j + "_speech"] = row[j + "_speech"]

        words.append(word)
    return words


def getRowsFromFile(fileLocation):
    with open(fileLocation, "r") as f:
        return list(csv.reader(f))


def main():
    langs = ['pl', 'en']
    words = {}

    dictionary = dictionaryparser.read_dictionary('dictionary.csv')    
    copy_template()

    for i in langs:
        words[i] = generate_words(dictionary, i)

        with open(f'final/html/scripts/words-{i}.js', 'w') as file:
            file.write(f"const words_{i} = " + json.dumps(words[i], separators=(',', ':')) + ";")

    print(f"Done! Open final/html/index.html")


if __name__ == '__main__':
    main()
