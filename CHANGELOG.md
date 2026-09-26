# Changelog

## v04 — 2026-09-24

**Data correction, found by checking a printed leaf.**

Two rows of the attestation table are now flagged. Nothing was deleted: two new
columns were added instead, `verification` and `verification_note`, so every row
keeps its original values and the reader sees what was checked.

| value | status | why |
|---|---|---|
| 861 | `unverified` | In the available text of Bnei Yissaschar (Kislev–Tevet, maamar 3, section 4) the phrase *keren ha-shor* and the mention of *Matityahu* both occur, but there is no explicit gematria equality between them and the number 861 (תתס״א) does not appear. Pending a check against a printed leaf. |
| 862 | `withdrawn` | Checked against the printed first edition — Sefer Karnayim, Żółkiew (Zolkiew) 1709, National Library of Israel, maamar 11, *Dan Yadin* commentary, pp. 32–33 of the NLI file. The two expressions belong to **one sentence**; the gematria discussed there is סע״ף = 210. No equality yielding 862 exists on that leaf. |

**Failure class now named: "split at be-gematria".** The extraction pipeline cut a
sentence at the word בגימטריא and treated what stood on either side as the two
members of an equality. When the two fragments happen to differ by one
(«ג אותיות אלו» = 863, «מורה על יציאת» = 862) the row was accepted as a
*kollel* record. Both flagged rows above are instances of this class. A check that
rejects such splits is being added to the pipeline; the whole table will be
re-screened for it and a further version issued if more rows are affected.

**New file: `sapir861_861_computed_v01.csv`** — computations over WLC/OSHB
consonants, done by our own code:

- exactly one verse in the whole Tanakh has a consonant sum of 861 — Psalms 119:91;
- the distribution of the 54 words summing to 861 across books (Exodus 15, Ezekiel 8, Numbers 6, Deuteronomy 5, …);
- the ±1 band: 860 → 354 words, 861 → 54, 862 → 39;
- words whose sum equals a divisor of 861 (3, 7, 21, 41, 123, 287);
- corpus control totals: 306,785 word tokens, 23,213 verses.

## v03 — 2026-09-19

First public deposit: attestation table (1,023 values), coincidence table,
null-model results, methods.
