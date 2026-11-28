// Patient GLM runner: sequential, slow pacing, long backoff on 429, resumable.
// usage: node glm_patient.js <in.jsonl> <out.jsonl> <promptId(minimal|careful)>
import fs from 'fs';

const [inPath, outPath, promptId] = process.argv.slice(2);
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
const mk = PROMPTS[promptId];
if (!mk) { console.error('bad promptId'); process.exit(1); }

const rows = fs.readFileSync(inPath, 'utf8').trim().split('\n').map(l => JSON.parse(l));
const done = new Set();
if (fs.existsSync(outPath)) {
  for (const line of fs.readFileSync(outPath, 'utf8').trim().split('\n')) {
    if (!line) continue;
    try { done.add(JSON.parse(line).idx); } catch {}
  }
}
console.log(`rows=${rows.length} done=${done.size} prompt=${promptId}`);
const out = fs.createWriteStream(outPath, { flags: 'a' });
const sleep = ms => new Promise(r => setTimeout(r, ms));

let idx = 0;
let consec429 = 0;
while (idx < rows.length) {
  if (done.has(idx)) { idx++; continue; }
  const row = rows[idx];
  const { system, user } = mk(row.s_bad);
  try {
    const res = await zai.chat.completions.create({
      messages: [{ role: 'system', content: system }, { role: 'user', content: user }],
      thinking: { type: 'disabled' }
    });
    const content = res.choices[0].message.content?.trim() ?? '';
    out.write(JSON.stringify({ idx, prompt: promptId, ok: true, out: content }) + '\n');
    done.add(idx);
    idx++;
    consec429 = 0;
    await sleep(1200); // gentle pacing
  } catch (e) {
    const is429 = String(e).includes('429') || String(e).includes('Too many');
    consec429++;
    const wait = is429 ? Math.min(300000, 20000 * consec429) : 8000;
    console.log(`err idx=${idx} 429=${is429} wait=${wait}ms consec=${consec429}`);
    await sleep(wait);
  }
}
console.log('COMPLETE', promptId);
