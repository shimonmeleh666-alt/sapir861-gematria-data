# Methods

Everything below can be re-run from the code in `sapir861_code.zip`. Nothing here depends on
any private database of ours: the input is a public text under a public licence,
and the output files in this record are what the code prints.

## 1. Source text

Open Scriptures Hebrew Bible (OSHB, `openscriptures/morphhb`), the Westminster
Leningrad Codex with morphological tagging, CC BY 4.0. We use the five books of
the Pentateuch: `Gen.xml`, `Exod.xml`, `Lev.xml`, `Num.xml`, `Deut.xml`.

Parsing gives **80,052 word forms in 5,853 verses**. (The verse count follows the
BHS/WLC chapter division, which differs from the traditional one in Exodus 20 and
Deuteronomy 5; the words are the same words.)

## 2. Letter values

Mispar hechrachi: alef 1 … tet 9, yod 10 … tsadi 90, qof 100 … tav 400.
Final letters take the value of the ordinary form. Vowel points and cantillation
marks are stripped; maqaf, geresh, gershayim and quotation marks are removed.
No other transformation is applied.

## 3. Two counting rules

* **strict** — only the morphemes OSHB tags as noun, verb or adjective
  (`N*`, `V*`, `A*`). Attached prefixes (conjunction, article, preposition,
  relative) are dropped, so what is summed is the content word.
  This yields **59,633 forms**.
* **loose** — the whole word form exactly as written, any part of speech.
  This yields **80,052 forms**.

strict is the harder rule and the one we report first. Anyone who wants a larger
number can use loose; both are in every table.

## 4. Portions

The 54 weekly portions of the ordinary annual cycle, given as 54 starting points
(book, chapter, verse) in `code/parasha_starts.json`. A word belongs to the
portion whose start is the last one at or before its verse.

## 5. Coverage

For every value 1–1500 we record in how many of the 54 portions at least one word
has that letter-sum. Output: `sapir861_coincidence_1500.csv`
(`value, portions_strict, portions_loose`).

Headline figures, strict / loose:

| range | at least one word (strict) | (loose) |
|---|---|---|
| 1–861 | 805 | 848 |
| 1–1000 | 867 | 937 |
| 1–1500 | 921 | 1024 |

Six values occur in **all 54** portions under the strict rule: 26, 50, 56, 62,
140, 311. Eighteen do so under the loose rule.

**861 has no content word at all under the strict rule.** Under the loose rule it
appears in 12 portions.

### Correction against our earlier figures

An earlier build of ours truncated Exodus 20 at verse 23 and so lost three
verses. Twenty-one of the 1500 rows were one portion too low. The corrected file
is the one in this record. None of the headline figures above changed.

## 6. Null models — the point of this record

A coverage figure alone says nothing. The question is what a text that carries no
message at all would produce. We therefore generate surrogate corpora and measure
the same quantities on them. Three models, increasingly faithful to Hebrew:

* **M1 — letter bag.** All consonants of the Pentateuch are permuted across the
  whole corpus. Word lengths, word order and portion boundaries are kept; letter
  frequencies are kept; every lexical fact is destroyed.
* **M2 — Markov surrogate.** Each word is regenerated letter by letter from a
  first-order Markov chain fitted on the Pentateuch itself, at its own length and
  in its own place. Local letter dependence — which is what actually shapes the
  distribution of sums — is preserved; the vocabulary is destroyed.
* **M3 — portion shuffle.** The real words are kept and reassigned to portions at
  random, portion sizes preserved. This tests the distribution across portions
  rather than the vocabulary; total coverage is unchanged by construction.

1000 replicates for M1 and M3, 300 for M2 (its per-replicate cost is an order of
magnitude higher, and with sd ≈ 3.5 the standard error of the mean is ≈ 0.2 —
far below the effect measured). Seed 861; the per-value tables use seed 354.
Reported as mean,
standard deviation, z of the observed value, and the empirical fraction of
replicates in which the surrogate reached or exceeded the observed value.

## 7. What the null models show

The finding runs against the direction gematria enthusiasm would predict, and
that is exactly why it is worth publishing:

**A random text covers more values than the Pentateuch does.**

Strict rule, values 1–1000: observed 867; M1 gives 946.9 ± 4.9 (z = −16.4),
M2 gives 938.1 ± 5.1 (z = −14.0). In none of the replicates of either model did
the surrogate fall to the observed level. Loose rule, 1–1000: observed 937
against 979.2 ± 3.4 (z = −12.3) and 978.6 ± 3.7 (z = −11.3). The same holds for
1–1500 and for the count of values present in all 54 portions (observed 6 strict;
M1 20.6 ± 3.5, M2 24.1 ± 3.4, M3 31.6 ± 2.9).

The reason is not mysterious. Real language repeats itself: a few thousand lemmas
carry eighty thousand word forms, so the distinct sums are fewer than a random
letter stream of the same size would give. Coverage is therefore not evidence of
design — it is below what chance alone delivers.

Consequence for any claim of the form *"the value X appears in the text, therefore
…"*: appearing is the normal case and is cheaper in a random text than in this
one. A claim needs a null model to mean anything.

## 8. The value 861

Under the strict rule 861 has no content word. The per-value null gives an
expected 3.85 ± 1.96 portions, so the observed zero sits at z = −1.97; an empty
result occurs in 4.3 % of M1 replicates and 1.0 % of M2 replicates. The absence
is mildly unusual and nothing more — one value out of 1500, where a comparable
number would look this way by chance alone. Under the loose rule 861 appears in
12 portions against an expected 11.5 ± 3.2: entirely ordinary. We state this with
its p-value attached, not as a finding.

`coverage_vs_null_1500.csv` gives every value its own null distribution, so any
claim about any number can be checked the same way, instead of only the summary.

## 9. The second dataset

`sapir861_attested_gematria_v03.csv` is a different kind of object: 8,629
gematria equalities actually asserted in classical works, rebuilt from the Hebrew
Wikisource (CC BY-SA 4.0) with our own code and recomputed by machine.
6,494 (75.3 %) hold exactly; 2,135 (24.7 %) need *im hakolel* (±1). 1,023 values,
834 works. The most kolel-dependent value is 110: 90 of its 106 attestations
(85 %) need the ±1.

This is a record of what authors wrote, not a claim that any of it is correct.

## 10. What is not here

* No comparison against other Hebrew corpora (Prophets, Writings, Mishnah).
* No second-order or morphology-aware surrogate beyond M2.
* The attestation dataset has not been re-derived by an independent party.
* We make no claim about the meaning of any equality, and no claim about any
  person. The datasets are descriptive.

## 11. Reproducing

```
pip install numpy
# put Gen.xml Exod.xml Lev.xml Num.xml Deut.xml from openscriptures/morphhb here
python3 oshb.py            # -> torah_words.json
python3 cover.py           # -> coverage_recomputed.csv
python3 nullmodel.py 1000 300    # -> nullmodel_results.json
python3 pervalue.py 300          # -> coverage_vs_null_1500.csv
```

## Attribution

Text and morphology: Open Scriptures Hebrew Bible, Westminster Leningrad Codex,
CC BY 4.0 — https://github.com/openscriptures/morphhb

Attestations: Hebrew Wikisource, CC BY-SA 4.0.

The 861 × 354 structure: Binyamin Pichkhadze, "Chumash 354" (חומש 354),
Bnei Brak, 2002 / התשס״ג.

## Verification against printed leaves (added in v04, 2026-09-24)

Machine extraction from digital texts produces a specific kind of false record,
and v04 names it: **"split at be-gematria"**. The extractor cut a sentence at the
word בגימטריא and treated the words on either side as the two members of an
equality. Where the two fragments happen to differ by one, the row was accepted
as a *kollel* record — a difference of one is admissible in the tradition, so the
arithmetic check did not catch it.

The protocol that catches it is manual and is applied source by source:

1. Obtain a scan of a printed edition, preferably the first, with rights that
   permit use.
2. Locate the leaf: work, maamar/section, page.
3. Read the sentence whole, not the fragment the extractor returned.
4. Recount the letters by hand.
5. Record the result in the table with `verification` = `ok`, `unverified` or
   `withdrawn`, and a note naming the edition and the leaf.

The first source passed through this protocol was Sefer Karnayim (Żółkiew 1709,
National Library of Israel, public domain). The result was negative: the single
attestation for 862 was withdrawn. Negative results are published in the same
place and with the same weight as positive ones.
