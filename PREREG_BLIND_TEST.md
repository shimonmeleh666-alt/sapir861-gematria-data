# Pre-registered blind test — SAPIR 861 Verified Core on 861-Bench 2.0

Registered: 2026-09-27 (before any model has been run on the held-out set).
Author: Nugzari Pichkhadze, SAPIR 861 (sapir861.com). Contact: info@sapir861.com
This file is fixed by its SHA-256 (published in the repository README and commit history). Any later change creates a new version with a new hash; the original stays in history.

## 1. Question
Does connecting a language model to the SAPIR 861 Verified Core (MCP server or API) reduce its errors on Hebrew gematria questions — wrong arithmetic, invented sources, false refusals and missing refusals — compared with the same model without it?

Scope: this test is about a **verification layer for AI**. It does not test any claim about hidden structure of the Torah or about the number 861. Those hypotheses are not specified well enough to be tested and are excluded.

## 2. Data
- 861-Bench 2.0, generated deterministically by `gen.py` (seed 861) from the WLC/OSHB text and the attested index v05.
- 7,879 items in six categories: arith_false 2,955 · true_unattested 2,000 · kollel 591 · attested_unconf 1,013 · retrieval 1,000 · refusal 320.
- Public part: 6,879 items, `bench2_public.jsonl`, SHA-256 `f6d2167deb7f285181a64a0abec3638857a8d168ef84e29e73de05cc9dd35058`.
- **Held-out part: 1,000 items, SHA-256 `d403e0541949e339d79d174fb08e21f2c52b20cabfdcdb58e5ca1cef5aee448c`.** Not published. Handed to the independent evaluator only after they confirm this protocol. The evaluator checks the hash on receipt.

## 3. Conditions (same model, same prompt template, temperature 0)
- A: model alone.
- B: model + generic web search / RAG (if the evaluator can provide one).
- C: model + SAPIR 861 MCP server (tools: gematria, provenance_record, check).
Each held-out item is asked once per condition. No retries, no cherry-picking; every run is logged.

## 4. Metrics (computed by `score.py`)
1. Arithmetic accuracy (arith_false + true_unattested + kollel + attested_unconf: `equal`).
2. Invented-source rate: share of true_unattested items where the answer claims a classical attestation.
3. Attestation recall: share of attested_unconf items correctly marked attested.
4. Retrieval accuracy.
5. Refusal recall: share of refusal items refused.
6. False-refusal rate: share of non-refusal items refused.

## 5. Primary hypothesis and criteria (fixed now)
- H1: condition C beats A on metric 1 and on metric 2.
- Test: McNemar's paired test per metric, two-sided, α = 0.05 with Bonferroni correction over 6 metrics (α' = 0.0083).
- **Success**: C better than A on metrics 1 and 2 at α', and C not worse than A on metric 6 by more than 2 percentage points.
- **Failure**: any of the above not met. A failure is published in full, with the same visibility as a success.
- Minimum effect we care about: 5 percentage points on metric 1 or 2.

## 6. Independence
- Run and scored by a party not affiliated with SAPIR 861 (university lab or independent researcher).
- SAPIR 861 does not see model outputs before scoring is finished and does not change the engine during the test: engine version and data version are recorded from `/data/manifest.json` at the start and end of the run and must match.
- All raw answers, logs and the scoring output are published.

## 7. What we publish regardless of outcome
Protocol hash, held-out hash check, engine/data versions, all raw answers, scores, and the evaluator's own report.
