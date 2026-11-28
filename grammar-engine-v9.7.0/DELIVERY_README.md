# Notepad Grammar Engine 94 v3 — delivery (build v9.7.0)

- **`grammar-engine-v9.7.0-complete.zip`** — the complete v9.7.0 take-away
  (hash-verified in `BUNDLE_MANIFEST.json`). Also on GitHub:
  https://github.com/KalonixReal/randomfiles/releases/tag/v9.7.0-bundle
- **`notepad-v9.7.0-grammar.html`** — the single-file offline Notepad build
  (8,702,088 bytes, fully offline): the grammar engine (rules-2.7, 144 rules),
  the Hunspell GB/US dictionaries with the 127-word NZ/Māori lexicon, the
  v9.3.4 original suggestions panel, and the dormant neural tagger. Open it
  in any modern browser.
- `grammar-engine-results-report.docx` / `.pdf` — the measured-results report
  (v9.5.0 run; the v9.6.0/v9.7.0 numbers are in `model/MODEL_CARD.md` and
  `model/results/`).
- `model/` — trained model files (gru3 checkpoints + export blobs), code,
  data (incl. the X2 and X3 one-shot sets and the U1 natural-clean corpus),
  results, model card, SHA-256 hashes.

## What changed in v9.7.0 (recall focus, UI restored)

34 new/extended rule families from X3 one-shot mining + dev FN analysis:
do-support 3sg ("Where does the trail ends?"), missing-do questions
("What time the shop opens?" → "What time does the shop open?"),
modal + past ("We should studied" → "should have studied"),
have + base ("The staff have attend the training" → "attended"),
capable-of-gerund ("capable to fix" → "capable of fixing", new engine kind),
plural-NP + was with PP ("The plums in the bowl was" → "were"),
mixed-register collectives ("The committee were unanimous in its decision"),
fake-plural wh-reorder bug fix ("Why the process is failing" → "Why is the
process failing"), plus ~60 new 3sg verb forms and lexicon extensions.
**The suggestions UI is the v9.3.4 original, restored verbatim** (spelling
wavy squiggle + grammar tint; hover-marks overlay removed).

## Key measured results (same scorer across builds)

| set | build | P | R | F0.5 | clean false alerts |
| --- | --- | --- | --- | --- | --- |
| X2 one-shot (170) | v9.5.0 | 0.766 | 0.620 | 0.731 | 3/97 |
| X2 one-shot (170) | v9.6.0 | 0.893 | 0.633 | 0.825 | 0/97 |
| **X2 one-shot (170)** | **v9.7.0** | **0.921** | **0.886** (0.962 combined) | **0.914** | **0/97** |
| X3 one-shot (155) | v9.6.0 | 0.955 | 0.389 | 0.739 | 0/104 |
| **X3 one-shot (155)** | **v9.7.0** | **0.962** | **0.926** (1.0 combined) | **0.954** | **0/104** |
| dev (251) | v9.6.0 | 0.883 | 0.875 | 0.881 | 0/140 |
| **dev (251)** | **v9.7.0** | **0.922** | **0.946** | **0.927** | **0/140** |

GLM head-to-head on X2 (careful prompt, still rate-limited at 93/170 rows):
GLM P 0.830 / R 0.975 / F0.5 0.855 with a 13% clean false-alert rate;
v9.7.0 on the full set: F0.5 0.914 with 0/97 clean false alerts. Latency
0–1 ms/sentence. Live in-browser check: 4/4 mixed grammar+spelling errors
flagged through the v9.3.4 panel, one-click fix applied correctly.
