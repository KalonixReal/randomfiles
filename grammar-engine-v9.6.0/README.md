# Notepad Grammar Engine 94 v3 — Complete Project Bundle (build v9.6.0)

This archive is the full take-away of the project: the offline grammar
Notepad app, the trained model, every script, all data, all results, the
report, and the exploration artifacts. `BUNDLE_MANIFEST.json` lists every
file with its size and SHA-256.

## Quick start

- Open `notepad-v9.6.0-grammar.html` in any modern browser. It is a single
  8,607,457-byte file, fully offline (no server, no network, no account):
  the Notepad editor with the rules-2.3 grammar engine, Hunspell spelling
  with the NZ/Maori lexicon, and the Writing-suggestions panel.
- `notepad-v9.3.4-ORIGINAL.html` is the untouched upstream build, kept as
  the comparison baseline.

## v9.6.0 in one line

Fourteen false-positive families fixed, NZ/tech spelling lexicon added,
tagger retrained with GLM-distilled hard negatives (ships dormant —
measured), fresh one-shot X2 evaluation: P 0.893 / F0.5 0.825 / 0 clean
false alerts / 0-1 ms latency; browser-measured displayed suggestions:
0 false alerts on the 135-sentence natural NZ/UK corpus.

## Contents

| Path | What it is |
| --- | --- |
| `model/` | The trained-model delivery: gru3 checkpoints, int8 exports (`engine94_*`), `rules2.json` (rules-2.3), `MODEL_CARD.md` (full v3 fix list + measurements), `SHA256SUMS.json`, `code/`, `data/` (v2 + v3 splits incl. X2 one-shot set), `results/` (incl. X2 evals, threshold sweep, GLM partial head-to-head, U1 browser harvest) |
| `code/` | Every project script, deduplicated by hash: dataset build, corruption, rules, engine (Python + JS), training (v1-v3), int8 export, HTML bundling, evaluation harnesses, GLM comparison, report generation |
| `code/data_authored/` | The authored corpus sources |
| `code/harper/` | The Harper WASM exploration modules (rejected path) |
| `data-v1/` | The first-generation dataset |
| `results-extra/` | GLM run logs, tagger reference, Harper final-test JSON |
| `report/` | `grammar-engine-results-report.docx` / `.pdf` + `figures/` |
| `screenshots/` | v9.6.0 suggestion-panel screenshots + earlier shots |
| `experiments/harper-wasm-probe/` | The extracted Harper WASM model binaries |

## Reproducing the v9.6.0 pipeline

1. Rules: `code/build_rules2.py` -> `rules2.json` (rules-2.3)
2. Distillation: `distill_glm.js` / `distill_glm2.js` (GLM clean text +
   error pairs) + `code/build_train_aug.py`
3. Train tagger v3: `code/train3.py` (hard negatives, gap monitor)
4. Export: `code/export_js.py` (int8 blobs)
5. Bundle: `code/build_html3.py` (surgical blob + engine + NZ-lexicon
   injection into the 8.4 MB shell)
6. Evaluate: `code/eval_shipped3.js` (shipped-file engine), `code/browser_harvest2.sh`
   (displayed suggestions), `code/sweep_threshold.js`
7. Integrity: verify the files in `model/SHA256SUMS.json`

## Not included

Superseded builds (v9.4.0; the v9.5.0 56 MB build lives in the earlier
`grammar-engine-v9.5.0-complete.zip` release), training-resume checkpoints
beyond those shipped, install logs. Everything else is in this archive.

## License

MIT for engine code, rules, lexicons, and trained weights released with
this project. The combined Notepad HTML retains the licenses of its
upstream components.
