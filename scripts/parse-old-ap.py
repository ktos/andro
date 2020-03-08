# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import re

data = []

with open('../ap.tex', 'r', encoding='utf-8') as f:
    data = f.readlines()

# %%
words = []

for i in range(len(data)):
    if data[i].startswith("\\dictword"):
        w = {}
        w['word'] = re.findall(r"{(.*?)}", data[i])[0]
        w['speech'] = re.findall(r"\[(.*?)\]", data[i])[0]
        w['notes'] = []

    elif data[i].startswith("\\dictterm"):
        w['type'] = data[i][10:data[i].index('}')]

        description = data[i][10:]

        if "(\\textsc{fem})" in description:
            w['fem'] = 'FEM'
            description = description.replace("(\\textsc{fem})", '')

        if "(\\textsc{fem}" in data[i]:
            fem = re.findall(r"\(\\textsc{fem} (.*?)]", data[i])

            if len(fem) > 0:
                f = fem[0].split(' ')
                w['fem'] = f[0]
                w['fem_speech'] = f[1][1:]

                description = description.replace("(\\textsc{fem}", '')
                description = description.replace(w['fem'], '')
                description = description.replace(w['fem_speech'], '')

        if "(\\textsc{pl}" in data[i]:
            fem = re.findall(r"\(\\textsc{pl} (.*?)]", data[i])

            if len(fem) > 0:
                f = fem[0].split(' ')
                w['pl'] = f[0]
                w['pl_speech'] = f[1][1:]

                description = description.replace("(\\textsc{pl}", '')
                description = description.replace(w['pl'], '')
                description = description.replace(w['pl_speech'], '')

        if "(\\textsc{pst}" in data[i]:
            fem = re.findall(r"\(\\textsc{pst} (.*?)]", data[i])

            if len(fem) > 0:
                f = fem[0].split(' ')
                w['pst'] = f[0]
                w['pst_speech'] = f[1][1:]

                description = description.replace("(\\textsc{pst}", '')
                description = description.replace(w['pst'], '')
                description = description.replace(w['pst_speech'], '')

        if "(\\textsc{comp}" in data[i]:
            fem = re.findall(r"\(\\textsc{comp} (.*?)]", data[i])

            if len(fem) > 0:
                f = fem[0].split(' ')
                w['comp'] = f[0]
                w['comp_speech'] = f[1][1:]

                description = description.replace("(\\textsc{comp}", '')
                description = description.replace(w['comp'], '')
                description = description.replace(w['comp_speech'], '')

        if "\\textsc{supl}" in data[i]:
            fem = re.findall(r"\\textsc{supl} (.*?)]", data[i])

            if len(fem) > 0:
                f = fem[0].split(' ')
                w['supl'] = f[0]
                w['supl_speech'] = f[1][1:]

                description = description.replace("\\textsc{supl}", '')
                description = description.replace(w['supl'], '')
                description = description.replace(w['supl_speech'], '')

        w['description'] = description.replace('{', '').replace('}', '').replace('[', '').replace(']', '').replace(')', '').replace('  ', '')
        if w['description'].startswith(w['type']):
            w['description'] = w['description'][len(w['type']):].strip()

        if w['description'].startswith(','):
            w['description'] = w['description'][1:]

        words.append(w)

    elif data[i].startswith("\\dictred"):
        w['redirect'] = re.findall(r"{(.*?)}", data[i])[0]

    elif data[i].startswith("\\note"):
        w['notes'].append(data[i][6:].replace("\\emph", ""))

    #elif not data[i].startswith("\\"):
    #    print(i)
    #    w['notes'].append(data[i][:-1])

    #elif data[i].startswith("\\"):
    #    words.append(w)
    #    w = {}
    #    w['notes'] = []

words = list(filter(lambda x: 'word' in x, words))

output = []

# %%
for i in words:    
    pl = f"pl:{i['pl']} {i['pl_speech']}" if 'pl' in i else ""
    
    fem = ""
    if 'fem' in i:
        if i['fem'] == 'FEM':
            fem = "fem"
        else:
            fem = f"fem:{i['fem']} {i['fem_speech']}"

    pst = f"pst:{i['pst']} {i['pst_speech']}" if 'pst' in i else ""
    supl = f"supl:{i['supl']} {i['supl_speech']}" if 'supl' in i else ""
    comp = f"comp:{i['comp']} {i['comp_speech']}" if 'comp' in i else ""
    
    notes = "note:" + " ".join(i['notes']) if len(i['notes']) > 1 else ""

    redirect = f"red:{i['redirect']}" if 'redirect' in i else ""

    output.append(f"{i['word']}\t{i['speech']}\t{i['type']}\t{pl}\t{fem}\t{supl}\t{comp}\t{pst}\t{i['description']}\t{notes}\t{redirect}")

with open('./dictionary2.tsv', 'w', encoding='utf-8') as f:
    f.writelines((x + '\n' for x in output))