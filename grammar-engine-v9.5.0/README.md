# Notepad Grammar Engine 94 v2 — Complete Project Bundle (build v9.5.0)

This archive is the full take-away of the project: the offline grammar
Notepad app, the trained model, every script, all data, all results, the
report, and the exploration artifacts. `BUNDLE_MANIFEST.json` lists every
file with its size and SHA-256.

## Quick start

- Open `notepad-v9.5.0-grammar.html` in any modern browser. It is a single
  56,149,208-byte file, fully offline (no server, no network, no account):
  the Notepad editor with the trained grammar engine behind a
  Grammarly-style suggestion panel (score ring, category chips,
  accept/dismiss cards, Fix all).
- `notepad-v9.3.4-ORIGINAL.html` is the untouched upstream build, kept as
  the comparison baseline the report measures against.

## Contents

| Path | What it is |
| --- | --- |
| `model/` | The trained-model delivery: `gru2_best.pt` (shipped tagger), int8 exports (`engine94_weights.b64`, `engine94_data.json`, `engine94_rules.json`, `engine94.js`), `rules2.json`, `MODEL_CARD.md`, `SHA256SUMS.json`, plus its own `code/`, `data/` (v2 dataset), `results/`, `checkpoints/` |
| `code/` | Every project script, deduplicated by hash: dataset build, corruption, rules, engine (Python + JS), training, int8 export, HTML bundling, evaluation harnesses, GLM comparison, report generation |
| `code/data_authored/` | The authored corpus sources (school / work / tech error and correct sentences, per split) |
| `code/harper/` | The Harper WASM exploration modules — the engine path explored and rejected (documented in the report, Section 9) |
| `data-v1/` | The first-generation dataset (train / validation / calibration / final_test) |
| `results-extra/` | GLM run logs (`glm_full/`, including the empty careful-prompt log that documents the rate-limit blockage), the GLM head-to-head subset input, tagger reference, Harper final-test JSON |
| `report/` | `grammar-engine-results-report.docx` / `.pdf` and `figures/` |
| `screenshots/` | Browser screenshots of the suggestion panel (v9.5.0 shots 1–2, one v9.4 shot) |
| `experiments/harper-wasm-probe/` | The extracted Harper WASM model binaries (45 MB) from the rejected path |

## Key measured results (final held-out test, one-shot)

Precision 0.707, recall 0.507, F0.5 0.655, false alerts 3.2%, meaning
violations 0/89, 17 ms median latency. GLM head-to-head on the same
157-sentence subset: F0.5 0.666 vs 0.586 (standard) / 0.598 (careful);
precision 0.687 vs 0.562/0.578; false alerts 7.6% vs 24.2%; GLM retains
the recall edge (0.708 vs 0.594). Grammarly was not compared (no
account/API access). Full detail: `report/` and `model/MODEL_CARD.md`.

## Reproducing the pipeline

1. Dataset: `code/build_dataset.py` (+ `code/data_authored/`) → `model/data/`
2. Train: `code/train2.py` (chunked CPU training, train-val gap logged
   every epoch, early stopping)
3. Export: `code/export_js.py` → the `engine94_*` files
4. Bundle into the HTML: `code/build_html2.py` (path note: its engine
   modules live in `code/harper/` inside this bundle)
5. Evaluate: `code/eval_shipped2.js`, `code/run_comparison.py`
6. Integrity check: verify the 13 files in `model/SHA256SUMS.json`

## Not included in this bundle

- The superseded v9.4.0 intermediate Notepad build (rebuildable via
  `code/build_html2.py`; the shipped v9.5.0 is included)
- Training-resume checkpoints (`*_last.pt`) beyond those in
  `model/checkpoints/`, the v1 optimizer state, npm/torch install logs
- Nothing else was omitted: all distinct scripts, all four data splits
  (both generations), all result JSONs, and all exploration artifacts are
  in this archive.

## License

MIT for engine code, rules, and trained weights released with this
project. The combined Notepad HTML retains the licenses of its upstream
components (see the report).
