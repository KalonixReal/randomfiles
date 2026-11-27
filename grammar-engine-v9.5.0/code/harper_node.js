// Node harness for the original build's Harper engine.
// Simulates the Web Worker environment that harperWorker85 expects.
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const W = path.resolve(__dirname, '../work');
const glueSrc = fs.readFileSync(path.join(W, 'harper_library.js'), 'utf8');
const html = fs.readFileSync(path.join(W, 'notepad-v9.3.4.html'), 'utf8');

function extractBlock(id) {
  const re = new RegExp('<script[^>]*id="' + id + '"[^>]*>([\\s\\S]*?)</script>');
  const m = html.match(re);
  if (!m) throw new Error('block not found: ' + id);
  return m[1].trim();
}

const archive = extractBlock('harperWasm85');
const forgivingAtob = (s) => atob(String(s).replace(/\s+/g, ''));

// blob URL shim
let blobCounter = 0;
const blobStore = new Map();
function createObjectURL(blob) {
  const url = 'blob:node/' + (++blobCounter);
  blobStore.set(url, blob);
  return url;
}
function revokeObjectURL(url) { blobStore.delete(url); }

const responseShim = (bytes) => ({
  ok: true,
  type: 'basic',
  url: 'blob:node/x',
  status: 200,
  headers: { get: (h) => h.toLowerCase() === 'content-type' ? 'application/wasm' : '' },
  arrayBuffer: async () => bytes,
});

const realFetch = globalThis.fetch;
async function fetchShim(input, init) {
  const url = typeof input === 'string' ? input : (input && input.url) || String(input);
  if (blobStore.has(url)) {
    const blob = blobStore.get(url);
    const bytes = blob.__bytes || new Uint8Array(await blob.arrayBuffer());
    return new Response(bytes, { status: 200, headers: { 'Content-Type': 'application/wasm' } });
  }
  return realFetch(input, init);
}

const sandbox = {
  console,
  TextDecoder, TextEncoder,
  atob: forgivingAtob, btoa,
  URL, Blob, Response, Request, Headers,
  fetch: fetchShim,
  performance: { now: () => Date.now() },
  crypto: { getRandomValues: (a) => { require('crypto').webcrypto.getRandomValues(a); return a; } },
  setTimeout, clearTimeout, Promise,
};
sandbox.globalThis = sandbox;
sandbox.self = sandbox;
sandbox.self.URL = URL;
// URL.createObjectURL shim inside sandbox
const sandboxURL = new Function('u', 'return new URL(u)'); // unused
sandbox.URL = URL;
try { if (!URL.createObjectURL) { URL.createObjectURL = createObjectURL; URL.revokeObjectURL = revokeObjectURL; } } catch (e) {}
// Direct property shims (some libs read self.URL.createObjectURL)
sandbox.createObjectURL = createObjectURL;
const ctx = vm.createContext(sandbox);
// Provide URL class with createObjectURL in the sandbox
vm.runInContext(`
  if (typeof URL !== 'undefined' && !URL.createObjectURL) {
    Object.defineProperty(URL, 'createObjectURL', { value: ${createObjectURL.toString()} });
    Object.defineProperty(URL, 'revokeObjectURL', { value: ${revokeObjectURL.toString()} });
  }
`, ctx);

vm.runInContext(glueSrc, ctx, { filename: 'harper_library.js' });

// --- worker message pump ---
const pending = new Map();
let seq = 0;
sandbox.postMessage = (data) => {
  if (data && data.id !== undefined && pending.has(data.id)) {
    const res = pending.get(data.id);
    pending.delete(data.id);
    res(data);
  } else if (data === 'ready') {
    module.exports._ready = true;
  }
};

async function ask(type, text, language, personal, extra) {
  const id = ++seq;
  return new Promise((resolve, reject) => {
    pending.set(id, (data) => {
      if (data.error) reject(new Error(data.error));
      else resolve(data.result);
    });
    sandbox.onmessage({ data: { id, type, text, language: language || 'US', personal: personal || [], ...extra } });
  });
}

async function init() {
  const result = await ask('init', '', 'US', [], { archive });
  return result;
}

module.exports = { sandbox, ask, init, extractBlock };

if (require.main === module) {
  (async () => {
    const t0 = Date.now();
    const r = await init();
    console.log('init:', JSON.stringify(r), `(${Date.now() - t0}ms)`);
    const t1 = Date.now();
    const lints = await ask('lint', 'She walk to school everyday and recieve good grades.', 'US', []);
    console.log('lint time:', Date.now() - t1, 'ms');
    console.log(JSON.stringify(lints, null, 1));
    const t2 = Date.now();
    const l2 = await ask('lint', 'The team have completed they report on colour usage.', 'GB', []);
    console.log('lint2 time:', Date.now() - t2, 'ms');
    console.log(JSON.stringify(l2, null, 1).slice(0, 1500));
    const t3 = Date.now();
    const l3 = await ask('lint', 'This sentence is entirely correct and needs no correction at all.', 'US', []);
    console.log('clean time:', Date.now() - t3, 'ms, lints:', JSON.stringify(l3));
  })();
}
