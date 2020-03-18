import csv
import ntpath
import json
import os.path
import shutil
import sys
import dictionaryparser

def inject_name(name):
    with open(name + "/index.html", "r+") as f:
        data = f.read()
        f.seek(0)
        f.write(data.replace("<!-- NAME -->", name, 2))
        f.truncate()

def copy_template(name):
    if not os.path.exists(name):
        os.makedirs(name)
    for filename in os.listdir("template"):
        target = name + "/" + filename
        templateFile = "template/" + filename
        if os.path.isdir(templateFile):
            if os.path.exists(target): shutil.rmtree(target)
            shutil.copytree(templateFile, target) # copy template
        else:
            if os.path.exists(target): os.remove(target)
            shutil.copy(templateFile, target) # copy template

def generate_words(rows):
    words = []    

    for i, row in enumerate(rows):
        if (i == 0): continue
        
        word = {
                "id":          i - 1,
                "word":        row['word'],
                "english":     row['description'],
                "types":       [row['type']],
                "ipa":         row['speech'],
                "definitions": [row['notes']],
                "examples":    []
                }
        
        words.append(word)
    return words

def getRowsFromFile(fileLocation):
    with open(fileLocation, "r") as f:
        return list(csv.reader(f))


def main():
    fileLocation = sys.argv[1]
    name = ntpath.basename(fileLocation).split(".")[0]

    dictionary = dictionaryparser.read_dictionary('../dictionary.csv')    
    words = generate_words(filter(lambda x: x['type'] not in ['name', 'phraseology'], dictionary))
    copy_template(name)

    with open(name + '/scripts/words.js', 'w') as file:
        file.write("const words = " + json.dumps(words, separators=(',', ':')) + ";")
    inject_name(name)
    print("Done! Open " + name + "/index.html")

if __name__ == '__main__':
    main()
