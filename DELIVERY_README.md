# Notepad Grammar Engine 94 v3 — delivery (build v9.6.0)

- **`notepad-v9.6.0-grammar.html`** — the single-file offline Notepad build
  (8,606,423 bytes, fully offline): the trained grammar engine (rules-2.3),
  the Hunspell GB/US dictionaries extended with a 127-word NZ/Māori lexicon,
  and the Writing-suggestions panel. Open it in any modern browser.
- `grammar-engine-results-report.docx` / `.pdf` — the measured-results report
  (v9.5.0 run; the v9.6.0 numbers are in `model/MODEL_CARD.md` and
  `model/results/`).
- `model/` — trained model files (gru3 checkpoints + export blobs), code
  pointer, data (incl. the fresh X2 one-shot set and the U1 natural-clean
  corpus), results, model card, SHA-256 hashes.

## What changed in v9.6.0 (false-positive focus)

Fourteen false-positive families fixed — question order ("Which candidate
did you vote for?"), perfect inversion ("Have you seen", "Seldom have we
seen"), camelCase identifiers ("kPoints holds"), singular -s nouns ("Maths
is", "Linguistics is", "The hypothesis was"), adverb subjects ("sometimes
seems"), "a unanimous", possessive modifiers, "Neither of the options
seems", "did he finish", i-SITE, irregular participles ("was send" ->
"sent", not "sended"), passive "told that", plus the NZ/Māori spelling
lexicon so "marae", "tangi", "jandals", "rūnanga" are no longer flagged.

## Key measured results (fresh one-shot X2 set, 170 rows)

| engine | P | R | F0.5 | clean false alerts | latency |
| --- | --- | --- | --- | --- | --- |
| v9.5.0 (old) | 0.766 | 0.620 | 0.731 | 3/97 | ~17 ms |
| **v9.6.0 (new)** | **0.893** | 0.633 | **0.825** | **0/97** | **0–1 ms** |

Browser-measured (the suggestions the app actually displays) on natural
NZ/UK text: **0 false alerts**. The retrained tagger (GLM-distilled hard
negatives) ships dormant: at every threshold the cascade measured worse
than rules-only, so the neural weights are retained but inactive — measured,
not hidden. GLM head-to-head: prior run had shipped F0.5 0.666 vs GLM
0.586/0.598 with GLM at 24.2% false alerts vs our 7.6%; the X2 head-to-head
is still rate-limited at publication time (partial run in `model/results/`).
