---
name: andro-ipa
description: Convert Andro words and sentences to IPA phonemization using the repository's ipa.py. Use when the user asks for Andro pronunciation, phonetic transcription, or IPA output.
---

# Andro IPA Phonemization

Converts Andro words and sentences into IPA with the repository's `ipa.py`
command.

## When to use

- The user asks how an Andro word is pronounced
- The user asks for an IPA or phonetic transcription
- The user wants to phonemize an Andro sentence

## How to phonemize

Run from the repository root:

```bash
python ipa.py <word>
python ipa.py mucha
python ipa.py "mucha kato"
echo "mucha kato" | python ipa.py
```

The command accepts one optional argument. If the argument is omitted, or is
`-`, it reads one line from standard input. Input must not be empty.

## Output

The result is enclosed in `/` and contains one IPA representation per input
word, separated by spaces:

```text
/ˈmu.ʈ͡ʂa/
/mu.ʈ͡ʂa katɔ[!]/
```

A single word receives its initial primary-stress marker. In a sentence, the
initial stress marker is omitted from each word. The command decides this by
checking whether the input contains a literal space.

IPA conventions include:

- Dot-separated syllables
- `ˈ` for primary stress
- `[!]` after heuristic or otherwise uncertain phonemization
- `ʏ[!]` for an inferred possessive suffix `-yi` when the base is recognized
- Names are checked after ordinary dictionary entries
- Unknown words fall back to direct romanization and receive `[!]`

Punctuation marks `, . ; ? !` are removed before phonemization, and matching is
case-insensitive with Unicode normalization.

## Examples

```bash
python ipa.py mucha
# /ˈmu.ʈ͡ʂa/

python ipa.py "mucha kato"
# /mu.ʈ͡ʂa katɔ[!]/

python ipa.py unknown
# /ˈunknɔwn[!]/

printf '%s\n' mucha | python ipa.py
# /ˈmu.ʈ͡ʂa/
```

## Tips

- Pass a complete sentence as one quoted argument so the shell does not split it into multiple arguments.
- Use stdin for text assembled by another command or for input containing shell-sensitive characters.
- For grammatical glosses, use `andro-gloss` with `python gloss.py <sentence>`.
- For dictionary meanings and inflected-form lookup, use `andro-search` with `python search.py`.
