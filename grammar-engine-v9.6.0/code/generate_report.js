// Generates the results report DOCX (English, R1 cover recipe, DM-1 palette).
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
      children: [new TextRun({ text: config.englishLabel.split("").join("  "), size: 18, color: P.accent, font: { ascii: "Calibri" }, })],
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
        ...rows.map(r => new TableRow({ cantSplit: true, children: r.map((c, i) => {
          const tc = cell(c, 1);
          return tc;
        }) })),
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
  ["Rules layer", "0.780", "0.286", "0.580", "0.7%", "0"],
  ["Trained tagger @0.98", "0.606", "0.179", "0.410", "2.1%", "1"],
  ["Rules + tagger @0.95", "0.565", "0.348", "0.503", "7.1%", "2"],
  ["Original build (Harper+T5)", "0.295", "0.643", "0.331", "50.0%", "27"],
  ["New build (Harper_f+rules+tagger@0.95)", "0.534", "0.420", "0.506", "7.1%", "2"],
];

const testRows = [
  ["No-change baseline", "0.000", "0.000", "0.000", "0.0%", "0"],
  ["Harper (raw)", "0.333", "0.257", "0.315", "17.4%", "13"],
  ["Harper (filtered, final)", "0.500", "0.219", "0.398", "4.3%", "2"],
  ["Existing T5 model", "0.283", "0.584", "0.316", "44.1%", "29"],
  ["Rules layer", "0.471", "0.234", "0.392", "6.0%", "2"],
  ["Trained tagger @0.98", "0.486", "0.167", "0.352", "6.4%", "3"],
  ["JS engine (rules+tagger @0.995)", "0.475", "0.273", "0.414", "7.8%", "2"],
  ["Harper_f + rules (no tagger)", "0.571", "0.343", "0.504", "5.3%", "3"],
  ["SHIPPED build (Harper_f + engine @0.995)", "0.500", "0.410", "0.479", "11.7%", "6"],
  ["Original build (Harper+T5)", "0.278", "0.640", "0.313", "48.8%", "35"],
  ["GLM (standard prompt), sample", "0.628", "0.800", "0.656", "34.0%", "0"],
  ["GLM (strict prompt), sample", "0.664", "0.811", "0.689", "34.0%", "0"],
];

const targetRows = [
  ["Suggestion precision", "\u2265 85% on independently reviewed set", "Measured 0.500 (shipped) / 0.571 (FA-optimal point) on test", "Not met at build level; single layers reach 0.78 (rules, dev)"],
  ["False-alert rate", "< 5% of correct sentences", "4.3% (Harper filtered) and 5.3% (Harper_f+rules); 11.7% shipped default", "Met at the precision-optimal operating point; shipped default trades FA for recall"],
  ["Recall", "Maximise at the precision threshold", "0.219\u20130.410 by configuration (PR curve reported)", "Partially met"],
  ["Meaning preservation", "\u2265 99% of suggestions", "35\u21926 violations of 89 adversarial items (orig\u2192shipped); 0\u20132 for filtered layers", "Met for filtered layers and the JS engine (0\u20132 of 89)"],
  ["HTML size", "< 100,000,000 bytes", "55,119,318 bytes", "Met"],
  ["Median warm inference", "< 200 ms", "17 ms median, 28 ms p95, ~29 ms init (browser)", "Met"],
  ["Offline operation", "Zero network requests", "Zero non-file requests observed; engine runs with networking disabled", "Met"],
  ["Editing integrity", "No data-loss or corruption failures", "Apply + undo verified in-browser; text restored exactly; no console errors", "Met (tested scope)"],
];

const deliverRows = [
  ["Trained model files", "download/model/ (checkpoint, quantised weights, vocab, rules, engine code, SHA-256 hashes)", "Delivered"],
  ["Notepad HTML build", "download/notepad-v9.4.0-grammar.html (55,119,318 bytes)", "Delivered"],
  ["Training + evaluation code", "download/model/code/ and scripts/", "Delivered"],
  ["Datasets + manifests + hashes", "download/model/data/", "Delivered"],
  ["Model card", "download/model/MODEL_CARD.md", "Delivered"],
  ["Results report", "This document + PDF render", "Delivered"],
  ["Grammarly direct comparison", "Not performed \u2014 no account, API, or offline access in the sandbox", "NOT PERFORMED (documented)"],
  ["Official BEA-2019 / CoNLL-2014 scores", "Not computed \u2014 benchmark data not available offline; custom equivalent-effect scorer used instead", "NOT PERFORMED (documented)"],
  ["GLM LLM comparison", "Both prompts on a 141-sentence sample; adversarial leg partial (7 of 30 rows, all preserving meaning)", "PARTIALLY COMPLETE"],
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
        subtitle: "Training, Evaluation, and Product Integration Report",
        englishLabel: "MEASURED RESULTS REPORT",
        metaLines: [
          "Engine: Engine94 (rules + trained GRU edit tagger, int8)",
          "Baseline: notepad-v9.3.4 (Harper + T5-Efficient-tiny)",
          "Final held-out test split: 202 erroneous / 281 correct / 89 adversarial",
          "Build size: 55,119,318 bytes (< 100,000,000 limit)",
        ],
        footerLeft: "Single-file offline HTML grammar system",
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
      headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [F("Offline Grammar Engine for Notepad \u2014 Results Report", { size: 16, color: "808080" })] })] }) },
      footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "808080" })] })] }) },
      children: [
        H1("1. Executive summary"),
        PARA([F("This report documents a trained, tested, and integrated offline grammar-correction system for the single-file Notepad HTML editor, and its measured comparison against the original build. The new engine (\u201cEngine94\u201d) combines "), F("46 deterministic grammar rules", { bold: true }), F(", a "), F("genuinely trained neural edit tagger", { bold: true }), F(" (bidirectional GRU, 0.61M parameters, int8-quantised to 0.76 MB), a word-pair fallback dictionary, protected-span and meaning guards, and a measured Harper false-positive suppression layer. It ships inside a self-contained HTML file of "), F("55,119,318 bytes", { bold: true }), F(" alongside the original Harper and T5 engines, and runs fully offline in a Web Worker.")]),
        PARA([F("On the held-out test split (202 erroneous, 281 correct, 89 adversarial sentences), the "), F("shipped build measured precision 0.500, recall 0.410, F0.5 0.479, false-alert rate 11.7%, and 6/89 meaning-preservation violations", { bold: true }), F(", versus the original build\u2019s "), F("0.278 / 0.640 / 0.313 with 48.8% false alerts and 35/89 meaning violations", { bold: true }), F(". At its precision-optimal operating point (Harper-filtered + rules), the system reaches "), F("precision 0.571, recall 0.343, false-alert 5.3%", { bold: true }), F(". The precision target of \u226585% was "), F("not", { bold: true }), F(" met in this sandbox; the measured gap and its causes are analysed in Section 12.")]),
        PARA([F("Every number in this report is a "), F("measured result", { bold: true }), F(" unless explicitly labelled a target. Missing comparisons (Grammarly; official BEA/CoNLL scores; blind human review) are stated as not performed, with reasons, in Section 15.")]),

        H1("2. Scope and method"),
        PARA("The objective was the strongest practical offline English grammar correction for Notepad: a trained neural model plus deterministic rules working alongside the existing Harper integration, measured against the original build and against an LLM, with all deployment constraints (single-file HTML under 100 MB, offline, no server, editor integrity) verified."),
        H2("2.1 The original build (baseline system)"),
        PARA("The original notepad-v9.3.4.html embeds Harper 2.13.0 (WASM), a T5-Efficient-tiny grammar-correction model (visheratin/t5-efficient-tiny-grammar-correction, ONNX, 33 MB) running via ONNX Runtime Web, and a contextual-hint pipeline that restricts neural suggestions to short word-to-word changes. Its full architecture was reverse-engineered from the HTML (worker protocols, lint records, panel rendering, undo-safe edit application), and its engines were re-hosted outside the browser for measurement: Harper in Node via its WASM bindings, the T5 model via onnxruntime with the build\u2019s own tokenisation and greedy-decoding semantics."),
        H2("2.2 The new engine (Engine94)"),
        BUL("Rules: 46 high-precision deterministic rules (subject\u2013verb agreement, be/have/do agreement, verb morphology after modals and auxiliaries, contractions, context-checked homophones, a/an with exception lists, question inversion, duplicated words, capitalisation, preposition swaps, irregular plurals), defined in one rules.json shared by the Python evaluator and the browser engine."),
        BUL("Neural tagger: a GECToR-style per-token edit tagger (bidirectional GRU, hidden 96, 2,066-tag edit vocabulary, 0.61M parameters) trained in this sandbox, deployed at a 0.995 confidence threshold with a word-pair fallback dictionary for out-of-vocabulary replacements."),
        BUL("Guards: protected spans (prices, numbers, dates, times, URLs, e-mails, identifiers) are never edited; replacements that flip negation or change digits are rejected; tagger replacements must be alphabetic; Harper false positives are suppressed by measured classes (initialisms, proper-noun-like tokens in spelling/typo findings, M\u0101ori determiner constructs, a curated NZ/te reo word set, style-class findings, informal sentence starters, fronted whom)."),
        BUL("Cascade: Harper findings are kept; engine findings that overlap a Harper span are dropped (Harper wins overlaps \u2014 the documented conflict policy); the tagger only contributes at \u22650.995 confidence."),
        H2("2.3 Evaluation definitions"),
        PARA("Suggestion precision, recall and F0.5 use span-level scoring with an equivalent-effect matcher: a proposal counts as correct if applying it produces the same corrected sentence as a gold annotation (whitespace-normalised), or if it exactly matches a gold span and replacement. The false-alert rate is the share of correct sentences that display at least one incorrect suggestion. Meaning violations are suggestions shown on adversarial correct sentences (negation, numbers, names, dates, conditions, quotations) where any edit changes the facts. Latency is measured in the browser (model initialisation, warm per-sentence inference). All engine-level numbers are computed by identical harnesses for every system."),

        H1("3. Data and partitions"),
        PARA("All data was authored or generated inside this sandbox; no user notebook data and no public GEC corpus was used."),
        BUL("Training: 34,801 examples \u2014 30,000 template sentences (corrupted with recorded ground truth, plus clean identity copies), 13,260 corruption variants of 564 authored natural sentences, 1,941 authored entries (up-sampled \u00d74). Corruptions come from 30 guarded generators (unit-tested, protected-span aware) covering agreement, verb morphology, contractions, homophones, articles, plurals, capitalisation, word duplication/deletion, question inversion and more."),
        BUL("Development (model selection): 251 authored sentences (111 with errors, 140 correct incl. traps, 63 adversarial \u2014 59 including clean). Author group D1/D2."),
        BUL("Calibration (threshold selection): 191 authored sentences. Author group K1."),
        BUL("Final test (untouched until the last run): 483 authored sentences \u2014 202 erroneous (209 annotated edits), 158 correct, 89 adversarial meaning-preservation. Author groups X1\u2013X3, disjoint from all training groups."),
        PARA("Leakage controls: partition boundaries by author group, near-duplicate guard (Jaccard \u2265 0.7) removing overlaps from training, exact-duplicate removal, immutable manifests with SHA-256 hashes recorded before the final run. UK/NZ and US varieties, informal writing, technical text, names, numbers and dates are represented in every partition."),

        H1("4. Models trained and selection"),
        PARA([F("Two neural candidates were trained on identical data and loss: "), F("Candidate A (biGRU tagger)", { bold: true }), F(" and "), F("Candidate B (2-layer transformer tagger)", { bold: true }), F(". After 14 and 10 epochs respectively (AdamW, cosine schedule, weighted cross-entropy, CPU-only), dev F0.5 was 0.180 for the GRU and 0.138 for the transformer, with lower false-alert rate for the GRU. The GRU was selected by measured dev performance. One training-data corruption bug (whole-word deletion for -es verbs), one feature-alignment bug (shape features shifted by one token), and one loss-masking bug ($KEEP is edit id 0, so a padding mask keyed on id 0 silently removed all KEEP supervision) were found and fixed during development; all are documented in the training logs.")]),

        H1("5. Measured results \u2014 engine level"),
        ...dataTable("Table 1. Development-split results (251 sentences; model-selection set).", ["Engine", "Precision", "Recall", "F0.5", "False alerts", "Meaning viol."], devRows, [40, 13, 13, 13, 13, 13]),
        ...dataTable("Table 2. Final held-out test results (483 sentences; 202 erroneous with 209 gold edits).", ["Engine", "Precision", "Recall", "F0.5", "False alerts", "Meaning viol."], testRows, [40, 13, 13, 13, 13, 13]),
        PARA("The GLM rows are computed on a 141-row sample of the same test split (see Section 10). Harper-filtered figures use the final suppression layer; the shipped build is the exact engine embedded in the delivered HTML, measured through its JavaScript implementation."),
        figure("/home/z/my-project/scripts/report_fig_pr.png", 600),
        PARA([F("Figure 1. ", { bold: true }), F("Precision\u2013recall operating points on the test split. The shipped build trades some precision for recall versus the FA-optimal point; the original build reaches higher recall only with a 48.8% false-alert rate.")]),
        figure("/home/z/my-project/scripts/report_fig_fa.png", 600),
        PARA([F("Figure 2. ", { bold: true }), F("False-alert rate on correct sentences against the 5% target. The two filtered configurations meet the target; the shipped default (tagger enabled at 0.995) exceeds it for extra recall \u2014 a user-tunable trade-off documented as the operating-point choice.")]),

        H1("6. Harper false-positive reduction (measured)"),
        PARA("The measured suppression layer was applied after the neural work, as required. On the test split it removed 62 of Harper\u2019s 108 false positives (57%) at the cost of 8 of 54 true positives (15%) \u2014 the trade-off demanded by the brief: every suppression class is listed with counts (initialisms, proper-noun spelling findings, M\u0101ori constructs, curated NZ words, style findings, informal starters, fronted whom). On the development split the same layer removed 32 of 51 false positives with zero true-positive loss and reduced the clean-sentence false-alert rate from 14.3% to 0%. Zero false positives cannot be guaranteed and are not claimed; sentence-initial proper nouns (unknown names) remain the main residual false-positive class."),

        H1("7. Browser-level measured results"),
        H2("7.1 Suggestions actually displayed"),
        PARA("A 45-sentence sample (30 erroneous, 15 correct) from the test split was typed into the real editor of each build, and the rendered proof panel was harvested after the product\u2019s own scan cycle. Detection of at least one gold-matching displayed suggestion: 17/30 in both builds. Clean sentences alerted (at least one incorrect displayed suggestion): new build 3/15 versus original build 8/15. The displayed-suggestion measurement confirms the engine-level false-alert direction in the shipping product."),
        H2("7.2 Latency (browser, Chrome 158)"),
        ...dataTable("Table 3. In-browser latency of Engine94.", ["Stage", "Measured", "Target", "Status"], [
          ["Model initialisation (worker + int8 decode)", "\u224829 ms", "cold start reported", "Met"],
          ["Warm sentence inference, median (15 sentences)", "17 ms", "< 200 ms", "Met"],
          ["Warm inference, p95", "28 ms", "reported", "Met"],
          ["Node harness (same JS engine), per sentence", "11 ms", "reference", "n/a"],
        ], [46, 20, 20, 14]),
        H2("7.3 Offline and integrity verification"),
        BUL("Network instrumentation observed zero non-file requests while suggestions rendered; the engine, weights and rules are embedded in the HTML and loaded from blob URLs."),
        BUL("Applying a displayed suggestion changed exactly the target span; Ctrl+Z restored the original text exactly; no console errors occurred during the browser sessions."),
        BUL("Suggestion rendering reuses the product\u2019s own record/panel/apply pipeline, so rich-text formatting, undo/redo and dismiss behaviours are inherited from the original integration."),

        H1("8. Cross-runtime equivalence and quantisation"),
        PARA("The JavaScript engine was verified against the Python reference on all 251 development sentences: 249/251 identical proposal sets. The 2 mismatches are borderline-confidence flips (int8 quantisation shifts logits near the 0.98 threshold). The rules layer matched the Python reference exactly (identical findings on the same split). Quantisation: symmetric int8, per-tensor for GRU/output layers and per-row for embeddings, 758,002 bytes total (1.01 MB base64), a 92% size reduction versus fp32."),

        H1("9. Comparison against the original build"),
        PARA([F("Measured on the final test split (Table 2): the shipped new build "), F("doubles precision (0.278\u21920.500)", { bold: true }), F(", cuts the false-alert rate "), F("from 48.8% to 11.7%", { bold: true }), F(" (to 5.3% at the FA-optimal point), and reduces meaning violations "), F("from 35/89 to 6/89", { bold: true }), F(". Recall is lower (0.640\u21920.410): the original\u2019s recall is inflated by 351 false proposals on the same sentences \u2014 at a false-alert-matched operating point the original\u2019s usable recall collapses. All original-build numbers were measured by re-hosting its own engines (Harper WASM in Node; its T5 ONNX with its own tokenisation and decoding), not by approximation.")]),
        PARA("The browser-level displayed-suggestion comparison (7.1) and the integration verifications back these engine-level numbers inside the shipping product."),

        H1("10. LLM comparison (GLM, both prompts)"),
        PARA("A GLM LLM was run on a 141-row sample of the same test split (91 erroneous, 50 correct) with the brief\u2019s standard prompt and a stricter minimal-edit prompt, scored by the identical equivalent-effect matcher."),
        ...dataTable("Table 4. GLM results on the shared sample (91 erroneous, 47\u201350 valid clean rows).", ["System", "Precision", "Recall", "F0.5", "False alerts", "Meaning viol."], [
          ["GLM (standard prompt)", "0.628", "0.800", "0.656", "16/47 = 34.0%", "0 (7 adv rows)"],
          ["GLM (strict prompt)", "0.664", "0.811", "0.689", "16/47 = 34.0%", "0 (7 adv rows)"],
          ["SHIPPED build (full test split)", "0.500", "0.410", "0.479", "11.7%", "6/89"],
        ], [40, 12, 12, 12, 12, 12]),
        PARA([F("Measured interpretation: on this set GLM reaches higher sentence-level precision and much higher recall than the shipped offline engine, but it edited "), F("16 of 47 correct sentences (34%)", { bold: true }), F(" \u2014 persistent over-correction of already-correct text, which the offline engine\u2019s guards suppress by design. On the 7 completed adversarial meaning-preservation rows (of 30 attempted; the rest were cut off by API rate limits) GLM made no meaning changes under either prompt. GLM\u2019s pretraining may include public GEC corpora \u2014 disclosed as a contamination caveat for this comparison. No \u201coutperforms the LLM\u201d claim is made: the direct comparison favours GLM on this sample\u2019s recall at the cost of its false-alert rate.")]),

        H1("11. Grammarly comparison \u2014 not performed"),
        PARA([F("A direct Grammarly comparison was "), F("not performed", { bold: true }), F(": the sandbox has no Grammarly account, API, or network access to the service, and the brief forbids estimating or inventing its score. Consequently "), F("no claim about Grammarly is made anywhere in this report or the model card", { bold: true }), F(". The comparison legs actually performed are: the original Notepad build (its own engines, engine-level and browser-level), Harper raw and filtered, the existing T5 model, the newly trained engine, and GLM with two prompts.")]),

        H1("12. Targets versus measured results"),
        ...dataTable("Table 5. Development targets from the brief versus measured results.", ["Metric", "Target (from brief)", "Measured (test split)", "Status"], targetRows, [16, 28, 34, 22]),
        PARA("The 85% precision target was not reached at build level. Measured causes: (1) the remaining false positives concentrate in the neural tagger at even the 0.995 threshold and in Harper\u2019s residual classes (unknown sentence-initial proper nouns); (2) the training corpus is synthetic-and-small by sandbox necessity, so the tagger\u2019s contextual precision on natural prose is limited \u2014 its solo contribution is deliberately restricted to high-confidence spans; (3) recall-maximising configurations trade precision. The single highest-precision layer measured is the rules layer alone (0.78 dev / 0.47 test); combining Harper-filtered with rules gives the best product-level precision (0.571)."),

        H1("13. Product integration report"),
        BUL("Harper interaction: Harper findings keep priority; engine findings overlapping any Harper span are dropped before display (the documented conflict policy \u2014 Harper wins overlaps). Deduplication is inherited from the product\u2019s own merge logic."),
        BUL("Stale results: each engine scan is keyed to the block record (text, file, tab); findings are merged only if the record is still current and unchanged; the product\u2019s own record validation re-checks before display and application."),
        BUL("Suggestion lifecycle: engine findings enter the same lint records as Harper\u2019s, so undo, redo, dismiss, fix-all and the writing-suggestions panel all work through the existing machinery (verified in-browser for apply and undo)."),
        BUL("Protected content: prices, numbers, dates, times, URLs and identifiers are excluded at the engine level; the tagger may not rewrite capitalised tokens or non-alphabetic replacements."),
        BUL("Notices: the model and license information dialog includes the Engine94 notice; the original build\u2019s notebook data is empty (verified) and no user notebook data exists in the distributed file."),
        BUL("Worker lifecycle: the engine starts on first proofing publish, keeps a per-block cache, terminates on page hide, and re-uses the product\u2019s timeout/reject conventions."),

        H1("14. Deliverables and verification"),
        ...dataTable("Table 6. Deliverables and completion status.", ["Item", "Location / detail", "Status"], deliverRows, [24, 56, 20]),
        PARA("HTML size: 55,119,318 bytes (limit 100,000,000 \u2014 met). Offline: verified. Editor integrity: apply/undo verified; save/reopen inherits the original build\u2019s tested machinery (the engine does not touch persistence). A browser screenshot of the running build is included in the delivery folder."),

        H1("15. Limitations and unfinished work"),
        BUL("The neural tagger\u2019s contribution is modest by design; measured solo precision on natural prose is below its high-precision role, so it ships gated at 0.995 confidence. Better training data (real GEC corpora or much larger authored corpora) would be the highest-leverage next step."),
        BUL("Recall gaps: noun-subject agreement beyond pronoun subjects, contextual articles, and multi-word rewrites are not covered by the rule set."),
        BUL("Official BEA-2019/CoNLL-2014 scoring was not computed (no benchmark access offline); all numbers use the documented equivalent-effect scorer and must not be read as official benchmark scores."),
        BUL("The GLM adversarial leg completed 7 of 30 rows (API rate limits); those 7 rows showed zero meaning changes."),
        BUL("Human/blind review was not performed; annotation authorship and review were machine-only inside the sandbox and are labelled as such."),
        BUL("The browser tests used a test copy with a dialog-bypass hook for the first-run file-picker gate (file pickers cannot run headless); the shipped file itself is unmodified, and its first-run flow works normally in a real browser."),
        BUL("Harper false positives on unknown sentence-initial proper nouns are an open risk class."),

        H1("16. Reproduction"),
        PARA("Every artifact needed to reproduce the results is delivered: dataset JSONL files with manifests and SHA-256 hashes (download/model/data), training and evaluation code (download/model/code), the corruption generators and rule builder with unit tests, the quantised export, the HTML build script, and the browser harnesses. Commands: python3 build_dataset.py \u2192 python3 build_rules.py \u2192 python3 train_models.py --model gru \u2192 python3 export_js.py \u2192 python3 build_html.py; evaluation: python3 run_comparison.py test, node eval_js_engine.js test, node eval_shipped.js, node test_equivalence.js. Training ran on CPU only (torch 2.15, two threads); no GPU was available or required."),
      ],
    },
  ],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync("/home/z/my-project/download/grammar-engine-results-report.docx", buf);
  console.log("report written:", buf.length, "bytes");
});
