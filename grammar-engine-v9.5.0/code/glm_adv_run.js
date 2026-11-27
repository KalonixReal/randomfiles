// GLM LLM comparison on the test split with two prompts (per brief §6.2).
// Sample: 100 error sentences + 50 clean/adversarial sentences.
const fs = require('fs');
const path = require('path');

const PROMPTS = {
  standard: `Correct only clear grammatical errors. Preserve the original meaning, spelling variety, tone, names, numbers, negation, and formatting. Make the fewest necessary edits. If the sentence is already acceptable, return it unchanged.`,
  strict: `You are a high-precision grammar checker. Fix ONLY unambiguous grammatical errors (agreement, verb forms, missing or duplicated short words, clear homophones, missing apostrophes, clear articles, capitalisation of the first word and the pronoun "I"). RULES: (1) Make the smallest possible edit; never rewrite phrasing. (2) Do not change meaning, negation, modal choice, numbers, dates, names, quantities, technical terms, or the English variety (keep UK/NZ spellings such as colour, behaviour). (3) If the sentence is already grammatical or the correction is uncertain, return the sentence UNCHANGED. (4) Output ONLY the corrected sentence, nothing else.`,
};

async function runGLM() {
  const ZAI = (await import('z-ai-web-dev-sdk')).default;
  const zai = await ZAI.create();

  const items = fs.readFileSync(path.join(__dirname, 'data_built', 'test.jsonl'), 'utf8')
    .split('\n').filter(x => x.trim()).map(JSON.parse);
  const errs = []; // adversarial-only run
  const cleans = items.filter(x => x.origin === 'adversarial').slice(0, 30);
  const sample = [...errs, ...cleans];

  let out = [];
  try {
    out = JSON.parse(fs.readFileSync(path.join(__dirname, 'export_out', 'glm_comparison.json'), 'utf8'));
  } catch (e) { out = []; }
  const valid = new Set(out.filter(r => !String(r.results.standard).startsWith('ERROR')
    && !String(r.results.strict).startsWith('ERROR')).map(r => r.text));
  let pending = sample.filter(it => !valid.has(it.text));
  console.log('pending:', pending.length);
  const sleep = (ms) => new Promise(r => setTimeout(r, ms));
  for (const it of pending) {
    const row = { text: it.text, edits: it.edits, origin: it.origin || '', results: {} };
    for (const [pName, pText] of Object.entries(PROMPTS)) {
      let corrected = '';
      for (let attempt = 0; attempt < 4; attempt++) {
        try {
          const completion = await zai.chat.completions.create({
            messages: [
              { role: 'assistant', content: pText },
              { role: 'user', content: it.text },
            ],
            thinking: { type: 'disabled' },
          });
          corrected = (completion.choices[0]?.message?.content || '').trim();
          break;
        } catch (e) {
          const msg = String(e.message || e);
          if (attempt === 3) corrected = 'ERROR: ' + msg.slice(0, 120);
          await sleep(msg.includes('429') ? (3000 * (attempt + 1)) : 2000);
        }
      }
      row.results[pName] = corrected;
      await sleep(1200);
    }
    // replace any prior partial row
    const idx = out.findIndex(r => r.text === it.text);
    if (idx >= 0) out[idx] = row; else out.push(row);
    fs.writeFileSync(path.join(__dirname, 'export_out', 'glm_comparison.json'), JSON.stringify(out, null, 1));
    await sleep(800);
  }
  console.log('done', out.length, 'valid:', out.filter(r => !String(r.results.standard).startsWith('ERROR')).length);
}
process.on('unhandledRejection', (r) => { console.error('UNHANDLED', String(r).slice(0, 100)); });
runGLM().catch(e => { console.error('FATAL', String(e).slice(0, 200)); });
