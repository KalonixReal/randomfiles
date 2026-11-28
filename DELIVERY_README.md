# Notepad Grammar Engine 94 v3 — Complete Project Bundle (build v9.7.2)

This archive is the full take-away of the project: the offline grammar
Notepad app, the trained model, every script, all data, all results, the
report, and the exploration artifacts. `BUNDLE_MANIFEST.json` lists every
file with its size and SHA-256.

## Quick start

- Open `notepad-v9.7.2-grammar.html` in any modern browser. It is a single
  8.7 MB file, fully offline (no server, no network, no account):
  the Notepad editor with the rules-2.9 grammar engine (163 rules), Hunspell
  spelling with the NZ/Maori lexicon, the v9.3.4 original suggestions
  panel, and the dormant neural tagger.
- `notepad-v9.3.4-ORIGINAL.html` is the untouched upstream build, kept as
  the comparison baseline (and the source of the restored suggestions UI).

## v9.7.2 in one line

v9.7.1 fixed the reported wh-subject FP family ("Why the process is
failing remains unclear." stays clean — the wh rules require
direct-question evidence) plus the singular -s noun guards. v9.7.2 then
mined the fresh set's 25 misses into 19 class-level families
("The essay discuss" -> "discusses", "Both proposal were" -> "proposals",
"will be close on Monday" -> "closed", "their has been" -> "there has
been", "significant improving" -> "improvement", ...) with a noun/verb
homograph split keeping compounds ("the book cover tears", "the job offer
expires") clean — FRESH set: sentence recall 1.00 (50/50) with 0/65 clean
false alerts (F0.5 1.000); X2 .923 / X3 .954 / dev .920 unchanged-or-up,
FA 0 everywhere. The bundled tagger was tested as a veto filter and
rejected (halves recall for zero FA gain).

## Contents

| Path | What it is |
| --- | --- |
| `model/` | The trained-model delivery: gru3 checkpoints, int8 exports (`engine94_*`), `rules2.json` (rules-2.9), `MODEL_CARD.md`, `SHA256SUMS.json`, `code/`, `data/` (v2 + v3 splits incl. X2/X3 one-shot sets and the FRESH comparison set), `results/` (v9.6.0 -> v9.7.2 evals, fresh-set comparison, tagger veto sweep, threshold sweep v4, GLM partial head-to-head) |
| `code/` | Every project script, deduplicated by hash: dataset build, corruption, rules, engine (Python + JS), training (v1-v3), int8 export, HTML bundling (build_html3.py = v9.6.0, build_html4.py = v9.7.x with the v9.3.4 UI restoration), evaluation harnesses incl. eval_fresh.js + tagger_veto_sweep.js, GLM comparison, report generation |
| `code/data_authored/` | The authored corpus sources |
| `code/harper/` | The Harper WASM exploration modules (rejected path) |
| `data-v1/` | The first-generation dataset |
| `results-extra/` | GLM run logs, tagger reference, Harper final-test JSON, fresh-set raw rows |
| `report/` | `grammar-engine-results-report.docx` / `.pdf` + `figures/` |
| `screenshots/` | v9.7.1 suggestion-panel screenshots + earlier shots |
| `experiments/harper-wasm-probe/` | The extracted Harper WASM model binaries |

## Reproducing the v9.7.1 pipeline

1. Rules: `code/build_rules2.py` -> `rules2.json` (rules-2.9)
2. Distillation: `distill_glm.js` / `distill_glm2.js` (GLM clean text +
   error pairs) + `code/build_train_aug.py`
3. Train tagger v3: `code/train3.py` (hard negatives, gap monitor)
4. Export: `code/export_js.py` (int8 blobs)
5. Bundle: `code/build_html4.py` (surgical blob + engine + NZ-lexicon
   injection into the 8.4 MB shell + v9.3.4 panel restoration)
6. Evaluate: `code/eval_x3.js` / `code/eval_x2.js` (shipped-file engine,
   strict + combined scoring), `code/eval_fresh.js` (fresh-set comparison
   incl. tagger-veto mode), `code/fp_adv2_check.js` (new-family strike zones), `code/fp_clean_check.js` /
   `code/fp_adv_check.js` (false-positive probes), `code/sweep_threshold.js`
7. Integrity: verify the files in `model/SHA256SUMS.json`

## Not included

Superseded builds (v9.4.0; v9.5.0 and v9.6.0 live in the earlier
`grammar-engine-v9.5.0-complete.zip` / `grammar-engine-v9.6.0-complete.zip`
releases, v9.7.0 in `grammar-engine-v9.7.0-complete.zip`), training-resume
checkpoints beyond the best ones, and the raw GLM API transcripts beyond the
saved logs.
