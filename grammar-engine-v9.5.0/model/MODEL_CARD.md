# Model Card — Notepad Grammar Engine 94 v2

## Model details
- **Name:** notepad-grammar-engine94-v2.0
- **Type:** deterministic rule engine + neural edit tagger (hybrid cascade)
- **Neural component:** bidirectional GRU sequence tagger (GECToR-style per-token
  edit tagging over a 2,240-tag edit vocabulary), hidden size 192, 1.45 M parameters
- **Rule component:** 110 deterministic English grammar rules (rules2.json) with
  template/group-suffix/delete-space/end-period apply kinds and
  previous-regex/must-not-match, minimum-word-count guards — implemented
  identically in Python (scripts/engine.py) and in the browser engine
  (scripts/engine94.js; verified 251/251 identical findings on the dev split)
- **Quantisation:** int8 symmetric (per-tensor for GRU/output layers, per-row for
  embeddings), 1,445,600 bytes of weights (1.93 MB base64)
- **Runtime:** pure JavaScript inference inside a Web Worker in the Notepad HTML
  file; no server, no network, no account. In this build Engine94 v2 **replaces**
  the original Harper/T5 lint source in the suggestion panel (measured decision —
  see the report, Section 9).
- **License:** MIT for engine code, rules, and trained weights released with this
  project. The combined Notepad HTML retains the licenses of its upstream
  components.

## Intended use
Offline English grammar suggestions inside the single-file Notepad HTML editor,
presented through the Grammarly-style suggestion panel (score ring, category
chips, accept/dismiss cards, Fix all). Suggestions are minimal, span-based,
undoable, and guarded against edits that change meaning.

## Training data
- 62,306 training examples: 34,801 base rows (30,000 template-generated with
  recorded ground truth, 13,260 corruption variants of authored natural
  sentences, 1,941 authored entries) plus 27,505 fresh corruption variants
  generated from the training corpus for tagger v2 (train split only).
- No user notebook data. No public GEC benchmark used for training or evaluation.
- Provenance labels: authored, authored-clean, adversarial, template-clean,
  template-corrupt, natural-clean, natural-corrupt, aug-corrupt.
- Partitions by author group: train (S/W/T + templates + augmentations),
  dev (D groups; model selection and rule iteration), calib (K group; threshold
  calibration), test (X groups; fired once on the frozen final build).

## Training
- 6 epochs completed (resumable chunked training, CPU-only), batch 48, AdamW
  (lr 2e-3, cosine schedule, weight decay 0.01), weighted cross-entropy
  (non-KEEP tokens ×8), gradient clipping 3.0, dropout 0.3; best checkpoint by
  dev F0.5 (epoch 2). Train-vs-dev loss gap logged every epoch; early stopping
  active; the final test fired once with no test-informed tuning afterwards.

## Evaluation (measured; equivalent-effect span scoring)
- Development split: rules2 P=0.884 R=0.884 F0.5=0.884, FA=0.0%
- Calibration split: rules2 P=0.816 R=0.690 F0.5=0.787, FA=0.0%
- **Final held-out test (one-shot, shipped JS engine): P=0.707, R=0.507,
  F0.5=0.655, false-alert 3.2%, meaning violations 0/89, 17 ms median latency**
- Original build baseline (same test): P=0.278, R=0.640, F0.5=0.313, FA=48.8%,
  35/89 meaning violations
- **GLM head-to-head (same 157-sentence subset, identical scorer):**
  shipped F0.5 0.666 vs GLM 0.586 (standard) / 0.598 (careful);
  precision 0.687 vs 0.562/0.578; false alerts 7.6% vs 24.2%; GLM retains a
  recall advantage (0.708 vs 0.594). The full-483 GLM run was blocked by
  persistent API rate limits and is documented as not completed.
- Grammarly was not compared (no account/API/network access) — no claim is made
  about Grammarly.
- The neural tagger's measured net contribution at the shipped 0.995 threshold
  is slightly negative (−0.006 F0.5 on dev); it ships as the hybrid
  architecture's neural component with its contribution reported honestly.

## Known limitations
Recall is bounded by the curated rule lists (unseen noun plurals, spellings
beyond the 180-word curated map, unusual frames); the dev→test F0.5 gap
(0.884→0.655) reflects vocabulary shift between author groups; the tagger's
solo dev F0.5 is 0.163; a dictionary-based spellchecker is the highest-leverage
missing component.
