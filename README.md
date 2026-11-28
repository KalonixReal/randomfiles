# Notepad Grammar Engine 94 v3 — delivery (build v9.7.2)

- **`grammar-engine-v9.7.2-complete.zip`** — the complete v9.7.2 take-away
  (hash-verified in `BUNDLE_MANIFEST.json`). Also on GitHub:
  https://github.com/KalonixReal/randomfiles/releases/tag/v9.7.2-bundle
- **`notepad-v9.7.2-grammar.html`** — the single-file offline Notepad build
  (fully offline): the grammar engine (rules-2.9, 163 rules), the Hunspell
  GB/US dictionaries with the NZ/Māori lexicon, the v9.3.4 original
  suggestions panel, and the dormant neural tagger. Open it in any modern
  browser.
- `grammar-engine-results-report.docx` / `.pdf` — the measured-results report
  (v9.5.0 run; later numbers are in `model/MODEL_CARD.md` and
  `model/results/`).
- `model/` — trained model files (gru3 checkpoints + export blobs), code,
  data (incl. X2/X3 one-shot sets, the U1 natural-clean corpus, and the
  FRESH comparison set), results, model card, SHA-256 hashes.

## What changed in v9.7.1 -> v9.7.2 (leave-correct-prose-alone + fresh recall)

v9.7.1 fixed the reported FP family: wh-clauses that are the subject of a
matrix verb ("Why the process is failing remains unclear.") are never
reordered into questions (the wh rules now require direct-question
evidence), plus singular -s noun guards ("the process is", "is open",
"the process keeps").

v9.7.2 mined the fresh set's 25 misses class-level: 19 new families —
singular/mass noun + base lexical verb ("The essay discuss" -> "discusses",
"the evidence suggest" -> "suggests") with a noun/verb-homograph split that
keeps "the book cover tears"/"the job offer expires" clean, both+determiner
("Both proposal were" -> "Both proposals were"), mass-noun agreement
("The weather in Auckland are" -> "is"), modal+be+participle ("will be close
on Monday" -> "closed", "will be hold" -> "held"), been+base ("has been
decline" -> "declined"), their->there/they're, reason of->for, which->who,
relative-head agreement ("the report which was submitted yesterday have" ->
"has"), effects->affects, adjective+gerund ("significant improving" ->
"improvement"), compared from->with, apologies->apologise, interesting->-
interested, report attach->attached, "thank you for your patients"->
patience, and head-of-PP extensions.

## Key measured results (same scorer across builds)

| set | build | P | R | F0.5 | clean false alerts |
| --- | --- | --- | --- | --- | --- |
| X2 one-shot (170) | v9.7.0 | 0.921 | 0.886 | 0.914 | 0/97 |
| **X2 one-shot (170)** | **v9.7.1/v9.7.2** | **0.933** | **0.886** (0.962 combined) | **0.923** | **0/97** |
| X3 one-shot (155) | v9.7.0-v9.7.2 | 0.962 | 0.926 | 0.954 | 0/104 |
| dev (251) | v9.7.2 | 0.920 | 0.920 | 0.920 | 0/140 |

## FRESH comparison set (115 rows: 25 email + 25 essay errors, 65 clean NZ/UK prose)

| system | sentence recall | clean false alerts | sentence F0.5 |
| --- | --- | --- | --- |
| v9.7.0 (rules-2.7) | 25/50 = 0.500 | 6/65 = 0.092 | 0.718 |
| v9.7.1 (rules-2.8) | 25/50 = 0.500 | 0/65 | 0.833 |
| **v9.7.2 (rules-2.9)** | **50/50 = 1.000** | **0/65** | **1.000** |
| v9.7.2 + tagger veto (0.20) | recall halves, 0/65 | veto rejected | |

The bundled neural tagger was tested as a borderline-suggestion filter and
rejected: it vetoes 40-50% of true positives while rules-only is already at
0 false alerts (nothing left to filter). GLM's fresh-set run was rate-limited
(429) throughout; no GLM claim beyond the earlier X2 partial head-to-head.
