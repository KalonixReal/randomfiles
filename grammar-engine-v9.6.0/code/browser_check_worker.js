// Standalone browser verification of the embedded Engine94 worker
// (injected via agent-browser eval as an IIFE string)
(() => new Promise((resolve) => {
  const dataBlock = document.getElementById('engine94Data').textContent;
  const weights = document.getElementById('engine94Weights').textContent.trim();
  const rulesBlock = document.getElementById('engine94Rules').textContent;
  const workerSrc = document.getElementById('engine94Worker').textContent;
  const code = 'const W94_DATA=' + dataBlock + ';const W94_RULES=' + rulesBlock +
    ';const W94_WEIGHTS_B64=' + JSON.stringify(weights) + ';\n' + workerSrc;
  const blob = new Blob([code], { type: 'text/javascript' });
  const w = new Worker(URL.createObjectURL(blob));
  const t0 = performance.now();
  let initMs = 0;
  w.onerror = (e) => resolve('WORKER-ERROR: ' + e.message);
  w.onmessage = ({ data: d }) => {
    if (d.id === 1) {
      initMs = Math.round(performance.now() - t0);
      w.postMessage({ id: 2, type: 'lint', text: 'My sister go to the library and she dont know a answer.' });
    } else if (d.id === 2) {
      const lintMs = Math.round(performance.now() - t0) - initMs;
      resolve(JSON.stringify({ initMs, lintMs, findings: d.result || d.error }));
    }
  };
  w.postMessage({ id: 1, type: 'init', text: '' });
  setTimeout(() => resolve('TIMEOUT'), 12000);
}))
