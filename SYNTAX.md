# Andro syntax for language models

This document summarizes the syntactic information in `the-book/chapters/syntax.tex`, with supporting morphology where it is needed to parse or generate sentences. It describes literary/high Andro unless a dialect is explicitly mentioned. Do not infer pronunciation or stress rules from this document.

## Core profile

- Andro is primarily analytic and uses many uninflected particles.
- It is mixed head-directionally: noun modifiers and most grammatical particles are head-final, while some verb-related constructions are head-initial.
- The default declarative clause order is **SVO**.
- The default direct-question order is **OSV**.
- The default subordinate-clause order is **SOV**.
- Grammatical particles may be omitted when their function is recoverable from word order and context.
- Personal pronouns, especially `mi` and `ti`, may be omitted. A subjectless clause can therefore be ambiguous between first and second person.

## Clause structure

### Declaratives

The normal pattern is:

```text
Subject Verb Object
Mi pazi muchi.
I like cats.
```

Adverbs, locative phrases, and other adjuncts commonly follow the verb or its object, but fronting is possible for emphasis or information structure. A clause may consist only of a verb or predicate when the subject is understood:

```text
Sormi ore.
The sun is rising now.
```

### Copular clauses

`esi` means “be” and is used for states, identity, classification, and descriptions:

```text
Myi muche esi ruko.
My cat is black.
```

The copula is often omitted, especially dialectally and in informal speech:

```text
Myi muche ruko.
My cat is black.
```

The copula may also be omitted in topic constructions. Do not treat every adjective-only predicate as an error.

### Topic marking

`ya` marks a topic, roughly “as for” or “regarding”. It is especially used for emphasis and can introduce a topic followed by a clause:

```text
Mi ya egla pazi.
As for me, I like her.
```

Topic constructions commonly have a subordinate-like **SOV** order. In ordinary literary Andro, `ya` is mainly emphatic; some analyses treat it as a conjunction rather than a distinct topic marker.

## Noun phrases

### Adjectives

Adjectives modifying nouns precede the noun and are therefore head-final:

```text
karie himji
beautiful women
```

Multiple adjectives may occur in either order:

```text
gruwe ruo pelir
big black dog
ruo gruwe pelir
black big dog
```

Adjectives do not agree in number or grammatical class. The same lexical adjective can modify a noun or a verb.

### Adverbial adjectives

When an adjective modifies a verb, it follows the verb and functions adverbially:

```text
Egla yon dio.
She looked back suddenly.
```

A full adjective phrase can likewise follow the verb:

```text
Mi fesgai recha tay.
I read every day.
```

This gives a useful contrast:

- `siro seja` = bright sun, adjective before noun
- `seja haji siro` = the sun shines brightly, adverb after verb

### Possession

The standalone possessive particle `yi` is head-final and normally follows the possessed noun, before the possessor:

```text
vipetode yi muche
cat's bowl / bowl of the cat
```

Possession can also be expressed with the suffix `-yi` on the possessor or possessive element:

```text
mucheyi vipetode
cat-POSS bowl
```

Nested possession may mix both strategies:

```text
vipetode yi myi arsityi natalia
bowl POSS 1SG.POSS parent-POSS mother
```

Possessive pronouns can function as possessors and can sometimes be used for genitive or dative marking, especially in older or formal usage.

### Number and class relevant to syntax

- Nouns normally have singular and plural forms.
- Plural suffixes include `-ji`, `-os`, `-s`, and sometimes `-i`; the correct form is lexical rather than fully predictable.
- Plural nouns are always grammatically masculine/non-feminine.
- Feminine nouns commonly use `-a`, but the unmarked masculine/non-feminine form can refer to a woman when gender is irrelevant or intentionally unspecified.
- Animate/inanimate distinctions mainly affect demonstratives, certain pronouns, and quantifier-like expressions.

## Case and adpositional particles

Case particles are normally **head-final**, following the noun phrase they mark. Accusative, genitive, and dative are often unmarked when word order makes the role clear.

| Function | Particle | Main use |
|---|---|---|
| Accusative | `chu` | Usually omitted; used for emphasis, in older texts, or in regional varieties |
| Possessive | `yi` | Possessed noun + `yi` + possessor; also a suffix `-yi` |
| Genitive | `chu` | Usually unmarked; emphatic/older use |
| Dative | `fo` | Marks the recipient/beneficiary, especially for emphasis |
| Instrumental | `da` | Tool or means used to perform an action |
| Comitative | `a` | “Together with” an animate participant |
| Locative | `in`, `on`, `an`, and others | Place, direction, time, and spatial relations |
| Ablative | `get`, `au` | “From”; `get` is especially associated with movement/change and derivational use |

Examples:

```text
Mi veydi chu yasaji.
I really see eels.                 # emphatic accusative

Mi jawirit chider fo ti.
I stole a bike for you.             # dative/beneficiary

Idak ostro da keja.
I opened the door with a key.       # instrumental

Mi labi a ti.
I play with you / we play together. # comitative

Mi loti in Nowaja.
I live in Nowaja.                   # locative
```

`in` is broad and can mark location, destination, and time. It can be omitted with nonspecific time expressions in informal speech. `on` is principally physical “on/onto”; `ner` means physically near, while `nea` can mean near either physically or figuratively. `a` is also a Desert-dialect locative particle, so its comitative and locative uses should not be combined without contextual disambiguation.

The negative particle `no` can negate a noun phrase in the special “instead of” construction:

```text
... no rujalaros femit
... instead of people hanging
```

## Negation

`no` is the ordinary negation particle. In ordinary verb clauses it is normally placed after the verb, including after a conjugated past-tense verb:

```text
Ti bugi no.
You do not lie.

Egi karlet no il rige.
He did not kill his lord.
```

In a negative imperative, `no` precedes the lexical verb and remains before the final imperative marker:

```text
Tori no dejitos do!
Do not throw the weapons!
```

Both a negative particle and a negative adverb may occur. This apparent double negative is grammatical and still expresses ordinary negation:

```text
Ze karli no moli.
I will never die.
```

In some religious and formal texts, `no` may instead occur at the end of the whole sentence.

The derivational prefix `no-` can form an antonymic adjective, such as `anper` “wet” versus `nonper` “dry”. This is distinct from the separate clause-level particle, although the meanings are related.

## Questions

### Yes/no and basic questions

There is no obligatory question particle. Intonation normally distinguishes a question, but written examples use `?`. The ordinary question order is **OSV**:

```text
Muchi ti pazi?
Cats you like?
Do you like cats?
```

Examples with no overt object can still use the same general interrogative pattern, and adjuncts can be fronted:

```text
Zetay ti epi ieni?
Tomorrow you can come?
Can you come tomorrow?
```

The verb remains at the end in modal questions:

```text
Chet mi epi seysi?
Here I can sit?
May I sit here?
```

`vay` is a formal emphatic “really?” particle. `ella` is its informal counterpart. Tag questions can append informal `ella` to a declarative:

```text
Ti pazi muchi, ella?
You like cats, right?
```

### Interrogative words

Interrogative words generally occur at the front of a direct question.

| Andro | Meaning |
|---|---|
| `chyi` | whose |
| `koe` | how, in what way |
| `osor` | why |
| `so` | what |
| `somar` | where |
| `soter` | who |
| `voli` | when |
| `wodo` | which way, by what route |
| `yage` | where to |
| `yasu` | where from |
| `ali` | how much, how many |
| `chui` | which one |
| `vaja` | is it true that |

Examples:

```text
Yasu ti ieni?
Where-from do you come?

Koe ti seiti?
How do you feel?

So tyi vahuryiaisi fo ti famei?
What does your tattoo mean to you?
```

`chyi` also has a reflexive use, so its interpretation depends on whether it asks for a possessor or refers back to the subject.

## Pronouns and reference

Pronouns encode person, number, gender/formality, and in some forms animacy. The most important forms for syntax are:

| Function | Forms |
|---|---|
| 1SG | `mi`; possessive `myi` |
| 2SG | `ti`; possessive `tyi` |
| formal 2SG/3SG | `epie` non-feminine, `epia` feminine; possessive `epil` |
| 3SG unspecified gender | `egi`; possessive `il` |
| 3SG masculine/feminine | `egli` / `egla`; possessive `il` |
| 3SG inanimate | `che`; possessive `chyi` |
| 1PL inclusive | `noni`; possessive `niyi` |
| 1PL exclusive | `nodi`; possessive `nodyi` |
| 2PL | `toi`; possessive `tyoi` |
| 3PL animate | `egoi`; possessive `egyi` |
| 3PL inanimate | `chei`; possessive `chey` |

`egi` avoids specifying third-person gender. The formal pronouns `epie` and `epia` are used for strangers, unknown persons, or socially superior persons. The non-feminine formal form can also be generic.

Pronouns can be omitted when the context supplies the referent:

```text
Mi pazi muchi.
Pazi muchi.
I/you like cats.
```

### Reflexive reference

`chyi` can refer reflexively to the subject in an action directed back at that subject:

```text
Egi rek chyi da tasek.
He hit himself with a table.
```

Without enough context, the sentence may also be interpreted as “He hit the table.”

## Demonstratives and relative reference

Demonstratives distinguish animacy and, for inanimates, relative distance from speaker and listener:

| Form | Typical reference |
|---|---|
| `je` / `ja` | demonstrative for animate entities, non-feminine / feminine |
| `heje` | inanimate object close to both speaker and listener |
| `aje` | inanimate object closer to listener |
| `che` | inanimate object closer to speaker |
| `dite` | inanimate object far from both but visible |
| `niger` | distant or out-of-sight inanimate object, mainly southeastern dialect |

For humans, personal pronouns are usually preferred over `je` or `ja`. Demonstratives can also be emphatic, especially before a name or adjective:

```text
Je Kasstor!
That Kasstor!
```

Most demonstratives can serve as relative pronouns, except that `je` and `ja` are normally replaced by a third-person personal pronoun or omitted when referring to animate people. The generic inanimate relative pronoun is `chei` in relative use, written distinctly from the ordinary inanimate plural demonstrative in the source grammar.

## Verbs, tense, aspect, and voice

The verb has a basic present/infinitive form and a past form. Future, aspect, and most moods are expressed with particles.

### Tense and aspect

| Meaning | Form and position |
|---|---|
| Present | Basic verb form; normally also implies imperfective aspect |
| Future | Head-final particle `ze` before the verb phrase |
| Past | Conjugated verb form, commonly represented by a past suffix such as `-t` |
| Imperfective | Particle `vi`, before the verb |
| Perfective | Head-final particle `va`, before or adjacent to the verb phrase |

Present:

```text
Ti fesgai.
You read / are reading.
```

Future:

```text
Ti ze fesgai.
You will read / will be reading.
```

Past:

```text
Seja va hajit.
The sun shone.
```

Imperfective past:

```text
Ti vi fesgat.
You started reading and have not finished.
```

Perfective future:

```text
Ti ze va fesgai.
You will read and finish reading.
```

The present and future default to imperfective, and the past defaults to perfective. `vi` and `va` can still be added for contrast or emphasis. In some dialects `va` occurs with a present verb to emphasize completion at the moment.

### Passive

`ge` marks passive voice on the verb phrase:

```text
Sotak ge karlet chu polno sotak.
Someone was killed by someone else.
```

The agent may be expressed using the ordinary case-marking resources; context determines the precise role where marking is omitted.

## Modals and nominalization

The small set of auxiliary/modal verbs is:

- `epi`: may, be allowed/able to
- `pazi`: like, when used as an auxiliary
- `kiruki`: can, be able to
- `vipini`: make someone do something; also used for obligation in examples

A modal occupies the normal finite-verb position, while the lexical action verb moves to the end and remains uninflected:

```text
Mi kiruki feni.
I can swim.

Mi epi chet seysi.
I may sit here.
```

Tense, aspect, and operator marking attach to the modal/finite verb, not to the final lexical action verb:

```text
Mi vi kiruket feni, abe va tayet.
I knew how to swim, but I forgot.
```

With `pazi`, the action is normally expressed by a bare final verb rather than by nominalizer `na`:

```text
Pazi fesgai.
I like reading.
```

Nominalization uses `na`. It turns a verb or adjective into a noun-like expression referring to an action or activity. It may be suffixed (`-na`) or occur as a separate head-final particle:

```text
Egi dekit rekina.
He decided to attack.

Chiwi-na esi ozeyo.
Writing is difficult.

Chiwi na esi ozeyo.
Writing is difficult.
```

Nominalized actions can function as objects, subjects, or complements. Do not add `na` after the final lexical verb in the ordinary `pazi` modal construction.

## Imperatives and related moods

The plain imperative marker is `do`. It is always the final word of the sentence:

```text
Tori dejitos do!
Throw the weapons!
```

In a negative imperative, `no` precedes the lexical verb but `do` remains final:

```text
Tori no dejitos do!
Do not throw the weapons!
```

Other command, request, and wish markers:

| Marker | Meaning and use | Position |
|---|---|---|
| `te` | informal imperative equivalent of `do` | final |
| `hemi` | polite exhortative/request, roughly “please” | final |
| `ihemi` | strong plea/begging | final |
| `heme` | cohortative: speaker and listener should do it together, “let’s” | final |
| `vage` | hortative/light order or recommendation, often expecting the action | generally before predicate, as a head-final operator in the clause |
| `vige` | formal optative/wish, especially religious or ceremonial | before the desired predicate, head-final relative to its clause |

Examples:

```text
Ti vage eni.
You should go.

Eni heme!
Let's go!

Vige halloi nome yi Ori!
May God's name be praised!

Mudi mi fayse, hemi.
Please give me a drink.
```

`do` is a direct and potentially impolite order. `hemi` is normally preferred for politeness; `vage` is a deferential/light order from a higher-status speaker; `vige` expresses a formal wish rather than a normal command. In rare highly formal contexts, `epi` can serve as a powerful imperative marker.

## Subordination and conjunction

Subordinate clauses normally use **SOV** order. They are attached to a main clause by a subordinator or conjunction. Relevant subordinating particles include:

| Particle | Meaning |
|---|---|
| `voli` | when, until |
| `imin` | because |
| `abe` | but, whereas |
| `abejar` | however, but |
| `pama` | at that time |
| `per` | in order to |

Basic conjunctions include:

| Particle | Meaning |
|---|---|
| `e` | and |
| `yen` | or |
| `leyfe` | exclusive or |
| `zor` | exclusive or |

Examples:

```text
Mi eni o jan, per mi vibo vibi.
I go home in order to eat food.

Abejar voli koboviros karli, egyi natalji inrit.
However, when the soldiers were dying, they called to their mothers.
```

The verb of a subordinate clause may be omitted when the context makes it recoverable. A topic construction with `ya` can also create a subordinate-like SOV clause.

### Conditionals

The documented examples use `miam` for the conditional “if” clause and `vimi` for the resulting “then” clause:

```text
Miam ... vimi ...
If ..., then ...
```

`vimi` may be omitted when the subordinate-clause word order clearly identifies the conditional structure. The source syntax chapter presents this system mainly through examples and does not provide a complete normative description, so do not invent additional conditional morphology.

## Comparison and degree

Adjectives have basic, comparative, and superlative degrees. Comparative and superlative morphology is normally lexical/suffixal. A comparative phrase can be followed by `o` “than”:

```text
Zetay ze esi votepoe o hetay.
Tomorrow will be hotter than today.
```

A special archaic construction juxtaposes comparative and superlative forms to mean “more than the most”:

```text
gruwea gruweam
bigger than the biggest
```

The source syntax chapter lists additional comparison particles but does not define them in prose. Use the lexical entries and examples rather than assuming a complete general rule from the list alone.

## Information structure and ambiguity rules

When parsing or generating Andro:

1. Start with SVO for a declarative.
2. Move the object or interrogative constituent to the front for a direct question, yielding OSV.
3. Use SOV inside a subordinate or topic-like clause.
4. Treat noun modifiers as pre-nominal and verb modifiers as post-verbal.
5. Treat most case and aspect particles as optional unless emphasis or disambiguation requires them.
6. Keep `do`, `te`, `hemi`, `ihemi`, and `heme` at the end of their clause.
7. Use `no` after the verb in ordinary negation, but before the verb in a negative imperative.
8. Do not require an overt subject, copula, accusative, genitive, or dative when context and order make the interpretation clear.
9. Resolve ambiguous omitted pronouns, unmarked cases, and multifunctional particles from discourse context.
10. Remember that `chu` can be accusative, genitive, or another grammatical/emphatic particle; its role is contextual.
11. Remember that `a` can be comitative or a dialectal locative.
12. Do not treat dialectal variants, older formal constructions, or zero copulas as ungrammatical automatically.

## Scope limitations

The syntax source contains several headings whose detailed rules are unfinished or commented out, especially parts of comparatives, diminutives, honorific syntax, and conditional constructions. This summary records only the rules and examples actually supported by the text. Pronunciation, phonotactics, and orthographic interpretation are intentionally excluded.
