---
name: andro-search
description: Search the Andro conlang dictionary by word (including inflected forms, accent-insensitive) or by English/Polish description text. Use when the user asks to look up, find, translate, or check a word in the Andro language, or wants words matching a phrase.
---

# Andro Dictionary Search

Searches the Andro conlang dictionary (`dictionary.csv` + `names.csv`) using the repo's `search.py`.

## When to use

- The user asks what an Andro word means (or what an inflected form is)
- The user wants to find words whose English or Polish description contains a phrase
- Checking whether a string appears as a word or inflection in the dictionary

## How to search

Run from the repo root (the script uses relative paths; `.venv` has the only dependency, `unidecode`):

```bash
python search.py <phrase>          # word forms + English descriptions (default)
python search.py -l pl <phrase>    # word forms + Polish descriptions
echo "cat" | python search.py      # phrase can also come from stdin
```

Matching behavior:

- Accent-insensitive: `kato` matches `kàto` (both sides are unidecoded, `[?]` dropped, lowercased)
- Word side: substring match against the base form and all inflected forms (`pl`, `fem`, `pst`, `comp`, `supl`)
- Description side: case-insensitive substring match in English (`en:`) or Polish descriptions
- Both sides are checked for every entry, so one query can hit words and descriptions at once

## Output format

One line per match:

```
word (type) (pl:form) (fem:form)...: description: Note: note text
```

- `(pl:...)`, `(pst:...)` etc. are the stored inflected forms; a bare `(fem)` means the feminine form is unspecified in the data
- `Note:` segments come from English notes (`ennote:`) or Polish notes (`note:`), depending on `-l`
- Pseudo-HTML markup in descriptions (`<see>`, `<phrase>`, `<em>`, `<alt>`, `<sc>`) is stripped, content kept

Exit code: `0` when at least one match is printed; `1` with `no entries found for '<phrase>'` on stderr when there are none.

## Examples

```bash
python search.py "muchyo"
# muchi (n) (pl:muchyo) (fem:muchya): small cat, kitten: Note: mućhi, mućhi -- ,,here, kitty, kitty''.

python search.py -l pl "kot"
# mucha (n) ...: kot, kotka  (plus other entries whose Polish description contains "kot")
```

## Tips

- Matching is substring-based, so short queries return many hits; prefer the longest distinctive fragment
- If nothing is found, retry with an unaccented spelling or a shorter fragment
- `phraseology.csv` (phrases and idioms) is NOT covered by search.py; grep that file directly for phrase lookups
- For IPA pronunciation use `python ipa.py <word>`; to gloss a whole sentence use `python gloss.py "<sentence>"`
