#!/usr/bin/env python
# coding: utf-8

import glob
import os
import re
import sys

TEX_DIR = 'the-book'
DEFAULT_OUTPUT = './final/examples.md'


def read_tex_files():
    """Yield (path, source) for every .tex file under the-book/"""
    files = sorted(glob.glob(os.path.join(TEX_DIR, '**', '*.tex'), recursive=True))
    for path in files:
        with open(path, encoding='utf-8') as f:
            src = f.read()
        # drop commented-out lines
        src = '\n'.join(line for line in src.split('\n') if not line.lstrip().startswith('%'))
        yield path, src


def parse_glossex(src):
    """Extract all \\glossex{a}{b}{c}{d} calls from TeX source.

    Returns a list of (andro, text, gloss, english) tuples. Handles nested
    braces (e.g. \\textbf{...}); if the final closing brace is missing the
    rest of the line is taken as the last argument."""
    entries = []
    for m in re.finditer(r'\\glossex\b', src):
        i = m.end()
        n = len(src)
        args = []
        while len(args) < 4 and i < n:
            while i < n and src[i] in ' \t\r\n':
                i += 1
            if i >= n or src[i] != '{':
                break
            i += 1
            depth = 1
            buf = []
            closed = False
            while i < n:
                c = src[i]
                if c == '\\':
                    buf.append(src[i:i + 2])
                    i += 2
                    continue
                i += 1
                if c == '{':
                    depth += 1
                elif c == '}':
                    depth -= 1
                    if depth == 0:
                        closed = True
                        break
                buf.append(c)
            if not closed:
                line_end = src.find('\n', i)
                if line_end == -1:
                    line_end = n
                buf.append(src[i:line_end])
                i = line_end
            args.append(''.join(buf))
        while len(args) < 4:
            args.append('')
        entries.append(tuple(args))
    return entries


def tex_to_md(text):
    """Convert the small LaTeX markup used in glossex to Markdown"""

    def bold(match):
        return '**' + match.group(1).strip() + '**'

    text = re.sub(r'\\textbf\{([^{}]*)\}', bold, text)
    # strip any remaining backslash commands
    text = re.sub(r'\\[a-zA-Z]+', '', text)
    text = text.replace('``', '"')
    text = text.replace("''", '"')
    text = text.replace('--', '—')
    return text.strip()


def split_translations(english):
    """Split ``A.'' \\ ``B.'' into a list of plain translations"""
    out = []
    for part in re.split(r'\\\\', english):
        part = tex_to_md(part).strip('"').strip()
        if part:
            out.append(part)
    return out


def main():
    output_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUTPUT

    output = ['# Andro glossed examples']
    count = 0

    for path, src in read_tex_files():
        for andro, text, gloss, english in parse_glossex(src):
            translations = split_translations(english)
            if not translations and not andro.strip():
                continue

            heading = ' / '.join(translations) if translations else tex_to_md(andro)
            output.append('')
            output.append(f'## {heading}')

            if andro.strip():
                output.append('')
                output.append(f'*{tex_to_md(andro)}*')

            if text.strip() or gloss.strip():
                output.append('')
                output.append('```')
                output.append(text)
                output.append(gloss)
                output.append('```')

            count += 1

    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output) + '\n')

    print(f'Wrote {count} examples to {output_path}')


if __name__ == '__main__':
    main()
