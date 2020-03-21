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

def copy_template(lang):
    name = f"final/html-{lang}/"
    template = f"html-{lang}-template"

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


def generate_words(rows):
    words = []

    for i, row in enumerate(rows):
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
    if len(sys.argv) > 1:
        lang = sys.argv[1]
    else:
        lang = 'pl'

    dictionary = dictionaryparser.read_dictionary('dictionary.csv')
    words = generate_words(filter(lambda x: x['type'] not in [
                           'name', 'phraseology'], dictionary))
    copy_template(lang)

    with open(f'final/html-{lang}/scripts/words.js', 'w') as file:
        file.write("const words = " + json.dumps(words,
                                                 separators=(',', ':')) + ";")

    print(f"Done! Open final/html-{lang}/index.html")


if __name__ == '__main__':
    main()
