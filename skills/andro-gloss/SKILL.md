---
name: andro-gloss
description: Gloss Andro words and sentences into grammatical labels using the repository's gloss.py. Use when the user asks to gloss, analyze, or break down Andro text word by word.
---

# Andro Glossing

Glosses Andro words and sentences with the repository's `gloss.py` command.

## When to use

- The user asks for an Andro word's gloss
- The user asks to gloss or analyze an Andro sentence
- The user wants a word-by-word grammatical analysis of Andro text

## How to gloss

Run from the repository root:

```bash
python gloss.py <sentence>
python gloss.py "mucha kato"
echo "mucha kato" | python gloss.py
```

The command accepts one optional argument. If the argument is omitted, or is
`-`, it reads one line from standard input. Input must not be empty.

## Output

The output is one space-separated gloss for each input word, in the same order:

```text
mucha kato
```

Gloss conventions include:

- `.PRS` for the present form of verbs beginning with `to` in the English description
- `-PST` for past-tense verb forms
- `-ADJ` for adjectives
- `-PL`, `-F`, `-COMP`, and `-SUP` for corresponding inflected forms
- `[REDIRECT!]` for dictionary redirects
- `[!]` after an unknown or uncertain word
- `-POSS` for an unrecognized word ending in the possessive suffix `-yi`
- Multiple possible analyses separated by `/`

Punctuation marks `, . ; ? !` are removed before glossing, and matching is
case-insensitive with Unicode normalization.

## Examples

```bash
python gloss.py "mucha kato"
# cat-F kato[!]

python gloss.py "unknown"
# unknown[!]

printf '%s\n' "mucha kato" | python gloss.py
# cat-F kato[!]
```

## Tips

- Pass the complete sentence as one quoted argument so the shell does not split it into multiple arguments.
- Use stdin for text assembled by another command or for input containing shell-sensitive characters.
- For dictionary meanings and inflected-form lookup, use `andro-search` with `python search.py` instead.
- For pronunciation, use `python ipa.py <word>`.
