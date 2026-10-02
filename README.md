# SAPIR 861 — open gematria datasets

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22848827.svg)](https://doi.org/10.5281/zenodo.22848827)

**EN** · Open data and code behind [sapir861.com](https://sapir861.com): word-sum coverage of the Pentateuch against null models, and 8,629 attested gematria equalities from classical sources. Every number is reproducible from public texts.
**RU** · Открытые данные и код проекта [sapir861.com](https://sapir861.com): гематрия Пятикнижия против случайных моделей и 8 629 равенств из классических источников. Каждое число можно пересчитать.
**HE** · נתונים וקוד פתוחים של [sapir861.com](https://sapir861.com): גימטריה בחומש מול מודלים אקראיים ו-8,629 שוויונות מתועדים ממקורות קלאסיים.

- Try it on your name: https://sapir861.com/hebrew-name
- API: https://sapir861.com/openapi.json · For AI agents: https://sapir861.com/llms.txt
- Archived version with DOI: https://doi.org/10.5281/zenodo.22848827

## Reproduce everything (one command)

```
python3 reproduce.py          # or: docker build -t sapir861 . && docker run --rm sapir861
```
Downloads the pinned WLC/OSHB text (SHA-256 in `MANIFEST.json`) and re-derives every control number. Standard library only. Current result: **ALL CHECKS PASSED**.

| check | result |
|---|---|
| Torah consonants, WLC (ketiv) | 304,850 |
| Torah verses | 5,853 |
| 861 × 354 grid | 304,794 |
| **861×354 reconciliation** | **354 / 354 pages** — sum of pages = 304,850 = grid + 56; 56 = page 1 (+11) + 45 spelling differences WLC vs edition (47 pages +1, 2 pages −1); edition total 304,805 |
| attested equalities | 8,629 = 6,494 exact + 2,135 kollel |
| example pairs re-added letter by letter | 1,015 pass; 8 extraction errors (number words, not equalities) marked `example_withdrawn` in v05 |

## 861-Bench 2.1 and the pre-registered blind test

- `bench2_public.jsonl` — 6,879 public items (arithmetic, kollel, true-but-unattested, attested-unconfirmed, retrieval, refusal); `bench2_manifest.json` has counts and hashes.
- 1,000 held-out items (861-Bench 2.1) are **not published**; they were drawn with a secret seed that is not in this repository. SHA-256 of the file: `f5d43745d5853ea7291d0e06f92b54ff1426c59d0f7975275b037a590beb0aa8`.
- `bench2_dev_v20.jsonl` — the retired 2.0 held-out split (1,000 items, SHA-256 `d403e0541949e339d79d174fb08e21f2c52b20cabfdcdb58e5ca1cef5aee448c`). It could be regenerated from the public generator, so it is now published as a development set. See `PREREG_AMENDMENT_1.md` (SHA-256 `9bc9702e21f5abd9c67673d22662a4cf2b2ff20afe09ea632a3672e76e0e13dc`).
- `gen.py` regenerates the public and development files (seed 861, run `reproduce.py` first to fetch the corpus); the held-out file needs the secret seed and cannot be regenerated from this repository. `score.py` scores any model's answers.
- `PREREG_BLIND_TEST.md` — protocol fixed before any run: question, conditions, six metrics, McNemar with Bonferroni, success and failure criteria, independence rules. SHA-256 `0dc7b1bcb59285113bd71f05636e1f0daf7a6a60bef651cb86a2e378c7071c12`. A negative result is published in full.

## Status labels
Every answer on sapir861.com and in `/api/provenance` carries a status: **COMPUTED** (letter arithmetic, deterministic), **UNCONFIRMED** (machine-extracted attestation, not yet checked against the printed page), **NOT FOUND** (no record among 8,629), **CONFIRMED** (reserved for records verified against the printed page). Example: 861 — COMPUTED; its two attestations (Bnei Yissaschar) are UNCONFIRMED.

## Versions
`MANIFEST.json` pins three things separately: **engine** (site code version), **data** (dataset release), **corpus** (WLC 4.20 via OSHB, file hashes).

## Licences
Code and computed tables: CC BY 4.0. `sapir861_attested_gematria_v05.csv` is derived from Hebrew Wikisource and is therefore **CC BY-SA 4.0**.

## Files
| file | what |
|---|---|
| `sapir861_attested_gematria_v05.csv` | attested equalities from classical texts (v05: comment row removed, 8 examples withdrawn) |
| `pages_861x354.csv` | letters per page for all 354 pages (WLC) and the difference from 861 |
| `reproduce.py`, `MANIFEST.json`, `Dockerfile`, `Makefile` | one-command reproduction |
| `sapir861_coincidence_1500.csv`, `coverage_vs_null_1500.csv`, `nullmodel_results.json` | coverage of values 1–1500 vs null models |
| `sapir861_861_computed_v01.csv` | computed facts about the number 861 |
| `oshb.py`, `cover.py`, `nullmodel.py` | code that produces the tables (text: OSHB / WLC) |
| `METHODS.md` | method in detail |

Please cite via `CITATION.cff`.

---

# Coincidence is cheap: word-sum coverage of the Pentateuch against null models, and 8,629 classical gematria attestations

Author: Nugzari Pichkhadze — SAPIR 861 (sapir861.com). Licence: CC BY 4.0.
Version 2.0, 2026-09-19.

Two datasets and the code that produces them. Everything is computed from a
public text under a public licence; nothing depends on a private database.

## The finding

For every value 1–1500 we count in how many of the 54 weekly Torah portions
some word has that letter-sum. 867 of the first 1000 values have at least one
content word somewhere in the Pentateuch.

That number on its own means nothing, so we measured what a text carrying no
message at all would give. Three surrogate models — a corpus-wide letter
permutation, a first-order Markov regeneration of every word, and a reshuffling
of real words across portions — 1000 replicates for the first and third, 300 for
the second.

**A random text covers more values than the Pentateuch does.**

| values 1–1000, strict rule | coverage |
|---|---|
| Pentateuch (observed) | **867** |
| M1 letter permutation | 946.9 ± 4.9 (z = −16.4) |
| M2 Markov surrogate | 938.1 ± 5.1 (z = −14.0) |

Not one replicate of either model fell to the observed level. The same holds
under the loose rule (observed 937 against 979.2 ± 3.4 and 978.6 ± 3.7), for the
range 1–1500, and for the number of values present in all 54 portions
(observed 6, against 20.6, 24.1 and 31.6).

The reason is ordinary: real language repeats itself, so a few thousand lemmas
carrying eighty thousand word forms produce fewer distinct sums than a random
letter stream of the same size. Coverage is therefore not evidence of design —
it is below what chance alone delivers.

The consequence is the point of this record. Any claim of the form *"the value X
occurs in the text, therefore …"* rests on an event that is the normal case and
is **cheaper in a random text than in this one**. Without a null model such a
claim carries no information. `coverage_vs_null_1500.csv` supplies that null
model for every single value, so any specific claim can be checked rather than
argued about.

## Files

| file | what it is |
|---|---|
| `sapir861_coincidence_1500.csv` | values 1–1500 × portions containing a word with that sum (strict, loose) |
| `coverage_vs_null_1500.csv` | the same values against their own null distribution: mean, sd, z, empirical p |
| `nullmodel_results.json` | summary of all three models under both rules |
| `sapir861_attested_gematria_v03.csv` | 8,629 gematria equalities asserted in 834 classical works |
| `METHODS.md` | full methodology, definitions, corrections, limits |
| `sapir861_code.zip` | the code: parser, coverage, null models, per-value tables |

## Counting rules

Mispar hechrachi (alef 1 … tav 400, final letters as ordinary). Vowel points and
cantillation stripped.

* **strict** — only morphemes tagged noun, verb or adjective; prefixes dropped.
  59,633 forms.
* **loose** — the whole word form as written, any part of speech. 80,052 forms.

## The second dataset

8,629 gematria equalities actually asserted in classical works, rebuilt from the
Hebrew Wikisource with our own code and recomputed by machine: 1,023 values,
834 works. **6,494 (75.3 %) hold exactly; 2,135 (24.7 %) require *im hakolel*,
the ±1 allowance.** The most kolel-dependent value is 110, where 90 of 106
attestations (85 %) need it.

This records what authors wrote. It is not a claim that any equality is correct.

## About 861

Under the strict rule the value 861 has no content word anywhere in the
Pentateuch. The null models put that at z = −1.97, with an empty result in 4.3 %
(M1) and 1.0 % (M2) of replicates. It is mildly unusual and nothing more — one
value out of 1500, where a comparable number would look this way by chance.
We state it with its p-value attached rather than as a finding. Under the loose
rule 861 appears in 12 portions against an expected 11.5 ± 3.2: entirely ordinary.

## Correction to our earlier figures

An earlier build of ours truncated Exodus 20 at verse 23 and lost three verses.
Twenty-one of the 1500 rows were one portion too low. The files here are the
corrected ones; no headline figure changed.

## Reproducing

```
pip install numpy
# add Gen.xml Exod.xml Lev.xml Num.xml Deut.xml from openscriptures/morphhb
python3 oshb.py && python3 cover.py
python3 nullmodel.py 1000 300
python3 pervalue.py 300
```

## Sources

Text and morphology: Open Scriptures Hebrew Bible, Westminster Leningrad Codex,
CC BY 4.0 — https://github.com/openscriptures/morphhb
Attestations: Hebrew Wikisource, CC BY-SA 4.0.
The 861 × 354 structure: Binyamin Pichkhadze, "Chumash 354" (חומש 354),
Bnei Brak, 2002 / התשס״ג.

Method pages: https://sapir861.com/research/coincidence · https://sapir861.com/research/kolel
