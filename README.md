# randomfiles

This repo also holds the **Notepad Grammar Engine 94 v2** delivery
(build v9.5.0) under `grammar-engine-v9.5.0/`:

- `grammar-engine-v9.5.0/notepad-v9.5.0-grammar.html` — the single-file
  offline grammar Notepad (56,149,208 bytes, fully offline).
- Full project: trained model (`model/`), all code (`code/`), datasets
  (`model/data/` + `data-v1/`), results incl. GLM head-to-head
  (`model/results/`, `results-extra/`), report (`report/`), screenshots.
- Every file is hash-listed in
  `grammar-engine-v9.5.0/BUNDLE_MANIFEST.json`.
- The complete single ZIP (160.3 MB) is attached as a Release asset —
  see Releases — since git itself blocks files over 100 MB.
- Key measured results (final held-out test): precision 0.707, recall
  0.507, F0.5 0.655, false alerts 3.2%, meaning violations 0/89,
  17 ms median latency.
