// engine94.js — self-contained grammar engine for Notepad (rules + trained GRU tagger).
// Runs in a Web Worker; findings emitted in the Harper lint format so the
// existing proofing UI renders and applies them unchanged.
//
// This file is the single source of truth for the JS side; the Python harness
// (scripts/engine.py) implements the same semantics and is cross-checked by
// the equivalence test (test_equivalence.js).
//
// W94_DATA and W94_WEIGHTS_B64 are injected at build time.

const W94 = (() => {
  const TOKEN_RE = /[A-Za-z0-9]+(?:'[A-Za-z0-9]+)*|[.,!?;:"()$£€%]/g;
  const PROTECT_RE = /\$[\d,.]+|\b\d[\d,.]*\b|\b\d{1,2}:\d{2}\b|https?:\/\/\S+|[\w.+-]+@[\w-]+\.[A-Za-z]+|\b(?:19|20)\d{2}\b|\b[A-Z]{2,}\d+\b/g;
  const THRESH = W94_DATA.threshold || 0.98;

  function tokenize(text) {
    const out = [];
    let m;
    TOKEN_RE.lastIndex = 0;
    while ((m = TOKEN_RE.exec(text))) out.push(m[0]);
    return out;
  }

  function tokenizeWithOffsets(text) {
    const out = [];
    let m;
    TOKEN_RE.lastIndex = 0;
    while ((m = TOKEN_RE.exec(text))) out.push([m[0], m.index, m.index + m[0].length]);
    return out;
  }

  function hashLight(s) {
    let h = 5381;
    for (let i = 0; i < s.length; i++) h = ((h << 5) + h + s.charCodeAt(i)) & 0xffffffff;
    return (h >>> 0) % 1000003;
  }

  // ---- weights
  let WEIGHTS = null;

  function loadWeights() {
    const raw = atob(W94_WEIGHTS_B64);
    const bytes = new Uint8Array(raw.length);
    for (let i = 0; i < raw.length; i++) bytes[i] = raw.charCodeAt(i);
    WEIGHTS = {};
    for (const [name, meta] of Object.entries(W94_DATA.weights)) {
      WEIGHTS[name] = {
        q: new Int8Array(bytes.buffer, meta.off, meta.n),
        shape: meta.shape,
        scale: meta.scale,
        scales: meta.scales,
      };
    }
  }

  function matvecRowwise(q, scales, x) {
    // q: int8 [rows, cols] flattened; scales: per-row; x: Float64Array cols
    const rows = scales.length, cols = x.length;
    const out = new Float64Array(rows);
    for (let r = 0; r < rows; r++) {
      let acc = 0;
      const base = r * cols;
      const s = scales[r];
      for (let c = 0; c < cols; c++) acc += q[base + c] * x[c];
      out[r] = acc * s;
    }
    return out;
  }

  function matvecTensor(q, scale, wRows, wCols, x, out) {
    const outRows = wCols;
    for (let c = 0; c < outRows; c++) out[c] = 0;
    for (let r = 0; r < wRows; r++) {
      const wq = q[r * wCols + 0]; // unused
    }
    // x @ W^T : out[j] = sum_i x[i] * W[j,i]
    for (let j = 0; j < outRows; j++) {
      let acc = 0;
      const base = j * wCols;
      for (let i = 0; i < wCols; i++) acc += q[base + i] * x[i];
      out[j] = acc * scale;
    }
    return out;
  }

  // featurize: returns array of [wid, hsuf, hpre] with <s>/</s> markers
  function featurize(text) {
    const toks = tokenize(text);
    const full = ["<s>", ...toks, "</s>"];
    const feats = [];
    for (const t of full) {
      if (t === "<s>") feats.push([W94_DATA.words["<s>"] || 2, 0, 0]);
      else if (t === "</s>") feats.push([W94_DATA.words["</s>"] || 3, 0, 0]);
      else {
        const wl = t.toLowerCase();
        const wid = W94_DATA.words[wl] !== undefined ? W94_DATA.words[wl] : 1;
        const suf = wl.slice(-4), pre = wl.slice(0, 3);
        feats.push([wid, suf ? hashLight(suf) & 4095 : 0, pre ? hashLight(pre) & 4095 : 0]);
      }
    }
    return { feats, toks, full };
  }

  function shapeFlags(tok) {
    if (!tok || tok === "<s>") return [0, 0, 0, 0, 0, 1, 0, 0];
    if (tok === "</s>") return [0, 0, 0, 0, 0, 0, 0, 1];
    const caps = /[A-Z]/.test(tok[0]);
    const allcaps = tok.length > 1 && tok === tok.toUpperCase() && caps;
    let hasDigit = false;
    for (const ch of tok) if (ch >= "0" && ch <= "9") { hasDigit = true; break; }
    const isPunct = /^[.,!?;:"()$£€%]$/.test(tok);
    const ln = Math.min(tok.length, 12) / 12;
    return [caps ? 1 : 0, allcaps ? 1 : 0, hasDigit ? 1 : 0, isPunct ? 1 : 0, ln, 0, 0, 0];
  }

  let __lastX = null;
  let __lastFeats = null;
  let __lastOut = null;

  function forward(text) {
    const { feats, toks, full } = featurize(text);
    __lastFeats = feats;
    const T = feats.length;
    const we = WEIGHTS.word_emb, hs = WEIGHTS.hash_suf, hp = WEIGHTS.hash_pre;
    const D = we.shape[1];
    const x = new Float64Array(T * 96);
    // embeddings + hash + shape, then proj
    const tmp = new Float64Array(88);
    const projW = WEIGHTS.proj_w, projB = WEIGHTS.proj_b;
    const projScale = projW.scale;
    const H = 96;
    for (let t = 0; t < T; t++) {
      const [wid, s1, p1] = feats[t];
      const rowOff = wid * D;
      const wS = we.scales[wid];
      for (let d = 0; d < D; d++) tmp[d] = we.q[rowOff + d] * wS;
      for (let d = 0; d < 8; d++) tmp[D + d] = hs.q[s1 * 8 + d] * hs.scales[s1];
      for (let d = 0; d < 8; d++) tmp[D + 8 + d] = hp.q[p1 * 8 + d] * hp.scales[p1];
      const sf = shapeFlags(full[t]);
      for (let d = 0; d < 8; d++) tmp[80 + d] = sf[d];
      // proj: 96 x 88
      for (let j = 0; j < H; j++) {
        let acc = 0;
        const base = j * 88;
        for (let i = 0; i < 88; i++) acc += projW.q[base + i] * tmp[i];
        x[t * H + j] = acc * projScale + projB.q[j] * projB.scale;
      }
    }
    // GRU bidirectional: torch layout w_ih [3H, IN], w_hh [3H, H]; gates order r,z,n
    const IN = WEIGHTS.gru_w_ih.shape[1];
    const G = WEIGHTS.gru_w_ih.shape[0];
    const HS = G / 3; // hidden size
    const out = new Float64Array(T * (2 * HS));
    for (const rev of [false, true]) {
      const wI = rev ? WEIGHTS.gru_w_ih_r : WEIGHTS.gru_w_ih;
      const wH = rev ? WEIGHTS.gru_w_hh_r : WEIGHTS.gru_w_hh;
      const bI = rev ? WEIGHTS.gru_b_ih_r : WEIGHTS.gru_b_ih;
      const bH = rev ? WEIGHTS.gru_b_hh_r : WEIGHTS.gru_b_hh;
      const h = new Float64Array(HS);
      const gi = new Float64Array(G), gh = new Float64Array(G);
      for (let step = 0; step < T; step++) {
        const t = rev ? T - 1 - step : step;
        // gates: gi = Wih x + bih ; gh = Whh h + bhh
        for (let g = 0; g < G; g++) {
          let acc = 0;
          const base = g * IN;
          for (let i = 0; i < IN; i++) acc += wI.q[base + i] * x[t * H + i];
          gi[g] = acc * wI.scale + bI.q[g] * bI.scale;
        }
        for (let g = 0; g < G; g++) {
          let acc = 0;
          const base = g * HS;
          for (let i = 0; i < HS; i++) acc += wH.q[base + i] * h[i];
          gh[g] = acc * wH.scale + bH.q[g] * bH.scale;
        }
        // torch GRU: r,z sigmoid gates; n = tanh(Win x + bin + r*(W hn h + bhn))
        for (let i = 0; i < HS; i++) {
          const r = sig(gi[i] + gh[i]);
          const z = sig(gi[HS + i] + gh[HS + i]);
          const n = Math.tanh(gi[2 * HS + i] + r * gh[2 * HS + i]);
          h[i] = (1 - z) * n + z * h[i];
        }
        for (let i = 0; i < HS; i++) out[t * 2 * HS + (rev ? HS : 0) + i] = h[i];
      }
    }
    // output layer: edits
    const ow = WEIGHTS.out_w, ob = WEIGHTS.out_b;
    const V = ow.shape[0];
    const OW = ow.shape[1]; // 2 * HS
    const logits = new Float64Array(T * V);
    for (let t = 0; t < T; t++) {
      for (let v = 0; v < V; v++) {
        let acc = 0;
        const base = v * OW;
        for (let i = 0; i < OW; i++) acc += ow.q[base + i] * out[t * OW + i];
        logits[t * V + v] = acc * ow.scale + ob.q[v] * ob.scale;
      }
    }
    __lastX = x; __lastOut = out;
    return { logits, T, V, toks, full };
  }

  function sig(x) { return 1 / (1 + Math.exp(-x)); }

  function xFloatSub(x, a, b) { return x.slice(a, b); }

  // ---- rules engine (mirrors engine.py rules_findings; rules2 kinds supported)
  function guardPasses(rule, mm, text) {
    const guard = rule.guard;
    if (!guard) return true;
    if (guard.end && !text.trimEnd().endsWith(guard.end)) return false;
    if (guard.not_group && mm[guard.not_group] &&
        guard.words.map(w => w.toLowerCase()).includes(mm[guard.not_group].toLowerCase())) return false;
    if (guard.no_plural && mm[rule.apply.group || 1] && mm[rule.apply.group || 1].endsWith("s")) return false;
    if (guard.no_camel && mm[guard.no_camel] && /[A-Z]/.test(String(mm[guard.no_camel]).slice(1))) return false;
    if (guard.first_in && mm[0].split(" ")[0].toLowerCase() !== "") {
      if (guard.first_in.map(w => w.toLowerCase()).includes(mm[0].split(" ")[0].toLowerCase())) return false;
    }
    if (guard.min_words && text.trim().split(/\s+/).length < guard.min_words) return false;
    if (guard.prev_not && mm.index > 0) {
      const DETS = "my|our|their|his|her|its|your|the|a|an|this|that|these|those|all|some|both|several|many|few|most|other|such|each|any|no|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|hundred|thousand";
      const pnSet = guard.prev_not.map(w => w.toLowerCase());
      const pm2 = text.slice(0, mm.index).match(/([A-Za-z]+)\s*$/);
      const pm1 = text.slice(0, mm.index).match(new RegExp("([A-Za-z]+)\\s+(?:" + DETS + ")\\s*$", "i"));
      if (pm2 && pnSet.includes(pm2[1].toLowerCase())) return false;
      if (pm1 && pnSet.includes(pm1[1].toLowerCase())) return false;
    }
    const prChecks = [["prev_re", false], ["prev_not_re", true]];
    for (const [gk, mustNot] of prChecks) {
      const pr = guard[gk];
      if (!pr) continue;
      const reStr = typeof pr === "string" ? pr : pr.re;
      const window = typeof pr === "string" ? (guard.window || 50) : (pr.window || (gk === "prev_re" ? 50 : 30));
      const seg = text.slice(Math.max(0, mm.index - window), mm.index);
      let hit = false;
      try { hit = new RegExp(reStr, "i").test(seg); } catch (e) { hit = false; }
      if (mustNot ? hit : !hit) return false;
    }
    return true;
  }

  function groupSpan(mm, g) {
    if (mm.indices && mm.indices[g]) return [mm.indices[g][0], mm.indices[g][1]];
    const before = mm[0].indexOf(mm[g]);
    const off = before >= 0 ? before : 0;
    return [mm.index + off, mm.index + off + mm[g].length];
  }

  const titleLike = s => s.split(" ").map(w => w[0].toUpperCase() + w.slice(1)).join(" ");

  function rulesFindings(text) {
    const out = [];
    const prot = [];
    let m;
    PROTECT_RE.lastIndex = 0;
    while ((m = PROTECT_RE.exec(text))) prot.push([m.index, m.index + m[0].length]);
    for (const rule of W94_RULES.rules) {
      const flags = (rule.case === "i" ? "gi" : "g") + "d";
      let re;
      try { re = new RegExp(rule.re, flags); } catch (e) { re = new RegExp(rule.re, flags.slice(0, -1)); }
      let mm;
      while ((mm = re.exec(text))) {
        const g = rule.apply.group || 0;
        if (!guardPasses(rule, mm, text)) {
          if (re.lastIndex === mm.index) re.lastIndex++;
          continue;
        }
        let gs = mm.index, ge = mm.index + mm[0].length;
        if (g) { const sp = groupSpan(mm, g); gs = sp[0]; ge = sp[1]; }
        if (prot.some(p => gs < p[1] && p[0] < ge)) {
          if (re.lastIndex === mm.index) re.lastIndex++;
          continue;
        }
        const kind = rule.apply.kind;
        let rep = null, span = [gs, ge];
        if (kind === "map") {
          const key = mm[g];
          const mp = rule.apply.map;
          rep = mp[key];
          if (rep === undefined && /^[a-z]/.test(key)) rep = mp[keyCap(key)];
          if (rep === undefined && /^[A-Z]/.test(key)) {
            const low = mp[key.toLowerCase()];
            rep = low !== undefined ? titleLike(low) : undefined;
          }
          if (rep === undefined) { if (re.lastIndex === mm.index) re.lastIndex++; continue; }
          if (rep === mm[g]) { if (re.lastIndex === mm.index) re.lastIndex++; continue; } // no-op self-map
        } else if (kind === "rep") {
          rep = rule.apply.text;
        } else if (kind === "template") {
          rep = String(rule.apply.template || "").replace(/\{(\d)\}/g, (_, d) => (mm[+d] || ""));
          span = [mm.index, mm.index + mm[0].length];
        } else if (kind === "g_ing") {
          const wg = String(mm[g]);
          // drop a single trailing 'e' (but never 'ee'): receive -> receiving
          rep = (wg.length > 2 && wg.endsWith("e") && !wg.endsWith("ee")) ? wg.slice(0, -1) + "ing" : wg + "ing";
        } else if (kind === "del_next") {
          const e2 = ge < text.length && text[ge] === " " ? ge + 1 : ge;
          span = [gs, e2];
          rep = "";
        } else if (kind === "period_end") {
          if (!text.trim() || !/^[A-Z]/.test(text.trim())) { if (re.lastIndex === mm.index) re.lastIndex++; continue; }
          const e = text.replace(/\s+$/, "").length;
          span = [e, e];
          rep = ".";
        } else if (kind === "capfirst") {
          span = [mm.index, mm.index + 1]; rep = text[0].toUpperCase();
        } else if (kind === "dup") {
          const w = mm[0];
          span = [mm.index + Math.floor(w.length / 2), mm.index + w.length];
          rep = "";
        } else if (kind === "suffix_ing") {
          rep = mm[0] + "ing";
        } else if (kind === "swap") {
          const tk = mm[0].split(" ");
          rep = tk[0] + " " + tk[2] + " " + tk[1];
        }
        if (rep === null) { if (re.lastIndex === mm.index) re.lastIndex++; continue; }
        out.push({ start: span[0], end: span[1], rep, type: rule.type, src: "rule:" + rule.id });
        if (re.lastIndex === mm.index) re.lastIndex++;
      }
    }
    out.sort((a, b) => a.start - b.start || a.end - b.end);
    const kept = [];
    for (const f of out) {
      if (kept.some(k => f.start < k.end && k.start < f.end)) continue;
      kept.push(f);
    }
    return kept;
  }

  const keyCap = s => s[0].toUpperCase() + s.slice(1);

  // ---- tagger decode (mirrors engine.py tagger_findings)
  function taggerFindings(text, thresh) {
    let cur = text;
    const fb = W94_DATA.fallback || {};
    for (let pass = 0; pass < 2; pass++) {
      const { logits, T, V, toks } = forward(cur);
      const withOff = tokenizeWithOffsets(cur);
      const ops = [];
      let edited = false;
      const prot = [];
      let m;
      PROTECT_RE.lastIndex = 0;
      while ((m = PROTECT_RE.exec(cur))) prot.push([m.index, m.index + m[0].length]);
      for (let i = 1; i <= withOff.length; i++) {
        // softmax over row
        let maxv = -Infinity, maxid = 0;
        for (let v = 0; v < V; v++) { const val = logits[i * V + v]; if (val > maxv) { maxv = val; maxid = v; } }
        let sum = 0;
        for (let v = 0; v < V; v++) sum += Math.exp(logits[i * V + v] - maxv);
        const p = 1 / sum;
        if (p < thresh) continue;
        const tag = W94_DATA.edits[maxid];
        if (tag === "$KEEP") continue;
        const [tok, ts, te] = withOff[i - 1];
        if (prot.some(pr => ts < pr[1] && pr[0] < te)) continue;
        if (tag === "$DELETE") {
          let e2 = te, s2 = ts;
          if (e2 < cur.length && cur[e2] === " ") e2++;
          else if (s2 > 0 && cur[s2 - 1] === " ") s2--;
          ops.push([s2, e2, ""]); edited = true;
        } else if (tag === "$CASE_CAP") {
          ops.push([ts, te, tok[0].toUpperCase() + tok.slice(1)]); edited = true;
        } else if (tag === "$REPLACE_OOV") {
          if (/^[A-Za-z']+$/.test(tok)) {
            const rep = fb[tok.toLowerCase()];
            if (rep && rep !== tok) { ops.push([ts, te, caseLike(tok, rep)]); edited = true; }
          }
        } else if (tag.startsWith("REPLACE_")) {
          ops.push([ts, te, caseLike(tok, tag.slice(8))]); edited = true;
        } else if (tag.startsWith("INSERT_")) {
          ops.push([ts, ts, tag.slice(7) + " "]); edited = true;
        } else if (tag.startsWith("APPEND_")) {
          const pos = te;
          const pad = (pos < cur.length && !" .,!?".includes(cur[pos])) ? " " : "";
          ops.push([pos, pos, tag.slice(7) + pad]); edited = true;
        }
      }
      if (!edited) break;
      let cur2 = cur;
      ops.sort((a, b) => b[0] - a[0]);
      for (const [s, e, r] of ops) cur2 = cur2.slice(0, s) + r + cur2.slice(e);
      if (cur2 === cur) break;
      cur = cur2;
    }
    if (cur === text) return [];
    return diffEdits(text, cur).map(([s, e, r]) => ({ start: s, end: e, rep: r, type: "tagger", src: "tagger" }));
  }

  function caseLike(src, rep) {
    if (/[A-Z]/.test(src[0]) && /[a-z]/.test(rep[0])) return rep[0].toUpperCase() + rep.slice(1);
    return rep;
  }

  // token-aligned diff (mirrors corrupt.py diff_edits)
  function diffEdits(a, b) {
    const ta = [], tb = [];
    let m;
    TOKEN_RE.lastIndex = 0;
    while ((m = TOKEN_RE.exec(a))) ta.push([m[0], m.index, m.index + m[0].length]);
    TOKEN_RE.lastIndex = 0;
    while ((m = TOKEN_RE.exec(b))) tb.push([m[0], m.index, m.index + m[0].length]);
    const wa = ta.map(x => x[0]), wb = tb.map(x => x[0]);
    // simple LCS-based opcodes
    const ops = diffSeq(wa, wb);
    const out = [];
    for (const [tag, i1, i2, j1, j2] of ops) {
      if (tag === "equal") continue;
      if (tag === "replace") {
        out.push([ta[i1][1], ta[i2 - 1][2], b.slice(tb[j1][1], tb[j2 - 1][2])]);
      } else if (tag === "delete") {
        let s = ta[i1][1], e = ta[i2 - 1][2];
        if (e < a.length && a[e] === " ") e++;
        else if (s > 0 && a[s - 1 === 0 ? 0 : s - 1] === " " && (e >= a.length || a[e] !== " ")) s--;
        out.push([s, e, ""]);
      } else if (tag === "insert") {
        const rep = b.slice(tb[j1][1], tb[j2 - 1][2]);
        let pos, r;
        if (i1 < ta.length) {
          pos = ta[i1][1];
          r = (pos === 0 || a[pos - 1] === " ") ? rep + " " : " " + rep + " ";
        } else {
          pos = a.length;
          r = (pos === 0 || a[pos - 1] !== " ") ? " " + rep : rep;
        }
        out.push([pos, pos, r]);
      }
    }
    return out;
  }

  function diffSeq(wa, wb) {
    // difflib-like SequenceMatcher opcodes (greedy LCS)
    const n = wa.length, m = wb.length;
    // classic LCS table (sentences are short)
    const dp = Array.from({ length: n + 1 }, () => new Uint16Array(m + 1));
    for (let i = n - 1; i >= 0; i--)
      for (let j = m - 1; j >= 0; j--)
        dp[i][j] = wa[i] === wb[j] ? dp[i + 1][j + 1] + 1 : Math.max(dp[i + 1][j], dp[i][j + 1]);
    const ops = [];
    let i = 0, j = 0;
    while (i < n && j < m) {
      if (wa[i] === wb[j]) { ops.push(["equal", i, i + 1, j, j + 1]); i++; j++; }
      else if (dp[i + 1][j] >= dp[i][j + 1]) i++;
      else j++;
    }
    // compress runs of non-equal
    const merged = [];
    for (const op of ops) {
      const last = merged[merged.length - 1];
      if (last && last[0] === "equal") merged.push(op);
      else if (last && last[0] !== "equal") { /* skip; handled below */ merged.push(op); }
      else merged.push(op);
    }
    // build opcodes properly: walk again and group
    const out = [];
    let i2 = 0, j2 = 0;
    while (i2 < n || j2 < m) {
      if (i2 < n && j2 < m && wa[i2] === wb[j2]) {
        const si = i2, sj = j2;
        while (i2 < n && j2 < m && wa[i2] === wb[j2]) { i2++; j2++; }
        out.push(["equal", si, i2, sj, j2]);
      } else {
        const si = i2, sj = j2;
        while ((i2 < n || j2 < m) && !(i2 < n && j2 < m && wa[i2] === wb[j2])) {
          if (i2 < n && j2 < m) {
            if (dp[i2 + 1][j2] >= dp[i2][j2 + 1]) i2++; else j2++;
          } else if (i2 < n) i2++;
          else j2++;
        }
        out.push([i2 > si && j2 > sj ? "replace" : (i2 > si ? "delete" : "insert"), si, i2, sj, j2]);
      }
    }
    return out;
  }

  // ---- messages
  const TYPE_MSG = {
    sva: "The verb does not agree with its subject.",
    verbform: "The verb form is not correct here.",
    participle: "Use the past participle after have/has/had.",
    modal: "Use the base form of the verb after a modal.",
    punct: "This contraction needs an apostrophe.",
    homophone: "A near-sounding word fits better here.",
    article: "Check the article before this word.",
    compar: "Double comparative.",
    plural: "This plural form is irregular.",
    agr: "The determiner does not match in number.",
    dup: "Repeated word.",
    capit: "Capitalisation.",
    inversion: "Question word order: auxiliary before subject.",
    preposition: "The preposition does not fit here.",
    advform: "This needs an adverb, not an adjective.",
    negation: "Double negative.",
    tense: "Check the verb tense.",
    missing: "A word seems to be missing here.",
    spelling: "Possible spelling mistake.",
    tagger: "Contextual grammar suggestion (neural model).",
    grammar: "Grammar",
    spelling2: "Spelling",
  };

  function toLint(f, text) {
    return {
      start: f.start, end: f.end,
      problem: text.slice(f.start, f.end),
      kind: f.type === "spelling" ? "spelling" : "grammar",
      category933: f.type === "spelling" ? "spelling" : "grammar",
      message: TYPE_MSG[f.type] || "Grammar suggestion.",
      rule: "Engine94:" + (f.src || f.type),
      type94: f.type,
      suggestions: [f.rep],
    };
  }

  function lint(text) {
    if (!WEIGHTS) loadWeights();
    const rules = rulesFindings(text).map(f => ({ ...f, kind: "grammar" }));
    let tagg = [];
    if (THRESH < 1) { try { tagg = taggerFindings(text, THRESH); } catch (e) { tagg = []; } }
    // cascade: tagger proposals that overlap rules are dropped
    const mine = [...rules];
    for (const f of tagg) {
      if (mine.some(o => f.start < o.end && o.start < f.end)) continue;
      mine.push(f);
    }
    // engine-level meaning guards: reject replacements that flip negation/numbers
    const safe = mine.filter(f => guard94(text, f) && (f.src !== "tagger" || /^[A-Za-z' ]*$/.test(f.rep || "")));
    return safe.map(f => toLint(f, text));
  }

  function guard94(text, f) {
    const orig = text.slice(f.start, f.end).toLowerCase();
    const rep = (f.rep || "").toLowerCase();
    const NEG = ["not", "no", "never", "cannot", "neither"];
    const oNeg = NEG.some(w => orig.includes(w)), rNeg = NEG.some(w => rep.includes(w));
    if (oNeg !== rNeg) return false;
    const oNum = (orig.match(/\d+/g) || []).join(), rNum = (rep.match(/\d+/g) || []).join();
    if (oNum !== rNum) return false;
    if (/[A-Z]/.test(text.slice(f.start, f.end)) && f.type === "tagger") {
      // tagger must not rewrite capitalised tokens (names)
      if (!/^[A-Z]/.test(f.rep || "")) return false;
    }
    return true;
  }

  return { lint, loadWeights, taggerFindings, rulesFindings, ensureLoaded: loadWeights, weights: () => WEIGHTS,
    forward: (t) => { const o = forward(t); return { T: o.T, V: o.V, logits: Array.from(o.logits) }; },
    dbg: () => ({ x: Array.from(__lastX || []), feats: __lastFeats, out: Array.from(__lastOut || []) }) };
})();

// worker protocol (matches Harper85.ask semantics)
self.onmessage = (e) => {
  const { id, type, text } = e.data;
  try {
    if (type === "init") {
      W94.loadWeights();
      postMessage({ id, result: { ready: true, version: "engine94-1.0" } });
      return;
    }
    const lints = W94.lint(text);
    postMessage({ id, result: lints });
  } catch (err) {
    postMessage({ id, error: String(err && err.message || err) });
  }
};
