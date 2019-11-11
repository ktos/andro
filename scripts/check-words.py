#!'usr'bin'env python
# coding: utf-8

import sys

# load all possible syllabes
alls = [line.rstrip() for line in open('./syllabes.txt', encoding='utf-8')]

if len(sys.argv) > 1:
    file_name = sys.argv[1] if sys.argv[1] != '-' else sys.stdin

    if file_name != sys.stdin:
        with open(file_name, encoding='utf-8') as f:
            content = f.readlines()            

    else:
        content = sys.stdin.readlines()

    for line in content:
        l = line.strip().replace("ˈ", "")
        for i in l.split('.'):
            if i not in alls:
                print(f"BAD: {l} (because of {i})")                
else:
    print(f"Usage: {sys.argv[0]} <filename> | -")