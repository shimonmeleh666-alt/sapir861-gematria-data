# Amendment 1 to the pre-registered blind test

Date: 2026-10-02. The original protocol (`PREREG_BLIND_TEST.md`, SHA-256
`0dc7b1bcb59285113bd71f05636e1f0daf7a6a60bef651cb86a2e378c7071c12`) is unchanged
and stays in this repository byte for byte. This amendment replaces one thing: the
held-out set.

## What was wrong

In 861-Bench 2.0 the 1,000 held-out items were drawn with the same public seed
(861) as the public items, by a generator published in this repository. Anyone
could run `gen.py` and obtain the held-out file. Its hash matched the pre-published
one, so the set was fixed in advance — but it was not secret. A held-out set that
can be regenerated from public code does not test anything a public set does not.

We found this ourselves on 2026-10-02 while auditing the repository.
No result on the 2.0 held-out set has been published.

## What changes

- The 2.0 held-out split is retired and published as `bench2_dev_v20.jsonl`
  (SHA-256 `d403e0541949e339d79d174fb08e21f2c52b20cabfdcdb58e5ca1cef5aee448c`,
  the hash announced earlier). It may be used as a development set.
- A new held-out set of 1,000 items (861-Bench 2.1) was drawn with a secret seed
  that is not in this repository and has not been published anywhere.
  SHA-256 of the file: `f5d43745d5853ea7291d0e06f92b54ff1426c59d0f7975275b037a590beb0aa8`.
- Composition: 400 arith_false, 280 true_unattested, 180 retrieval, 90 kollel,
  50 refusal. No item text repeats a public or a retired item.
- The category `attested_unconf` is not in the new held-out set: all 1,013 such
  pairs come from the public attested index and cannot be withheld. Metrics for
  that category are reported on the public split only and are labelled as such.
- The public split `bench2_public.jsonl` is byte-identical to 2.0.

Everything else in the protocol — question, conditions, metrics, statistical test,
success and failure criteria, independence rules — stands as registered.
