# SAPIR Quote Verifier — pilot 0.1 (2026-09-27)

Question it answers: **"Did this author really write this, and where exactly?"** — for texts from several cultures, with the same honest statuses as the gematria engine.

## Statuses
- **FOUND_EXACT** — the exact wording occurs; every location is listed (work, place, text, licence, source link).
- **FOUND_CLOSE** — wording ≥ 85% similar (different edition or translation); the closest real text is shown.
- **NOT_FOUND** — not in this corpus in this wording. This is a statement about the corpus, not about the world; the corpus size is always reported.
- Attribution: **MATCHES_CLAIM** (found in the claimed author's own work) or **DIFFERENT_SOURCE** (the words exist, but in someone else's text).
Every answer carries a SHA-256 record.

## Pilot corpus (all openly licensed)
| corpus | languages | works | licence |
|---|---|---|---|
| gutenberg | en | 408 | US public domain (Project Gutenberg, via GITenberg mirror) |
| perseus | en | 34 | CC BY-SA 4.0 (Perseus Digital Library) |
| perseus | grc | 32 | CC BY-SA 4.0 (Perseus Digital Library) |
| wlc | he | 40 | CC BY 4.0 (WLC/OSHB) |

1,132,254 passages. Includes: Hebrew Bible (Hebrew, 39 books), New Testament and Plato's Republic (Greek + English), ~410 classics in English: KJV Bible, Plato, Aristotle, Marcus Aurelius, Epictetus, Seneca, Confucius, Tao Te Ching, Dhammapada, Bhagavad Gita, the Koran (three translations), Dante, Cervantes, Shakespeare, Montaigne, Pascal, Voltaire, Goethe, Tolstoy, Dickens, Darwin, Marx, Nietzsche, Paine, Lincoln, Emerson and others.

## First test: 34 famous quotes, genuine and misattributed
Agreement with expected answer: **28 / 34**.

| ✓/✗ | status | attribution | expected genuine | quote | claimed |
|---|---|---|---|---|---|
| ✓ | FOUND_EXACT | MATCHES_CLAIM | True | It is a truth universally acknowledged, that a single man in | Jane Austen |
| ✓ | FOUND_EXACT | MATCHES_CLAIM | True | Call me Ishmael | Herman Melville |
| ✓ | FOUND_EXACT | MATCHES_CLAIM | True | It was the best of times, it was the worst of times | Charles Dickens |
| ✓ | FOUND_EXACT | MATCHES_CLAIM | True | The mass of men lead lives of quiet desperation | Henry David Thoreau |
| ✗ | NOT_FOUND | - | True | It is better to be feared than loved, if you cannot be both | Machiavelli |
| ✓ | FOUND_CLOSE | MATCHES_CLAIM | True | All happy families are alike; each unhappy family is unhappy | Tolstoy |
| ✓ | FOUND_EXACT | MATCHES_CLAIM | True | We hold these truths to be self-evident, that all men are cr | Jefferson |
| ✓ | FOUND_EXACT | MATCHES_CLAIM | True | In the beginning God created the heaven and the earth | Bible |
| ✓ | FOUND_EXACT | MATCHES_CLAIM | True | The unexamined life is not worth living | Plato |
| ✓ | FOUND_CLOSE | MATCHES_CLAIM | True | Workingmen of all countries unite | Marx |
| ✗ | FOUND_EXACT | DIFFERENT_SOURCE | True | These are the times that try men's souls | Thomas Paine |
| ✓ | FOUND_CLOSE | DIFFERENT_SOURCE | False | Lasciate ogne speranza, voi ch'intrate | Dante |
| ✗ | NOT_FOUND | - | True | Abandon all hope, ye who enter here | Dante |
| ✓ | FOUND_EXACT | MATCHES_CLAIM | True | God is dead | Nietzsche |
| ✓ | FOUND_CLOSE | MATCHES_CLAIM | True | The heart has its reasons which reason knows nothing of | Pascal |
| ✗ | NOT_FOUND | - | True | The supreme art of war is to subdue the enemy without fighti | Sun Tzu |
| ✓ | NOT_FOUND | - | False | Be the change you wish to see in the world | Gandhi |
| ✓ | NOT_FOUND | - | False | Insanity is doing the same thing over and over again and exp | Einstein |
| ✓ | NOT_FOUND | - | False | The only thing necessary for the triumph of evil is for good | Edmund Burke |
| ✓ | NOT_FOUND | - | False | Well-behaved women seldom make history | Shakespeare |
| ✓ | FOUND_CLOSE | DIFFERENT_SOURCE | False | A journey of a thousand miles begins with a single step | Lao Tzu |
| ✓ | NOT_FOUND | - | False | Let them eat cake | Marie Antoinette |
| ✓ | FOUND_EXACT | DIFFERENT_SOURCE | False | Elementary, my dear Watson | Arthur Conan Doyle |
| ✓ | NOT_FOUND | - | False | Play it again, Sam | Casablanca |
| ✗ | FOUND_EXACT | MATCHES_CLAIM | False | Money is the root of all evil | Bible |
| ✓ | FOUND_EXACT | MATCHES_CLAIM | True | The love of money is the root of all evil | Bible |
| ✓ | FOUND_EXACT | MATCHES_CLAIM | True | Pride goeth before destruction, and an haughty spirit before | Bible |
| ✓ | FOUND_EXACT | DIFFERENT_SOURCE | False | Cleanliness is next to godliness | Bible |
| ✓ | FOUND_CLOSE | DIFFERENT_SOURCE | False | God helps those who help themselves | Bible |
| ✓ | FOUND_EXACT | MATCHES_CLAIM | True | To thine own self be true | Shakespeare |
| ✓ | FOUND_EXACT | MATCHES_CLAIM | True | Survival of the fittest | Charles Darwin |
| ✓ | NOT_FOUND | - | False | Religion is the opium of the people | Marx |
| ✓ | FOUND_EXACT | DIFFERENT_SOURCE | False | I think, therefore I am | Aristotle |
| ✗ | FOUND_EXACT | DIFFERENT_SOURCE | True | Know thyself | Plato |

### What the 6 disagreements teach
1. **Translations** (Machiavelli, Dante, Sun Tzu): the popular wording comes from a modern translation; the old public-domain translation says it differently. The tool correctly says "not in this wording" — but the product must match across translations. Next step: cross-translation matching.
2. **Corpus gaps** (Paine's *The Crisis*): the text is not yet in the pilot. Solved by scale.
3. **Misquote inside a real quote** ("Money is the root of all evil" vs KJV "the *love of* money is the root of all evil"): the substring exists, so a naive match says "found". Next step: flag when the claimed quote drops words that change meaning.
4. **Very short quotes** ("Know thyself"): too common to attribute from text alone.

## Sources considered, licences, access
| source | content | licence | status |
|---|---|---|---|
| Project Gutenberg | ~75,000 books | US public domain | 410 in pilot; full set needs gutenberg.org in network allowlist |
| Perseus (GitHub) | Greek & Latin + translations | CC BY-SA 4.0 | in pilot (partial) |
| OSHB / WLC | Hebrew Bible | CC BY 4.0 | in pilot |
| Sefaria export | Talmud, Mishnah, Midrash, commentators | per text: CC0 / CC BY / PD, some CC BY-NC | blocked here (storage.googleapis.com) — needs allowlist |
| Wikisource (all languages) | millions of pages | CC BY-SA | needs allowlist |
| Tanzil | Qur'an Arabic text | verbatim-only licence | possible, text must not be altered |
| GRETIL | Sanskrit | research use, varies | needs checking per text |
| ctext.org | Chinese classics | API with limits, no bulk | partnership needed |

## Reproduce
`qv_build.py` downloads nothing itself: fetch the books listed in `qv_books.json` from the GITenberg mirror, WLC from OSHB, Perseus from GitHub, then `python3 qv_build.py` → SQLite FTS5 index; `python3 qv_verify.py "quote" "author"`.
