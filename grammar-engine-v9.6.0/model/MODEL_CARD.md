# Model Card — Notepad Grammar Engine 94 v3

## Model details
- **Name:** notepad-grammar-engine94-v3.0
- **Type:** deterministic rule engine (primary, measured) + neural edit tagger
  (shipped, dormant by threshold measurement)
- **Rule component:** 110 curated English grammar rules (rules-2.3) — v2 rules
  with 14 false-positive families fixed (see Fixes) — implemented identically
  in Python (scripts/engine.py) and in the browser engine
  (scripts/engine94.js; verified 0/251 mismatches on the dev split).
- **Neural component:** bidirectional GRU sequence tagger (GECToR-style
  per-token edit tagging over a 2,284-tag edit vocabulary), hidden 192,
  1.54 M parameters, trained v3 with GLM-distilled data + hard negatives.
- **Spelling:** the host shell's Hunspell GB/US dictionaries extended with a
  127-word NZ English / te reo Māori lexicon (build-time injection).
- **Quantisation:** int8 symmetric, 1,537,484 bytes of weights (2.05 MB base64).
- **Runtime:** pure JavaScript inside a Web Worker in the Notepad HTML file;
  no server, no network, no account. Threshold 1.0 (tagger dormant): median
  latency 0 ms/sentence (p90 1 ms) on the shipped build.
- **License:** MIT for engine code, rules, lexicons, and trained weights
  released with this project. The combined Notepad HTML retains the licenses
  of its upstream components.

## Intended use
Offline English grammar + spelling suggestions inside the single-file
Notepad HTML editor, presented through the Writing suggestions panel
(category chips, accept/dismiss cards, Fix all). Suggestions are minimal,
span-based, undoable, and guarded against edits that change meaning.

## Training data (tagger v3)
- 62,306 v2 rows (unchanged) + 480 distilled/authored rows: 100 GLM-written
  error pairs (7 error families), 264 GLM-written clean sentences
  (hard negatives), 116 authored clean sentences (hard negatives).
- GLM distillation is precision-directed: GLM authored clean text and error
  pairs; every "clean" sentence was re-validated against the rule engine
  (8 flagged -> all 8 were engine false positives, fixed; corpus passed 264/264).
- No user notebook data. No public GEC benchmark used for training or
  evaluation. Partitions unchanged (train S/W/T, dev D, calib K, test X,
  plus new author groups U1 = iteration eval, U2 = training negatives,
  X2 = final one-shot holdout).

## Training (tagger v3)
- 12 epochs, CPU-only, batch 48, AdamW (lr 2e-3 cosine, weight decay 0.01),
  weighted cross-entropy (non-KEEP x8), clipping 3.0, dropout 0.3.
- Overfit monitor: train-vs-dev loss gap logged every epoch (0.44 -> 1.62,
  visible and rising; selection by dev F0.5 with false-alert penalty;
  best epoch 10 of 12). The tagger's hard-negative FP rate reached 0.000 on
  trained negatives but stayed >0 on held-out U1 — memorisation, not
  generalisation: the measured decision below follows from this.

## Measured decision (v9.6.0): tagger ships DORMANT
Threshold sweep on dev/calib/test/U1 with the retrained tagger: at every
active threshold (0.98-0.999) the cascade scores lower F0.5 than rules-only
on every split, with higher false alerts. Rules-only (threshold 1.0) wins
everywhere; the tagger and its weights still ship (dormant) as the hybrid
architecture's neural component, with this measurement reported honestly.

## Fixes in v9.6.0 (all driven by mined false positives)
1. Question word order: correct questions with subject after auxiliary
   ("Which candidate did you vote for?") no longer reordered.
2. Perfect-inversion: "Have you seen", "Seldom have we seen" no longer
   flagged as "seen -> saw".
3. camelCase/technical identifiers: "kPoints holds" no longer re-pluralised
   (new no_camel guard, both engines).
4. Singular -s nouns and -ics/-is academic words: "Maths is", "Linguistics
   is", "The hypothesis was", "The chassis was" no longer flagged.
5. Adverb pseudo-subjects: "She sometimes seems" no longer flagged.
6. "a unanimous / a universal": y-sound words excluded from a->an.
7. Possessive modifiers: "yesterday's meeting have" no longer read as
   subject-verb disagreement.
8. Quantified-of subjects: "Neither of the options seems", "Each of the
   players receives" no longer flagged.
9. Base form after did/do/modals: "Not only did he finish" no longer
   flagged ("finish -> finishes").
10. i-SITE / Wi-Fi: standalone "i" capitalisation no longer fires inside
    hyphenated tokens.
11. Irregular participles: "was send" -> "was sent" (was "sended");
     gerund e-drop: "look forward to receive" -> "receiving"
     (was "receiveing").
12. Passive "told that": "We were told that..." no longer receives a bogus
    "told us" insertion.
13. WH agreement rules: same no_camel guard.
14. NZ/Māori spelling lexicon (127 words) into the Hunspell dictionaries —
    "marae", "tangi", "jandals", "rūnanga" etc. no longer flagged.

## Evaluation (equivalent-effect span scoring; X2 = fresh one-shot set)
- dev (rules-only): P=0.884 R=0.884 F0.5=0.884, FA=0.0%
- calib (rules-only): P=0.837 R=0.707 F0.5=0.807, FA=0.0%
- **X2 final one-shot (170 rows, 97 clean + 73 errors), shipped build:**
  **P=0.893, R=0.633, F0.5=0.825, false alerts 0/97, 0 ms median latency**
- Same X2, old v9.5.0 engine: P=0.766, R=0.620, F0.5=0.731, false alerts
  3/97 ("What time did", "hypothesis was", "receives -> receive")
- **Browser-measured displayed suggestions (the real UI), 40-sentence U1
  sample: 0 false alerts** (grammar 0; spelling 0 after NZ lexicon)
- U1 natural-clean corpus (135 sentences): 0 rule false alerts
  (was 7/135 = 5.2% before the fixes)
- GLM head-to-head on X2 (careful prompt): rate-limited to a 93/170-row
  partial run. On the completed subset GLM scored P=0.830, R=0.975,
  F0.5=0.855 with a 13% clean-sentence false-alert rate (7/54); our engine
  on the full 170 rows: P=0.893, R=0.633, F0.5=0.825 with 0/97 clean false
  alerts. GLM retains a recall advantage; ours retains the precision /
  false-alert advantage. Prior head-to-head on 157 sentences: shipped
  F0.5 0.666 vs GLM 0.586 standard / 0.598 careful; false alerts 7.6%
  vs 24.2%.
- Grammarly was not compared (no account/API/network access) — no claim is
  made about Grammarly.

## Known limitations
Recall remains bounded by the curated rule lists (0.633 on X2; unseen
plurals, spellings beyond the curated maps, unusual frames); the neural
tagger ships dormant because it does not yet beat the rules in the
cascade (solo dev F0.5 0.181 after v3 training; needs a stronger
architecture/training budget to contribute); the original dev/test splits
are saturated for the rules (FA 0.0%), so X2 and browser-harvest
measurements are the honest recall/FA evidence.
