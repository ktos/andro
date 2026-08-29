# AGENTS.md

## Project Overview

**Andro** is a constructed-language (conlang) documentation project, licensed CC-BY 4.0. It contains:

- A grammar reference guide in LaTeX (`the-book/` → `andro-language-reference-guide.pdf`)
- Two small dictionaries in LaTeX: Polish-Andro and English-Andro (`small-andro-polish-dictionary/`, `small-andro-english-dictionary/`)
- Dictionary source data as pseudo-CSV files at the repo root
- Python generator scripts that turn the data into TeX entries, Markdown tables, wordlists, and an HTML web dictionary
- An HTML template for the live web dictionary (https://androlang.netlify.app/#en)

The only Python dependency is `Unidecode>=1.1.1` (see `requirements.txt`). There is no pyproject/setup.py; scripts are run directly from the repo root. A local venv lives in `.venv/`.

## Repository Layout

```
dictionary.csv          # main dictionary data (~1942 lines)
names.csv               # proper names (~49 lines)
phraseology.csv         # phrases and idioms (~47 lines)
syllabes.txt            # list of valid syllables, used by check-words.py
pyandro/                # the real Python package
  dictionary.py         # parser for the pseudo-CSV data files
  phonemizer.py         # IPA romanization (AndroPhonemizer)
  glosser.py            # word/sentence glossing (AndroGlosser)
html-template/          # static web-dictionary template (index.html, phoglo.html, style/, scripts/)
final/                  # ALL generated output lands here (PDFs, tables-*.md, words-*.txt, html/)
the-book/               # LaTeX: grammar reference guide
small-andro-polish-dictionary/   # LaTeX: Polish dictionary
small-andro-english-dictionary/  # LaTeX: English dictionary
```

Root-level scripts (all run from the repo root, all use relative paths):

| Script | Purpose |
|---|---|
| `check-words.py` | Validate syllables/romanization/descriptions in the data files; modes below |
| `generate-tex-dictionary.py [en]` | Generate `ap.tex` + `pa.tex` (forward/reverse entries) into the Polish or English dictionary dir |
| `generate-md.py [en]` | Generate `final/tables-pl.md` or `final/tables-en.md` |
| `generate-wordlist.py` | Generate `final/words-basic.txt` and `final/words-all.txt` (no args) |
| `generate-html-dictionary.py` | Copy `html-template/` → `final/html/` and write `final/html/scripts/words-{pl,en}.js` (no args, always both languages) |
| `sort-csv.py [file]` | Sort a data file in place by unidecoded first field (default `dictionary.csv`) |
| `word-exists.py <file> \| - \| p <word>` | Flag words not present in `final/words-all.txt` |
| `random-words.py` | Generate random candidate words not yet in the wordlist (no args) |
| `gloss.py [sentence]` | Gloss a sentence via `AndroGlosser` (stdin if no arg) |
| `search.py [phrase] [-l {en,pl}]` | Substring-search words (incl. inflected forms, accent-insensitive) and English (`--lang en`, default) or Polish descriptions; prints each match as `word: description[: Note: ...]` on one line (stdin if no arg) |
| `ipa.py [word]` | IPA romanization via `AndroPhonemizer`; front accent only for single words (stdin if no arg) |
| `arbabet.py [word]` | ARPAbet output (stdin if no arg) |
| `and_phonemizer.py` | Coqui TTS (`🐸TTS`) phonemizer wrapper — see gotchas; not runnable with the declared deps |

## The Data Format (pseudo-CSV)

**The data files are NOT real CSV.** Lines are pipe-separated with a variable number of fields:

```
word|IPA-speech|type|prefixed-fields...
```

Parsing lives in `pyandro/dictionary.py` (`read_dictionary(path, type)`). Fields after the third are interpreted by prefix:

| Prefix | Meaning / applies to |
|---|---|
| `pl:` | plural form (n only) |
| `pst:` | past tense (v only) |
| `fem:` | feminine form (n only) |
| `fem` (bare token, no colon) | feminine-only placeholder; stored as the literal string `"FEM"`, skipped by syllable checks, rendered `!!` in Markdown |
| `comp:` | comparative (adj only) |
| `supl:` | superlative (adj only) |
| `red:` | redirect target. **Not documented in README.** Glosser emits `[REDIRECT!]`; entry is skipped entirely in MD output and exempt from the empty-description check |
| `note:` | note text, appended to notes |
| `morph:` | morphology annotation. **Must split into exactly 2 space-separated tokens** (enforced by `check-words.py`). Appended to notes in HTML output |
| `example:` | example sentence (PL) |
| `en:` | English description/translation |
| `ennote:` | English note |
| `enexample:` | English example |
| `src:` | source reference |
| `!ignore_err` | exempts the entry from all checks. **Not documented in README** |
| (no prefix) | free text → description; if multiple, the last one wins |

**Type-gating is silent**: a type-gated prefix on the wrong word type (e.g. `pl:` on an adjective) is silently ignored — no error is raised. Word types observed in the data: `n adj v part name phraseology idiom pro proper`.

Additional parser behavior:

- IPA uses dot-separated syllables with `ˈ` marking primary stress. If `ˈ` is absent, the parser **auto-prepends it** to the main word's speech and to every inflection's speech (`pl_speech`, `pst_speech`, etc.).
- `noaccent_word = unidecode(word).replace('[?]', '')` — this is what drives sorting.
- `phraseology.csv` format: `word|type|description|en:...` — the 4th field must start with `en:`.
- `names.csv` entries are parsed by the same word parser (type `name`).
- Lines are split via `strip().split("|")`.

### Pseudo-HTML markup in descriptions

Descriptions use a small inline markup: `<see>`, `<phrase>`, `<em>`, `<alt>`, `<sc>`, plus escapes `--` → em dash, `,,` → „, `''` → ”, `~` → non-breaking space, `\-` (removed). How each output renders them differs:

- **TeX**: `<see>` becomes plain `\emph{}` — *not* a link.
- **HTML**: `<see>` becomes `<a class="see" href="#">` — a dead anchor; `<phrase>/<em>/<alt>` → `<em>`; `<sc>` → `<span class="sc">`.
- **Markdown**: everything collapses to `*`.

## Commands

All Python commands run from the repo root. The local interpreter is `.venv` (contains only unidecode).

```bash
# Validation
python check-words.py            # default: prints warnings with WARN prefix
python check-words.py strict     # CI gate: FAIL prefix, exit(1) on first problem
python check-words.py single <IPA-string>   # check dot-split syllables against syllabes.txt only

# Generation (order matters where noted)
python generate-tex-dictionary.py        # Polish → small-andro-polish-dictionary/
python generate-tex-dictionary.py en     # English → small-andro-english-dictionary/
python generate-md.py [en]               # → final/tables-{pl,en}.md
python generate-wordlist.py              # → final/words-basic.txt, final/words-all.txt
python generate-html-dictionary.py       # → final/html/ (both languages)

# Must run AFTER generate-wordlist.py (they read ./final/words-all.txt):
python random-words.py
python word-exists.py <file> | - | p <word>

# Utilities
python sort-csv.py [file]      # default dictionary.csv; sorts in place
python gloss.py [sentence]     # stdin if no arg
python ipa.py [word]           # stdin if no arg
python arbabet.py [word]       # stdin if no arg
```

### LaTeX builds

Each of the three projects is built independently with `latexmk main.tex` inside its directory. All three have an identical `.latexmkrc`:

- `$pdflatex = "xelatex %O %S"` — **XeLaTeX, not pdfLaTeX** (the variable name is misleading)
- `pdf_mode 1`
- Custom hook running `makeglossaries` for `.glo→.gls` and `.acn→.acr` (glossaries + acronym packages)

So a full local build requires a TeX installation with XeLaTeX and makeglossaries, run once per project directory.

## CI Pipeline

Two workflows in `.github/workflows/`:

**`generate-pdf.yml`** — runs only when `**/*.tex` or `dictionary.csv` changes (built-in `paths:` trigger filter; the tex generator reads only `dictionary.csv`). Sequence:

1. Checkout
2. Python 3.10 setup + `pip install -r requirements.txt`
3. `python check-words.py strict` ← **the validation gate; nothing builds if this fails**
4. `generate-tex-dictionary.py` and `… en` (writes ap.tex/pa.tex into both dictionary dirs)
5. Compile all three LaTeX projects via `xu-cheng/latex-action@v3` (root_file `main.tex`)
6. Copy the PDFs to:
   - `final/small-andro-polish-dictionary.pdf`
   - `final/small-andro-english-dictionary.pdf`
   - `final/andro-language-reference-guide.pdf`
7. Upload `final/*.pdf` as artifact `pdfs`

**`generate-md-html.yml`** — runs on every push/PR to master (no path filter):

1. Checkout, Python 3.10 setup + deps
2. `python check-words.py strict` (validation gate)
3. `generate-md.py`, `… en`, `generate-wordlist.py`
4. `generate-html-dictionary.py`
5. Upload `final/tables-*.md`, `final/words-*.txt`, `final/html` as artifact `md-html`

Only the two small dictionaries `\input{ap.tex}` / `\input{pa.tex}` (Polish at `main.tex:107,110`, English at `main.tex:99,102`). **`the-book` does not include them** — regenerating ap/pa.tex has no effect on the grammar book.

## Data-File Invariants

These are enforced by `check-words.py strict` (the CI gate) and must hold for any edit to `dictionary.csv`:

1. **Sorted by unidecoded word** (`unidecode` of the first pipe field). Fix with `python sort-csv.py`.
2. **File must end with a trailing newline.**
3. Every syllable in speech + all inflection speeches must appear in `syllabes.txt` (checked via romanization); entries marked `!ignore_err` and bare-`FEM` values are skipped.
4. Both PL description and EN (`en:`) must be non-empty — except redirects and type `name`.
5. `morph:` must be exactly 2 space-separated tokens.

## Gotchas

1. **Misplaced prefixes fail silently.** Type-gated prefixes (`pl:`/`fem:` need `n`, `pst:` needs `v`, `comp:`/`supl:` need `adj`) on the wrong type are dropped without error. If an inflection "disappears", check the word's type first.
2. **`check-words.py:24–25`:** romanization mishandles `ŋ` — it is replaced with `n` for comparison purposes only (a known workaround, not a bug fix).
3. **`[!]` markers are meaningful:** the phonemizer appends `[!]` to heuristic/unverified IPA output; the glosser returns `word + "[!]"` for unknown words and base-gloss + `-POSS` for unknown words ending in `-yi` (possessive suffix).
4. **Glosser output conventions:** redirect → `[REDIRECT!]`; multiple matches joined by `/`; gloss suffixes `.PRS`/`-PST` for `to …` verbs, `-ADJ`, `-PL`, `-F`, `-SUP`, `-COMP`; `<sc>…</sc>` in a description is extracted and uppercased.
5. **TeX section-letter quirks** (`generate-tex-dictionary.py`): forward Andro sections skip Q and X and use standalone `CH` (lines 153–154); reverse Polish sections add Ć, Ł, Ó, Ś, Ż, Ź (lines 180–181). Don't "normalize" these.
6. **CWD assumption:** every root script assumes CWD = repo root (relative paths). The exception is `pyandro/glosser.py`, which resolves `dictionary.csv`/`names.csv` relative to its own file location and works from any CWD.
7. **`and_phonemizer.py` is not runnable with declared deps.** It imports Coqui TTS (`TTS.tts.utils.text.phonemizers.base`), which is in neither `requirements.txt` nor CI. Treat it as an optional external integration, not a repo script.
8. **Ordering dependency:** `random-words.py` and `word-exists.py` read `./final/words-all.txt`, so they must run after `generate-wordlist.py`.
9. **Minor bugs in check-words.py** (cosmetic, don't "fix" casually): line 97's missing-newline warning is missing its f-string prefix and prints the literal `{lprefix}`; `single <IPA>` mode passes the literal label `"stdin"` as the word for the romanization half of the check.
10. **Wordlist filtering:** `words-basic.txt` contains basic forms only and excludes types `name`, `phraseology`, `proper`; `words-all.txt` includes basic + pl/pst/fem(excl `FEM`)/supl/comp across ALL words including names, sorted by `unidecode(x).replace('[?]', '')`.
11. **HTML word JSON:** each entry gets a 0-based `id` (same order in both languages), and for every present inflection the generator adds both the value and a `{j}_speech` field (`pl_speech`, `fem_speech`, …). The template's `index.html:51–52` loads exactly `scripts/words-en.js` and `scripts/words-pl.js`.
12. **README is authoritative but incomplete:** it documents the data format (lines 135–216) but misses the `morph:`, `!ignore_err`, and `red:` prefixes — all real and enforced/parsed in code.
