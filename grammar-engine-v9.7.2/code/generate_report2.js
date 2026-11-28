// Generates the v9.5.0 results report DOCX (English, R1 cover, DM-1 palette).
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  ImageRun, PageBreak, Header, Footer, PageNumber, NumberFormat,
  AlignmentType, HeadingLevel, WidthType, BorderStyle, ShadingType,
  TableLayoutType, TableOfContents, VerticalAlign,
} = require("docx");
const fs = require("fs");

const NB = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const allNoBorders = { top: NB, bottom: NB, left: NB, right: NB };
const noBorders = { top: NB, bottom: NB, left: NB, right: NB };

// DM-1 palette (Deep Cyan — AI/tech)
const P = {
  bg: "162235", accent: "37DCF2",
  titleColor: "FFFFFF", subtitleColor: "B0B8C0", metaColor: "90989F", footerColor: "687078",
  table: { headerBg: "1B6B7A", headerText: "FFFFFF", innerLine: "C8DDE2", surface: "EDF3F5" },
};

function calcCoverSpacing(params) {
  const { titleLineCount = 1, titlePt = 36, hasSubtitle = false, hasEnglishLabel = false,
    metaLineCount = 0, fixedHeight = 800, pageHeight = 16838 } = params;
  const SAFETY = 1200;
  const usableHeight = pageHeight - SAFETY;
  const titleHeight = titleLineCount * (titlePt * 23 + 200);
  const subtitleHeight = hasSubtitle ? (12 * 23 + 600) : 0;
  const englishLabelHeight = hasEnglishLabel ? (9 * 23 + 600) : 0;
  const metaHeight = metaLineCount * (10 * 23 + 100);
  const implicitParaHeight = 3 * 300;
  const contentHeight = titleHeight + subtitleHeight + englishLabelHeight + metaHeight + fixedHeight + implicitParaHeight;
  const remainingSpace = usableHeight - contentHeight;
  const safeRemaining = Math.max(remainingSpace, 400);
  const FOOTER_MIN = 800;
  const rawTop = Math.floor(safeRemaining * 0.45);
  const rawBottom = Math.floor(safeRemaining * 0.45);
  const bottomSpacing = Math.max(rawBottom, FOOTER_MIN);
  const topSpacing = Math.max(rawTop - Math.max(0, FOOTER_MIN - rawBottom), 400);
  return { topSpacing, bottomSpacing };
}

function buildCoverR1(config) {
  const padL = 1200, padR = 800;
  const availableWidth = 11906 - padL - padR - 300;
  const title = config.title;
  let titlePt = 40;
  let titleLines = [title];
  while (titlePt > 24 && titleLines[0].length * titlePt * 20 > availableWidth * 3) titlePt -= 2;
  const splitAtWord = (t, target) => {
    let i = Math.min(target, t.length - 1);
    while (i > 0 && t[i] !== " ") i--;
    if (i <= 0) return [t];
    return [t.slice(0, i), t.slice(i + 1)].filter(x => x);
  };
  if (title.length > 46) { titleLines = splitAtWord(title, 46); }
  else if (title.length > 23) { titleLines = splitAtWord(title, Math.ceil(title.length / 2)); }
  const titleSize = titlePt * 2;
  const spacing = calcCoverSpacing({
    titleLineCount: titleLines.length, titlePt,
    hasSubtitle: !!config.subtitle, hasEnglishLabel: !!config.englishLabel,
    metaLineCount: (config.metaLines || []).length, fixedHeight: 400,
  });
  const accentLeft = { style: BorderStyle.SINGLE, size: 8, color: P.accent, space: 12 };
  const children = [];
  children.push(new Paragraph({ spacing: { before: spacing.topSpacing } }));
  if (config.englishLabel) {
    children.push(new Paragraph({
      indent: { left: padL, right: padR }, spacing: { after: 500 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: P.accent, space: 8 } },
      children: [new TextRun({ text: config.englishLabel.split("").join("  "), size: 18, color: P.accent, font: { ascii: "Calibri" } })],
    }));
  }
  for (let i = 0; i < titleLines.length; i++) {
    children.push(new Paragraph({
      indent: { left: padL },
      spacing: { after: i < titleLines.length - 1 ? 100 : 300, line: Math.ceil(titlePt * 23), lineRule: "atLeast" },
      children: [new TextRun({ text: titleLines[i], size: titleSize, bold: true, color: P.titleColor, font: { ascii: "Arial" } })],
    }));
  }
  if (config.subtitle) {
    children.push(new Paragraph({
      indent: { left: padL }, spacing: { after: 800 },
      children: [new TextRun({ text: config.subtitle, size: 24, color: P.subtitleColor, font: { ascii: "Arial" } })],
    }));
  }
  for (const line of (config.metaLines || [])) {
    children.push(new Paragraph({
      indent: { left: padL + 200 }, spacing: { after: 80 },
      border: { left: accentLeft },
      children: [new TextRun({ text: line, size: 24, color: P.metaColor, font: { ascii: "Arial" } })],
    }));
  }
  children.push(new Paragraph({ spacing: { before: spacing.bottomSpacing } }));
  children.push(new Paragraph({
    indent: { left: padL, right: padR },
    border: { top: { style: BorderStyle.SINGLE, size: 2, color: P.accent, space: 8 } },
    spacing: { before: 200 },
    children: [
      new TextRun({ text: config.footerLeft || "", size: 16, color: P.footerColor, font: { ascii: "Arial" } }),
      new TextRun({ text: "                                        " }),
      new TextRun({ text: config.footerRight || "", size: 16, color: P.footerColor, font: { ascii: "Arial" } }),
    ],
  }));
  return [new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    layout: TableLayoutType.FIXED,
    borders: allNoBorders,
    rows: [new TableRow({
      height: { value: 16838, rule: "exact" },
      children: [new TableCell({
        shading: { type: ShadingType.CLEAR, fill: P.bg }, borders: noBorders, children,
      })],
    })],
  })];
}

// ---------- helpers
const F = (text, opts = {}) => new TextRun({ text, size: opts.size || 22, font: { ascii: "Calibri", eastAsia: "Calibri" }, color: opts.color || "1A1A1A", bold: opts.bold, italics: opts.italics });
const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 300, after: 160, line: 312 }, children: [F(t, { size: 30, bold: true, color: "0F3A4D" })] });
const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 240, after: 120, line: 312 }, children: [F(t, { size: 25, bold: true, color: "1B6B7A" })] });
const PARA = (runs, opts = {}) => new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { after: 120, line: 312 }, children: Array.isArray(runs) ? runs : [F(runs)], ...opts });
const BUL = (runs) => new Paragraph({ alignment: AlignmentType.LEFT, spacing: { after: 80, line: 312 }, bullet: { level: 0 }, children: Array.isArray(runs) ? runs : [F(runs)] });

function dataTable(caption, header, rows, widths) {
  const cell = (t, i, bold) => new TableCell({
    children: [new Paragraph({ alignment: AlignmentType.LEFT, spacing: { line: 276 }, children: [F(String(t), { size: 19, bold })] })],
    shading: i === 0 ? { type: ShadingType.CLEAR, fill: P.table.headerBg } : undefined,
    margins: { top: 50, bottom: 50, left: 100, right: 100 },
    verticalAlign: VerticalAlign.CENTER,
    width: widths ? { size: widths[i], type: WidthType.PERCENTAGE } : undefined,
  });
  return [
    new Paragraph({ keepNext: true, spacing: { before: 160, after: 60 }, children: [F(caption, { bold: true, size: 20, color: "0F3A4D" })] }),
    new Table({
      width: { size: 100, type: WidthType.PERCENTAGE },
      borders: {
        top: { style: BorderStyle.SINGLE, size: 2, color: P.table.headerBg },
        bottom: { style: BorderStyle.SINGLE, size: 2, color: P.table.headerBg },
        left: NB, right: NB,
        insideHorizontal: { style: BorderStyle.SINGLE, size: 1, color: "D0D0D0" },
        insideVertical: NB,
      },
      rows: [
        new TableRow({ tableHeader: true, cantSplit: true, children: header.map((h, i) => cell(h, 0, true)) }),
        ...rows.map(r => new TableRow({ cantSplit: true, children: r.map((c, i) => cell(c, 1)) })),
      ],
    }),
  ];
}

function figure(pngPath, widthPx) {
  const { imageSize } = require("image-size");
  const size = imageSize(fs.readFileSync(pngPath));
  const w = widthPx || 620;
  const h = Math.round(w * size.height / size.width);
  return new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { before: 120, after: 60 },
    children: [new ImageRun({ type: "png", data: fs.readFileSync(pngPath), transformation: { width: w, height: h } })],
  });
}

// ---------- content tables
const devRows = [
  ["No-change baseline", "0.000", "0.000", "0.000", "0.0%", "0"],
  ["Harper (raw)", "0.440", "0.357", "0.420", "14.3%", "12"],
  ["Harper (filtered)", "0.678", "0.357", "0.575", "0.0%", "0"],
  ["Existing T5 model", "0.311", "0.589", "0.344", "46.4%", "23"],
  ["Rules layer v1 (46 rules)", "0.780", "0.286", "0.580", "0.7%", "0"],
  ["Rules layer v2 (110 rules)", "0.884", "0.884", "0.884", "0.0%", "0"],
  ["Trained tagger v2 @0 (solo)", "0.152", "0.232", "0.163", "42.1%", "0"],
  ["Rules v2 + tagger @0.995", "0.876", "0.884", "0.878", "0.7%", "0"],
  ["Harper(f) + rules v2", "0.776", "0.804", "0.781", "0.0%", "0"],
  ["Original build (Harper+T5)", "0.295", "0.643", "0.331", "50.0%", "27"],
];

const calibRows = [
  ["Rules layer v2 (110 rules)", "0.816", "0.690", "0.787", "0.0%", "0"],
  ["Rules v2 + tagger @0.995", "0.812", "0.672", "0.780", "0.7%", "0"],
  ["Harper(f) + rules v2", "0.548", "0.586", "0.556", "7.4%", "3"],
];

const testRows = [
  ["No-change baseline", "0.000", "0.000", "0.000", "0.0%", "0"],
  ["Harper (raw)", "0.333", "0.257", "0.315", "17.4%", "13"],
  ["Existing T5 model", "0.283", "0.584", "0.316", "44.1%", "29"],
  ["SHIPPED v9.5.0 (rules v2 + tagger @0.995)", "0.707", "0.507", "0.655", "3.2%", "0"],
  ["Original build (Harper+T5)", "0.278", "0.640", "0.313", "48.8%", "35"],
];

const glmRows = [
  ["SHIPPED v9.5.0 (this build, offline)", "0.687", "0.594", "0.666", "5/66 = 7.6%", "0/16"],
  ["GLM (standard minimal-edit prompt)", "0.562", "0.708", "0.586", "16/66 = 24.2%", "n/a"],
  ["GLM (careful grammar prompt)", "0.578", "0.698", "0.598", "16/66 = 24.2%", "n/a"],
];

const targetRows = [
  ["Suggestion precision", "\u2265 85% on independently reviewed set", "0.707 shipped / 0.816\u20130.884 on dev-calib (rules)", "Not met at build level vs the 85% bar; +0.23 vs previous build"],
  ["False-alert rate", "< 5% of correct sentences", "3.2% shipped (9/281); 0.0% on dev and calib", "Met"],
  ["Recall", "Maximise at the precision threshold", "0.507 test / 0.884 dev / 0.690 calib", "Substantial improvement; below GLM's 0.708 on the subset"],
  ["Meaning preservation", "\u2265 99% of suggestions", "0 of 89 adversarial items flagged (0%)", "Met"],
  ["HTML size", "< 100,000,000 bytes", "56,149,208 bytes", "Met"],
  ["Median warm inference", "< 200 ms", "17 ms median, 28 ms p95 (JS harness, in-product worker code)", "Met"],
  ["Offline operation", "Zero network requests", "Engine, weights and rules embedded; runs from blob URLs", "Met"],
  ["Editing integrity", "No data-loss or corruption failures", "Accept, Fix-all, undo and re-scan verified in-browser", "Met (tested scope)"],
];

const deliverRows = [
  ["Trained model files", "download/model/ (GRU v2 checkpoint, quantised weights, vocab, rules v2, engine code, SHA-256 hashes)", "Delivered"],
  ["Notepad HTML build", "download/notepad-v9.5.0-grammar.html (56,149,208 bytes)", "Delivered"],
  ["Training + evaluation code", "download/model/code/ and scripts/", "Delivered"],
  ["Datasets + manifests + hashes", "download/model/data/", "Delivered"],
  ["Model card", "download/model/MODEL_CARD.md (v2)", "Delivered"],
  ["Results report", "This document + PDF render", "Delivered"],
  ["UI verification screenshots", "download/notepad-v9.5.0-shot-1.png, shot-2.png", "Delivered"],
  ["Grammarly direct comparison", "Not performed \u2014 no account, API, or network access in the sandbox", "NOT PERFORMED (documented)"],
  ["Official BEA-2019 / CoNLL-2014 scores", "Not computed \u2014 benchmark data not available offline", "NOT PERFORMED (documented)"],
  ["GLM LLM comparison", "Both prompts, same 157-sentence subset, identical scorer; full-483 GLM run blocked by persistent API rate limits", "COMPLETE (subset basis)"],
  ["Blind human review", "Not performed \u2014 no human reviewers available in the sandbox", "NOT PERFORMED (documented)"],
];

// ---------- document
const doc = new Document({
  styles: { default: { document: { run: { font: { ascii: "Calibri" } } } } },
  sections: [
    // ---- Cover
    {
      properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 0, bottom: 0, left: 0, right: 0 } } },
      children: buildCoverR1({
        title: "Offline Grammar Engine for Notepad",
        subtitle: "Training, Evaluation, GLM Comparison, and Product Integration Report \u2014 Build v9.5.0",
        englishLabel: "MEASURED RESULTS REPORT",
        metaLines: [
          "Engine: Engine94 v2 (110 rules + trained GRU edit tagger, int8)",
          "Baseline: notepad-v9.3.4 (Harper + T5-Efficient-tiny)",
          "Final held-out test split: 202 erroneous / 281 correct / 89 adversarial",
          "GLM comparison: same 157-sentence subset, identical scorer, both prompts",
          "Build size: 56,149,208 bytes (< 100,000,000 limit)",
        ],
        footerLeft: "Single-file offline HTML grammar system with Grammarly-style panel",
        footerRight: "2026-11-27",
      }),
    },
    // ---- TOC
    {
      properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1417, bottom: 1417, left: 1701, right: 1417 } } },
      children: [
        new Paragraph({ spacing: { before: 240, after: 120 }, children: [F("Contents", { bold: true, size: 30, color: "0F3A4D" })] }),
        new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-2" }),
        new Paragraph({ spacing: { before: 100 }, children: [F("Note: right-click the table of contents and choose Update Field to refresh page numbers.", { italics: true, size: 18, color: "808080" })] }),
        new Paragraph({ children: [new PageBreak()] }),
      ],
    },
    // ---- Body
    {
      properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1417, bottom: 1417, left: 1701, right: 1417 }, pageNumbers: { start: 1, formatType: NumberFormat.DECIMAL } } },
      headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [F("Offline Grammar Engine for Notepad \u2014 Results Report (v9.5.0)", { size: 16, color: "808080" })] })] }) },
      footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "808080" })] })] }) },
      children: [
        H1("1. Executive summary"),
        PARA([F("This report documents build v9.5.0 of the offline grammar-correction system for the single-file Notepad HTML editor: the engine, the measured GLM comparison, and the new Grammarly-style suggestion panel. The engine (\u201cEngine94 v2\u201d) combines "), F("110 deterministic grammar rules", { bold: true }), F(" (46 base + 64 new, many derived as exact inverses of the corruption generators), a "), F("genuinely trained neural edit tagger", { bold: true }), F(" (bidirectional GRU, hidden 192, 1.45M parameters, int8-quantised to 1.4 MB), protected-span and meaning guards, and \u2014 measured decision \u2014 "), F("replaces", { bold: true }), F(" the original Harper/T5 lint source in the shipped build.")]),
        PARA([F("On the final held-out test split (483 sentences; 202 erroneous, 281 correct, 89 adversarial), the shipped build measured "), F("precision 0.707, recall 0.507, F0.5 0.655, false-alert rate 3.2%, zero meaning violations, 17 ms median latency", { bold: true }), F(" \u2014 versus the original build\u2019s "), F("0.278 / 0.640 / 0.313 with 48.8% false alerts and 35/89 meaning violations", { bold: true }), F(".")]),
        PARA([F("Against GLM on the "), F("same 157-sentence subset with the identical scorer", { bold: true }), F(", the shipped offline engine measured "), F("F0.5 0.666 vs GLM 0.586 (standard prompt) and 0.598 (careful prompt)", { bold: true }), F("; precision 0.687 vs 0.562/0.578; false alerts on correct sentences "), F("7.6% vs 24.2%", { bold: true }), F("; zero meaning violations. GLM retains a recall advantage (0.708 vs 0.594). The comparison basis, scorer, and both prompts are stated exactly; the full-483 GLM run could not be completed (persistent API rate limits) and is documented as such.")]),
        PARA([F("Every number is a "), F("measured result", { bold: true }), F(" unless labelled a target. The final test fired "), F("once", { bold: true }), F(" on the frozen final configuration; all iteration happened on the development and calibration splits only.")]),

        H1("2. Scope and method"),
        PARA("The objective: the strongest practical offline English grammar correction for the Notepad HTML editor, with a genuinely trained neural component, a Grammarly-style suggestion experience, and honest measurement against the original build and an LLM (GLM), under the deployment constraints: one self-contained HTML file under 100,000,000 bytes, fully offline, no server, undo-safe editing."),
        H2("2.1 The original build (baseline system)"),
        PARA("The original notepad-v9.3.4.html embeds Harper 2.13.0 (WASM), a T5-Efficient-tiny grammar-correction model (ONNX), and a contextual-hint pipeline. Its engines were re-hosted outside the browser for measurement (Harper via Node WASM bindings; the T5 via onnxruntime with the build\u2019s own tokenisation and greedy decoding), so all baseline numbers are measured, not approximated."),
        H2("2.2 The new engine (Engine94 v2)"),
        BUL("Rules v2: 110 high-precision deterministic rules \u2014 the 46 base rules plus 64 new ones (singular/plural noun-subject agreement with collective-noun and measure guards, irregular plurals, contraction variants, over-regularised pasts, regular-past inverses, modal\u2013verb form rules, be+participle rules, person-state participles, broadened homophone contexts, question-inversion agreement rules, embedded-question inversion with context guard, pronoun case, adverb-form with verb-context guard, articles including a/an with silent-h and yoo-sound words, preposition frames, double comparatives, fewer/less, irregular possessives, double negatives, redundant \u201crevert back\u201d, missing final punctuation, and a 180-word curated misspelling map). New rule kinds (template, group-suffix-ing, delete-with-space, end-period) and guards (previous-regex must-match / must-not-match, minimum word count) are implemented identically in the Python harness and the browser engine."),
        BUL("Neural tagger v2: GECToR-style per-token edit tagger, bidirectional GRU (hidden 192, 1.45M parameters, 2,240-tag edit vocabulary), trained with 27,505 additional corruption variants generated from the training corpus, weighted cross-entropy (non-KEEP \u00d78), AdamW with cosine schedule, gradient clipping, early stopping, and train-vs-dev gap logging; int8-quantised to 1,445,600 bytes and shipped at a 0.995 confidence threshold with a word-pair fallback dictionary."),
        BUL("Guards: protected spans (prices, numbers, dates, times, URLs, e-mails, identifiers) are never edited; replacements that flip negation or change digits are rejected; tagger replacements must be alphabetic and may not rewrite capitalised tokens."),
        BUL("Composition (measured decision): Engine94 v2 is the sole lint source in the shipped build. On dev and calib, filtered Harper contributed zero unique true positives while adding unique false positives (SplitWords, TheMy, MergeWords, IsBeen classes), and overlap priority let Harper\u2019s findings block correct rule fixes \u2014 so the v9.5.0 build replaces the proof source entirely (Harper\u2019s worker still runs but its findings are no longer displayed; the replacement is at publish time)."),
        H2("2.3 Evaluation definitions"),
        PARA("Suggestion precision/recall/F0.5 use span-level scoring with an equivalent-effect matcher: a proposal is correct if applying it produces the same corrected sentence as a gold annotation (whitespace-normalised), or if it exactly matches a gold span and replacement. The false-alert rate is the share of correct sentences displaying at least one incorrect suggestion. Meaning violations are edits shown on adversarial correct sentences that change the facts. Latency is measured on the exact worker code shipped in the HTML. All systems are scored by the same harness; the GLM comparison uses the same matcher on GLM\u2019s corrected outputs (edit extraction by token diff, \u226550% span overlap with normalised replacement equality)."),

        H1("3. Data and partitions"),
        BUL("Training: 34,801 examples (30,000 template-generated with recorded ground truth, 13,260 corruption variants of 564 authored natural sentences, 1,941 authored entries) plus 27,505 fresh corruption variants generated for tagger v2. Thirty guarded, unit-tested corruption generators; protected-span aware."),
        BUL("Development (model selection / rule iteration): 251 sentences \u2014 111 erroneous, 140 correct, 63 adversarial. Author groups D1/D2."),
        BUL("Calibration (threshold selection): 191 sentences, author group K1 (deliberately informal NZ register \u2014 contractions, double negatives, \u201ched of passed\u201d constructions)."),
        BUL("Final test (untouched until the one-shot final run): 483 sentences \u2014 202 erroneous (209 gold edits), 281 correct, 89 adversarial. Author groups X1\u2013X3, disjoint from training."),
        PARA("Leakage controls: partitioning by author group, near-duplicate guard (Jaccard \u2265 0.7), immutable manifests with SHA-256 hashes recorded before the final run. UK/NZ and US varieties, school essays, professional writing, technical text, names, numbers, dates, quotations and negation are represented in every partition."),

        H1("4. Model training and selection"),
        PARA([F("Tagger v2 was trained (CPU-only) on the augmented corpus with early stopping; its best development F0.5 was 0.163 (solo, threshold 0). At the shipped 0.995 threshold, the tagger\u2019s measured net contribution on dev is "), F("\u22120.006 F0.5", { bold: true }), F(" and on calib \u22120.013 \u2014 the rules layer now covers most recoverable errors. The tagger remains in the shipped engine as the hybrid system\u2019s neural component (a deliberate architecture requirement of this project), gated at high confidence, with its measured contribution reported honestly. Overfitting controls: strict group-disjoint partitions, per-epoch dev evaluation with logged train/dev loss gap, early stopping, weight decay, dropout 0.3, and the one-shot final test \u2014 no test-informed tuning occurred after the final test fired.")]),

        H1("5. Measured results \u2014 engine level"),
        ...dataTable("Table 1. Development-split results (251 sentences; rule-iteration and model-selection set).", ["Engine", "Precision", "Recall", "F0.5", "False alerts", "Meaning viol."], devRows, [40, 13, 13, 13, 13, 13]),
        ...dataTable("Table 2. Calibration-split results (191 sentences; threshold-selection set, informal register).", ["Engine", "Precision", "Recall", "F0.5", "False alerts", "Meaning viol."], calibRows, [40, 13, 13, 13, 13, 13]),
        ...dataTable("Table 3. Final held-out test results (483 sentences, one-shot on the frozen build).", ["Engine", "Precision", "Recall", "F0.5", "False alerts", "Meaning viol."], testRows, [40, 13, 13, 13, 13, 13]),
        figure("/home/z/my-project/scripts/report_fig_prog.png", 560),
        PARA([F("Figure 1. ", { bold: true }), F("Engine-level F0.5 progression on the development split: rules v1 (46 rules) \u2192 rules v2 (110 rules) \u2192 combinations. The rules expansion (informed by a per-category miss analysis of the corruption generators\u2019 exact inverse mappings) lifted F0.5 from 0.580 to 0.884 while keeping the clean-sentence false-alert rate at zero.")]),
        PARA("The dev-to-test gap (F0.5 0.884 \u2192 0.655) reflects the test split\u2019s authored vocabulary and category mix (e.g., plural and spelling errors on words outside the curated rule lists); no rule was tuned against test data."),

        H1("6. GLM comparison (same subset, both prompts)"),
        PARA("GLM was run on a 157-sentence subset of the test split (125 erroneous, 16 authored-clean, 16 adversarial) with a standard minimal-edit prompt and a careful high-precision grammar prompt. All systems in this table are scored by the same equivalent-effect matcher on the same rows; GLM\u2019s outputs were collected before the engine was finalised."),
        ...dataTable("Table 4. Head-to-head on the shared 157-sentence subset (identical scorer).", ["System", "Precision", "Recall", "F0.5", "False alerts", "Meaning viol."], glmRows, [40, 12, 12, 12, 12, 12]),
        figure("/home/z/my-project/scripts/report_fig_pr2.png", 560),
        PARA([F("Figure 2. ", { bold: true }), F("Precision\u2013recall locations. The shipped offline engine sits in the high-precision/low-false-alert quadrant; GLM trades precision for recall and edits 24.2% of correct sentences.")]),
        figure("/home/z/my-project/scripts/report_fig_fa2.png", 560),
        PARA([F("Figure 3. ", { bold: true }), F("Clean-sentence false-alert rates: original build 48.8%, GLM 24.2% (both prompts), shipped build 7.6% on the subset and 3.2% on the full test split.")]),
        PARA([F("Measured interpretation: on the shared subset the shipped offline engine "), F("beats GLM under both prompts on F0.5 (0.666 vs 0.586/0.598), F1, precision, and false alerts (7.6% vs 24.2%)", { bold: true }), F(", with zero meaning violations. GLM wins recall (0.708 vs 0.594) \u2014 an inherent advantage of a 100B-scale general model over a 1.4 MB purpose-built offline engine, stated plainly here. The full-483 GLM comparison could not be completed: the sandbox API connection was persistently rate-limited (HTTP 429) during this session despite a patient retry loop; the 157-subset comparison is the measured basis and is labelled as such. GLM\u2019s pretraining may include public GEC corpora \u2014 disclosed as a comparison caveat.")]),

        H1("7. The Grammarly-style suggestion panel (product UI)"),
        PARA("Build v9.5.0 replaces the original suggestion panel with a Grammarly-style writing assistant, verified in-browser: an animated score ring (0\u2013100) with colour states, a per-category chip row (All / Grammar / Spelling / Punctuation) with live counts, suggestion cards showing the problem text struck through with an arrow to the replacement, a green \u201cUse X\u201d accept button per card, an explanation line, Dismiss / Dismiss-all controls, an \u201cAdd to dictionary\u201d action for spelling, a green \u201cFix all\u201d button, a clean state (green check, \u201cNo writing issues found\u201d), and a stats footer (words, sentences, reading time, engine badge)."),
        H2("7.1 In-browser verification (headless Chrome)"),
        BUL("Typed \u201cMy sister go to the library and she dont know a answer.\u201d \u2192 three cards rendered (go\u2192goes, dont\u2192doesn\u2019t, a\u2192an), score 42, footer stats live."),
        BUL("Clicked \u201cUse doesn\u2019t\u201d \u2192 the edit applied exactly to the editor text, the card disappeared, score rose to 56, remaining cards re-rendered."),
        BUL("Clicked \u201cFix all\u201d \u2192 final text \u201cMy sister goes to the library and she doesn\u2019t know an answer.\u201d, zero cards, score 100, clean state with the green check."),
        BUL("No console errors; the panel re-scans after every edit; screenshots delivered (notepad-v9.5.0-shot-1.png, shot-2.png)."),
        H2("7.2 Latency (in-product worker code, JS harness)"),
        ...dataTable("Table 5. Latency of the shipped engine (483-sentence run, Node harness on the exact worker code).", ["Metric", "Measured", "Target", "Status"], [
          ["Median warm inference per sentence", "17 ms", "< 200 ms", "Met"],
          ["p95 warm inference per sentence", "28 ms", "reported", "Met"],
          ["Full 483-sentence batch wall time", "\u224814 s", "reference", "n/a"],
        ], [46, 20, 20, 14]),

        H1("8. Cross-runtime equivalence and quantisation"),
        PARA("The JavaScript rule engine was verified against the Python reference on all 251 development sentences: 251/251 identical proposal sets (spans, replacements, types) with the 110-rule ruleset, including all new rule kinds and guards. The neural path is int8-quantised (symmetric per-tensor for GRU/output layers, per-row for embeddings): 1,445,600 bytes int8 (1.93 MB base64) versus 5.8 MB fp32 \u2014 the shipped HTML grows by only ~2.7 MB over the original build while embedding the full trained engine."),

        H1("9. Harper replacement decision (measured)"),
        PARA("The v9.4.0 build merged Engine94 findings into Harper\u2019s (Harper winning overlaps). With rules v2, that composition became strictly worse on both dev and calib: every remaining filtered-Harper true positive overlapped an existing rule fix (zero unique TPs), while Harper added unique false positives and its overlap priority blocked correct rule fixes. Per-class contribution tables (dev and calib) are in the results directory. The v9.5.0 build therefore replaces the lint source at publish time: record.lints = Engine94 findings. Harper\u2019s worker continues to run (its scan is the trigger cadence for re-proofing) but its findings are no longer displayed; the measured effect is the move from F0.5 0.479 (v9.4.0, Harper-composed) to 0.655 (v9.5.0, engine-only) on the test split."),

        H1("10. Targets versus measured results"),
        ...dataTable("Table 6. Targets versus measured results.", ["Metric", "Target (from brief)", "Measured (final test unless stated)", "Status"], targetRows, [16, 28, 34, 22]),
        PARA("The 85% precision target remains unmet at build level on the final test (0.707); on dev and calib the rules layer alone measures 0.88/0.82 precision with zero false alerts. The remaining test-split false positives and misses concentrate in vocabulary outside the curated lists (plural forms of unseen nouns, spellings beyond the 180-word curated map, unusual sentence frames) \u2014 the known cost of the no-network, single-file constraint, documented rather than hidden."),

        H1("11. Deliverables and verification"),
        ...dataTable("Table 7. Deliverables and completion status.", ["Item", "Location / detail", "Status"], deliverRows, [24, 56, 20]),
        PARA("HTML size: 56,149,208 bytes (limit 100,000,000 \u2014 met). Offline: the engine, quantised weights, vocabulary, rules and the panel code are embedded in the HTML and run from blob URLs; zero network requests. Editor integrity: accept, fix-all, undo and re-scan verified in-browser through the product\u2019s own edit pipeline."),

        H1("12. Limitations and unfinished work"),
        BUL("The neural tagger\u2019s measured net contribution at the shipped 0.995 threshold is slightly negative (\u22120.006 F0.5 on dev); it ships as the hybrid architecture\u2019s neural component, and better training data (larger authored corpora) is the highest-leverage next step."),
        BUL("Recall on the test split (0.507) trails GLM (0.708 on the subset): the curated-list design trades recall for precision and offline size; a dictionary-based spell checker and broader noun coverage are the obvious extensions."),
        BUL("The GLM comparison is subset-based (157 of 483); the full run was blocked by persistent API rate limits (HTTP 429) with a documented retry loop. No GLM number is extrapolated."),
        BUL("Official BEA-2019/CoNLL-2014 scoring was not computed (no benchmark access offline); the equivalent-effect scorer is documented and must not be read as official benchmark scores."),
        BUL("Human/blind review was not performed; all annotation authorship and review were machine-only inside the sandbox and are labelled as such."),
        BUL("Harper still runs in the background (its findings are replaced, not the worker); a future build could disable its scan entirely to save CPU."),
        BUL("The dev\u2192test F0.5 gap (0.884\u21920.655) is a generalization cost of list-based rules under vocabulary shift; it is reported, not tuned away (the final test fired once)."),

        H1("13. Reproduction"),
        PARA("Pipeline: build_dataset.py \u2192 build_rules2.py (rules v2 with new kinds/guards) \u2192 train2.py (tagger v2, resumable chunks) \u2192 export_js.py (int8 export of rules v2 + gru2 checkpoint) \u2192 build_html2.py (single-file HTML with the Engine94 replacement patch and the Grammarly-style panel). Evaluation: node check_rules_equiv.js (Python\u2194JS parity), node eval_shipped2.js (one-shot final test on the exact worker code), python3 score_glm_subset.py (GLM subset scoring), browser verification via agent-browser. All code, data, manifests and SHA-256 hashes are delivered under download/model/."),
      ],
    },
  ],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync("/home/z/my-project/download/grammar-engine-results-report.docx", buf);
  console.log("report written:", buf.length, "bytes");
});
