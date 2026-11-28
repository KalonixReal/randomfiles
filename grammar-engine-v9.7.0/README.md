# Notepad Grammar Engine 94 v3 — Complete Project Bundle (build v9.7.0)

This archive is the full take-away of the project: the offline grammar
Notepad app, the trained model, every script, all data, all results, the
report, and the exploration artifacts. `BUNDLE_MANIFEST.json` lists every
file with its size and SHA-256.

## Quick start

- Open `notepad-v9.7.0-grammar.html` in any modern browser. It is a single
  8,702,088-byte file, fully offline (no server, no network, no account):
  the Notepad editor with the rules-2.7 grammar engine (144 rules), Hunspell
  spelling with the NZ/Māori lexicon, the v9.3.4 original suggestions
  panel, and the dormant neural tagger.
- `notepad-v9.3.4-ORIGINAL.html` is the untouched upstream build, kept as
  the comparison baseline (and the source of the restored suggestions UI).

## v9.7.0 in one line

Recall focus with zero false-alert regression: 34 new/extended rule
families mined from the fresh X3 one-shot set + dev FN analysis
("Where does the trail ends?", "What time the shop opens?", "should
studied", "have attend", "capable to fix", "plums in the bowl was",
fake-plural wh-reorder fix) — X2 F0.5 .825 → .914, X3 recall .389 → .926
(1.0 combined), dev F0.5 .881 → .927, all with 0 clean false alerts;
the v9.3.4 suggestions UI restored verbatim.

## Contents

| Path | What it is |
| --- | --- |
| `model/` | The trained-model delivery: gru3 checkpoints, int8 exports (`engine94_*`), `rules2.json` (rules-2.7), `MODEL_CARD.md` (full fix list + measurements), `SHA256SUMS.json`, `code/`, `data/` (v2 + v3 splits incl. X2/X3 one-shot sets), `results/` (incl. v9.6.0→v9.7.0 evals, threshold sweep v4, GLM partial head-to-head) |
| `code/` | Every project script, deduplicated by hash: dataset build, corruption, rules, engine (Python + JS), training (v1-v3), int8 export, HTML bundling (build_html3.py = v9.6.0, build_html4.py = v9.7.0 with the v9.3.4 UI restoration), evaluation harnesses, GLM comparison, report generation |
| `code/data_authored/` | The authored corpus sources |
| `code/harper/` | The Harper WASM exploration modules (rejected path) |
| `data-v1/` | The first-generation dataset |
| `results-extra/` | GLM run logs, tagger reference, Harper final-test JSON |
| `report/` | `grammar-engine-results-report.docx` / `.pdf` + `figures/` |
| `screenshots/` | v9.7.0 suggestion-panel screenshots + earlier shots |
| `experiments/harper-wasm-probe/` | The extracted Harper WASM model binaries |

## Reproducing the v9.7.0 pipeline

1. Rules: `code/build_rules2.py` -> `rules2.json` (rules-2.7)
2. Distillation: `distill_glm.js` / `distill_glm2.js` (GLM clean text +
   error pairs) + `code/build_train_aug.py`
3. Train tagger v3: `code/train3.py` (hard negatives, gap monitor)
4. Export: `code/export_js.py` (int8 blobs)
5. Bundle: `code/build_html4.py` (surgical blob + engine + NZ-lexicon
   injection into the 8.4 MB shell + v9.3.4 panel restoration)
6. Evaluate: `code/eval_shipped3.js` / `code/eval_x3.js` (shipped-file
   engine, strict + combined scoring), `code/fp_clean_check.js` /
   `code/fp_adv_check.js` (false-positive probes), `code/sweep_threshold.js`
7. Integrity: verify the files in `model/SHA256SUMS.json`

## Not included

Superseded builds (v9.4.0; the v9.5.0 56 MB build lives in the earlier
`grammar-engine-v9.5.0-complete.zip` release, and v9.6.0 in
`grammar-engine-v9.6.0-complete.zip`), training-resume checkpoints beyond
those shipped, install logs. Everything else is in this archive.

## License

MIT for engine code, rules, lexicons, and trained weights released with
this project. The combined Notepad HTML retains the licenses of its
upstream components.
