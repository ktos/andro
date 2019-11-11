#!/usr/bin/env python
# coding: utf-8

from random import choice, random

consonants = [ 'b', 'ch', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'r', 's', 't', 'v', 'w', 'y', 'z' ]
vowels = [ 'a', 'e', 'i', 'o', 'u' ]

consonants1 = [ 'k', 'l', 'n', 'r', 's', 't' ]

def generate_syllable():
    first = ''
    second = ''
    third = ''
    
    if random() < 0.7:
        first = choice(consonants)

    second = choice(vowels)

    if random() < 0.3:
        third = choice(consonants1)

    return first + second + third

syllabes = []

for i in range(300):
    syllabes.append(generate_syllable())

for k in range(2):
    for i in range(22):
        word = ''
        for j in range(3, 5 + k):
            word += choice(syllabes)

        print(word)