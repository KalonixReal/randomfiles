// GLM as grammar checker on the FRESH comparison set — patient edition.
// Infinite retries with capped exponential backoff; resumable via output file.
// usage: nohup node glm_fresh_run.js > work/glm_fresh.log 2>&1 &
import fs from 'fs';

const IN = '/home/z/my-project/scripts/data_built/fresh.jsonl';
const OUT = '/home/z/my-project/scripts/work/glm_fresh_out.jsonl';
const ZAI = (await import('z-ai-web-dev-sdk')).default;
const zai = await ZAI.create();

const SYSTEM = 'You are a precise offline grammar checker. Fix ONLY clear grammar, spelling, punctuation and word-choice errors (e.g. subject-verb agreement, verb forms, articles, plurals, confusable words, missing apostrophes, capitalisation at sentence start, missing final punctuation, double negatives). Do NOT rephrase, do NOT change word order, do NOT add or remove content, do NOT change UK/US/NZ spelling variants of each other, keep names, numbers, dates and quotations exactly. If the text is already correct, output it unchanged. Output ONLY the corrected text, nothing else.';

const rows = fs.readFileSync(IN, 'utf8').trim().split('\n').map(l => JSON.parse(l));
const done = new Set();
if (fs.existsSync(OUT)) {
  for (const l of fs.readFileSync(OUT, 'utf8').trim().split('\n')) {
    if (l) done.add(JSON.parse(l).idx);
  }
}
console.log('rows:', rows.length, 'already done:', done.size, new Date().toISOString());

const sleep = ms => new Promise(r => setTimeout(r, ms));

async function callOne(text) {
  let delay = 30000;
  while (true) {
    try {
      const completion = await zai.chat.completions.create({
        messages: [
          { role: 'assistant', content: SYSTEM },
          { role: 'user', content: text }
        ],
        thinking: { type: 'disabled' }
      });
      const out = completion.choices[0]?.message?.content;
      if (out == null || !out.trim()) throw new Error('empty completion');
      return out.trim();
    } catch (e) {
      const msg = String(e && e.message || e);
      console.log('  retry in ' + Math.round(delay / 1000) + 's (' + msg.slice(0, 60) + ') ' + new Date().toISOString());
      await sleep(delay);
      delay = Math.min(delay * 2, 300000);
    }
  }
}

let i = -1;
for (const it of rows) {
  i++;
  if (done.has(i)) continue;
  const out = await callOne(it.text);
  fs.appendFileSync(OUT, JSON.stringify({ idx: i, text: it.text, edits: it.edits, genre: it.genre, glm: out }) + '\n');
  console.log('done ' + (i + 1) + '/' + rows.length + ' | ' + (out === it.text ? 'unchanged' : 'CHANGED'));
  await sleep(2500);
}
console.log('GLM fresh run complete: ' + OUT);
