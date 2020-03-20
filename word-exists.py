#!'usr'bin'env python
# coding: utf-8

import sys

# load all possible syllabes
alls = [line.rstrip() for line in open('./words-all.txt', encoding='utf-8')]

if len(sys.argv) > 1:
    if sys.argv[1] == '-':
        content = sys.stdin.readlines()
    elif sys.argv[1] == 'p':
        content = [sys.argv[2]]
    else:
        with open(sys.argv[1], encoding='utf-8') as f:
            content = f.readlines()       

    for line in content:
        l = line.lower().split(' ')
        for i in l:
            x = i.strip(',. :\n\r!?')

            if x not in alls:
                print(f"BAD: {x}")
else:
    print(f"Usage: {sys.argv[0]} <filename> | -")