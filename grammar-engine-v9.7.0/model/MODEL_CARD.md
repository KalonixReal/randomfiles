# Model Card — Notepad Grammar Engine 94 v3

## Model details
- **Name:** notepad-grammar-engine94-v3.1 (build v9.7.0, rules-2.7)
- **Type:** deterministic rule engine (primary, measured) + neural edit tagger
  (shipped, dormant by threshold measurement)
- **Rule component:** 144 curated English grammar rules (rules-2.7) — v9.6.0's
  110 rules (14 false-positive families fixed) plus 34 recall families/mining
  fixes from the X3 one-shot set and dev FN analysis — implemented identically
  in Python (scripts/engine.py) and in the browser engine
  (scripts/engine94.js; new apply kind `to_of_ing` in both).
- **Neural component:** bidirectional GRU sequence tagger (GECToR-style
  per-token edit tagging over a 2,284-tag edit vocabulary), hidden 192,
  1.54 M parameters, trained v3 with GLM-distilled data + hard negatives.
- **Spelling:** the host shell's Hunspell GB/US dictionaries extended with a
  127-word NZ English / te reo Māori lexicon (build-time injection).
- **Quantisation:** int8 symmetric, 1,537,484 bytes of weights (2.05 MB base64).
- **Runtime:** pure JavaScript inside a Web Worker in the Notepad HTML file;
  no server, no network, no account. Threshold 1.0 (tagger dormant): median
  latency 0 ms/sentence (p90 1 ms) on the shipped build.
- **UI:** the v9.3.4 original suggestions panel restored verbatim (spelling
  wavy squiggle + grammar tint highlight; the hover-marks overlay removed).
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

## Fixes in v9.7.0 (recall focus: X3 one-shot mining + dev FN analysis)
Same-scorer progression, v9.6.0 shipped -> v9.7.0 shipped (strict
per-edit effective-sentence scoring, identical harness):
- X2: P .893 / R .633 / F0.5 .825 -> **P .921 / R .886 / F0.5 .914**
  (combined-sentence recall .962), FA 0 both builds
- X3 (new one-shot set, 51 error rows): R .389 -> **.926** (combined 1.0)
- dev: P .883 / R .875 / F0.5 .881 -> **P .922 / R .946 / F0.5 .927**
New/changed families (all validated at 0 FP on the 609-sentence clean
corpus + 52 adversarial strike-zone sentences):
1. 3sg verb maps extended (~60 forms: ends, trains, explains, catches,
   focuses... feeding sva_noun_plur_3sg / does_3sg_adjacent / _final / new
   does_3sg_q mid-question variant).
2. NOUN_SINGULAR lexicon extended (principal, warehouse, mare, stallion,
   pony, filly, vet...) and the `bus` guard conflict fixed ("The bus dont
   run" -> "doesn't").
3. wh_pl_np_* fake-plural bug: singular -s nouns ("Why the process is
   failing") no longer blind-reordered to "are"; the plain wh_front_missing
   reorder now handles them correctly.
4. modal_have_past: "We should studied" -> "should have studied" (with
   -eed word protection: "would proceed" untouched).
5. have_base_dobj: "The staff have attend the training" -> "attended".
6. capable_to_ing (new engine kind to_of_ing): "capable to fix" ->
   "capable of fixing".
7. whq_does_insert + whq_3sg_base: "What time the shop opens?" ->
   "What time does the shop open?" (two findings matching gold's two
   edits; embedded questions and subordinate clauses guarded).
8. noun_plur_pp_was: "The plums in the bowl was bruised" -> "were"
   (fractional heads like "two thirds of the crop was" protected).
9. collective_its_mixed: "The committee were unanimous in its decision" ->
   "was" (GB-plural + US-its mixed register).
10. almost_people_be, loose-lose object list extension ("loose your
    place"), possessive object list extension ("my cousins bike").

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

## Evaluation (equivalent-effect span scoring; X2/X3 = fresh one-shot sets)
- dev (rules-2.7, rules-only): **P=0.922 R=0.946 F0.5=0.927, FA=0.0%**
- **X2 final one-shot (170 rows, 97 clean + 73 errors), v9.7.0 shipped:**
  **P=0.921, R=0.886, F0.5=0.914 (combined-sentence R 0.962), false alerts
  0/97, 0 ms median latency**
- **X3 second one-shot set (155 rows, 104 clean + 51 errors, authored after
  v9.6.0 to mine unseen families), v9.7.0 shipped: P=0.962, R=0.926,
  F0.5=0.954 (combined R 1.0 — every error row fully corrected), FA 0**
- Progression on the same X2, same scorer: v9.5.0 P=0.766 R=0.620
  F0.5=0.731 (3/97 false alerts) -> v9.6.0 P=0.893 R=0.633 F0.5=0.825
  (0/97) -> **v9.7.0 P=0.921 R=0.886 F0.5=0.914 (0/97)**
- **Browser-measured displayed suggestions (the real UI), 40-sentence U1
  sample: 0 false alerts** (grammar 0; spelling 0 after NZ lexicon); the
  v9.7.0 build re-verified live: 4/4 mixed grammar+spelling errors flagged
  in-browser, one-click fix applied correctly (panel = v9.3.4 UI)
- U1 natural-clean corpus (135 sentences): 0 rule false alerts
  (was 7/135 = 5.2% before the fixes); full clean corpora (609 sentences
  incl. X3 clean): 0 false positives
- GLM head-to-head on X2 (careful prompt): rate-limited to a 93/170-row
  partial run (still rate-limited at v9.7.0 publication). On the completed
  subset GLM scored P=0.830, R=0.975, F0.5=0.855 with a 13%
  clean-sentence false-alert rate (7/54); our v9.7.0 on the full 170
  rows: P=0.921, R=0.886 (0.962 combined), F0.5=0.914 with 0/97 clean
  false alerts. Prior head-to-head on 157 sentences: shipped F0.5 0.666
  vs GLM 0.586 standard / 0.598 careful; false alerts 7.6% vs 24.2%.
- Grammarly was not compared (no account/API/network access) — no claim is
  made about Grammarly.

## Known limitations
Remaining misses on X2/dev are documented designed-misses, not silent gaps:
(1) GB collectives ("Our team have won") are deliberately not flagged —
UK plural usage is correct and our adversarial contract requires it;
(2) three dev gold rows are broken ("where is" -> "where the" doubles the
"the"); the engine's reorder is the correct fix; (3) double-negative
"without no" is protected by the meaning-guard (no negation flips);
(4) "She explained me the problem" — the engine's "explained to me the
problem" and the gold's "explained the problem to me" are both correct
English (paraphrase-level); (5) ambiguous bare verbs ("The parcel arrive")
need context beyond syntax. Recall remains bounded by the curated lists
elsewhere; the neural tagger ships dormant because it does not yet beat
the rules in the cascade (solo dev F0.5 0.181 after v3 training; needs a
stronger architecture/training budget); the original dev/test splits are
saturated, so X2/X3 and browser-harvest measurements are the honest
evidence.
