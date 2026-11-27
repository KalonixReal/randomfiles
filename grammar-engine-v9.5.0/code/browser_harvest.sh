#!/bin/bash
# Browser-level displayed-suggestion harvest.
# Usage: bash browser_harvest.sh <html-file> <sentence-jsonl> <out.json>
# For each sentence: type it into the real editor, wait for the scan,
# read the rendered proof-panel list (the suggestions Notepad actually displays).
set -u
HTML="$1"
IN="$2"
OUT="$3"
PORT=8123
cd /home/z/my-project

agent-browser open "file://$HTML" > /dev/null 2>&1
agent-browser wait 5000
agent-browser press Escape > /dev/null 2>&1
agent-browser wait 1500

RESULT="["; FIRST=1
n=0
while IFS= read -r line; do
  text=$(printf '%s' "$line" | python3 -c "import sys,json; print(json.dumps(json.load(sys.stdin)['text']))")
  n=$((n+1))
  agent-browser eval "(() => { const ed = document.getElementById('editor'); ed.focus({preventScroll:true}); const p = ed.querySelector('p'); p.textContent = $text; const r = document.createRange(); r.selectNodeContents(p); r.collapse(false); getSelection().removeAllRanges(); getSelection().addRange(r); ed.dispatchEvent(new KeyboardEvent('keydown', {key: 'a', bubbles: true})); ed.dispatchEvent(new InputEvent('input', {bubbles: true, inputType: 'insertText'})); const rail = document.querySelector('#proofPanel933 .proof-rail933'); if (rail && document.getElementById('proofPanel933').classList.contains('collapsed')) rail.click(); return 'ok'; })()" > /dev/null 2>&1
  sleep 3
  RES=$(agent-browser eval "(() => { const list = document.querySelector('#proofPanel933 .proof-list933'); const items = list ? [...list.querySelectorAll('.proof-card-apply933, button')].map(b => b.textContent.trim()).filter(t => t && !/^Dismiss/.test(t)) : []; const marks = [...document.querySelectorAll('#harperProofLayer85 i')].map(x => x.className); return JSON.stringify({items, marks}); })()" 2>/dev/null | head -1)
  if [ -z "$RES" ] || [ "$RES" = "null" ]; then RES='{"items":[],"marks":[]}'; fi
  if [ "$FIRST" = "1" ]; then FIRST=0; else RESULT="$RESULT,"; fi
  RESULT="$RESULT{\"text\":$text,\"displayed\":$RES}"
done < "$IN"
RESULT="$RESULT]"
echo "$RESULT" > "$OUT"
echo "harvested $n sentences -> $OUT"
agent-browser close > /dev/null 2>&1
