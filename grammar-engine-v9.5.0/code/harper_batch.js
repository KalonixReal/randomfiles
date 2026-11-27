// Batch Harper runner: reads JSONL {id, text, language} from stdin, writes
// JSONL {id, findings} to stdout. Reuses the harper_node harness.
const path = require('path');
const readline = require('readline');

async function main() {
  const harper = require('./harper_node.js');
  await harper.init();
  const rl = readline.createInterface({ input: process.stdin });
  for await (const line of rl) {
    if (!line.trim()) continue;
    const { id, text, language, personal } = JSON.parse(line);
    try {
      const findings = await harper.ask('lint', text, language || 'US', personal || []);
      process.stdout.write(JSON.stringify({ id, findings }) + '\n');
    } catch (e) {
      process.stdout.write(JSON.stringify({ id, error: String(e.message || e) }) + '\n');
    }
  }
}
main().catch(e => { console.error(e); process.exit(1); });
