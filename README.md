# randomfiles

This repo holds the **Notepad Grammar Engine 94** delivery:

- `grammar-engine-v9.6.0/` — the current build (rules-2.3, 14
  false-positive families fixed, NZ/Māori spelling lexicon, GLM-distilled
  tagger v3 ships dormant by measurement). Quick start: open
  `grammar-engine-v9.6.0/notepad-v9.6.0-grammar.html` — single file,
  fully offline, 8.6 MB.
  - One-shot X2 eval: precision 0.893, F0.5 0.825, **0/97 clean false
    alerts**, 0–1 ms latency. Browser-measured displayed suggestions:
    0 false alerts on a 135-sentence natural NZ/UK corpus.
  - GLM head-to-head (rate-limited 93/170 partial): GLM F0.5 0.855 /
    recall 0.975 but 13% clean-sentence false alerts; ours 0%.
- `grammar-engine-v9.5.0/` — the previous delivery (measured: P 0.707,
  F0.5 0.655, FA 3.2% on its one-shot test; GLM head-to-head shipped
  F0.5 0.666 vs 0.586/0.598).
- Releases: complete ZIP bundles (v9.5.0 and v9.6.0), each file
  hash-verified via `BUNDLE_MANIFEST.json` inside.

Older unrelated files (NZOI archives, images, css) remain from before.
