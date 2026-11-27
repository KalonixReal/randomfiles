// GLM scoring runner: corrects each sentence with a given prompt, saves
// raw outputs. Robust: exponential backoff on 429/5xx, resume support.
// usage: node glm_score.js <in.jsonl> <out.jsonl> <promptId> [limit]
import fs from 'fs';

const [inPath, outPath, promptId, limitArg] = process.argv.slice(2);
const ZAI = (await import('z-ai-web-dev-sdk')).default;
const zai = await ZAI.create();

const PROMPTS = {
  minimal: (s) => ({
    system: 'You are a grammar correction tool. Correct grammatical, spelling and punctuation errors in the user text. Preserve meaning and style. Output ONLY the corrected text, nothing else.',
    user: s
  }),
  careful: (s) => ({
    system: 'You are a precise offline grammar checker. Fix ONLY clear grammar, spelling, punctuation and word-choice errors (e.g. subject-verb agreement, verb forms, articles, plurals, confusable words, missing apostrophes, capitalisation at sentence start, missing final punctuation, double negatives). Do NOT rephrase, do NOT change word order, do NOT add or remove content, do NOT change UK/US/NZ spelling variants of each other, keep names, numbers, dates and quotations exactly. If the text is already correct, output it unchanged. Output ONLY the corrected text, nothing else.',
    user: s
  })
};

const mkPrompt = PROMPTS[promptId];
if (!mkPrompt) { console.error('bad promptId'); process.exit(1); }

const rows = fs.readFileSync(inPath, 'utf8').trim().split('\n')
  .map(l => JSON.parse(l));
const limit = limitArg ? parseInt(limitArg, 10) : rows.length;

// resume: collect completed indices
const done = new Set();
if (fs.existsSync(outPath)) {
  for (const line of fs.readFileSync(outPath, 'utf8').trim().split('\n')) {
    if (!line) continue;
    try { done.add(JSON.parse(line).idx); } catch {}
  }
}
console.log(`rows=${rows.length} limit=${limit} alreadyDone=${done.size}`);

const out = fs.createWriteStream(outPath, { flags: 'a' });

const sleep = ms => new Promise(r => setTimeout(r, ms));

async function ask(idx, row) {
  const { system, user } = mkPrompt(row.s_bad);
  let attempt = 0;
  while (attempt < 9) {
    try {
      const res = await zai.chat.completions.create({
        messages: [
          { role: 'system', content: system },
          { role: 'user', content: user }
        ],
        thinking: { type: 'disabled' }
      });
      const content = res.choices[0].message.content?.trim() ?? '';
      out.write(JSON.stringify({ idx, prompt: promptId, ok: true, out: content }) + '\n');
      return true;
    } catch (e) {
      attempt++;
      const is429 = String(e).includes('429') || String(e).includes('Too many');
      const wait = Math.min(is429 ? 30000 : 8000, 2000 * Math.pow(1.7, attempt));
      if (attempt >= 5) {
        console.error(`idx ${idx} failed attempt ${attempt}: ${String(e).slice(0, 120)}`);
      }
      await sleep(wait);
    }
  }
  out.write(JSON.stringify({ idx, prompt: promptId, ok: false, out: '' }) + '\n');
  return false;
}

let n = 0, failures = 0;
const CONC = 3;
const queue = [];
for (let i = 0; i < Math.min(limit, rows.length); i++) {
  if (!done.has(i)) queue.push(i);
}
(async () => {
  let ptr = 0;
  async function worker(wid) {
    while (ptr < queue.length) {
      const i = queue[ptr++];
      const ok = await ask(i, rows[i]);
      n++;
      if (!ok) failures++;
      if (n % 25 === 0) console.log(`progress ${n}/${queue.length} failures=${failures}`);
    }
  }
  await Promise.all(Array.from({ length: CONC }, (_, w) => worker(w)));
  out.end();
  console.log(`DONE processed=${n} failures=${failures}`);
})();
