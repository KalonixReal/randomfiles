#!/bin/bash
# Browser-level displayed-suggestion harvest v2: clears the editor before each
# sentence so no stale cards from previous/default content survive.
# Usage: bash browser_harvest2.sh <html-file> <sentence-jsonl> <out.json>
set -u
HTML="$1"
IN="$2"
OUT="$3"

agent-browser open "file://$HTML" > /dev/null 2>&1
agent-browser wait 6000 > /dev/null 2>&1
agent-browser press Escape > /dev/null 2>&1
agent-browser wait 1500 > /dev/null 2>&1
# make sure the panel is expanded and spell/grammar enabled
agent-browser eval "(() => { const rail = document.querySelector('#proofPanel933 .proof-rail933'); if (rail && document.getElementById('proofPanel933').classList.contains('collapsed')) rail.click(); return 'ok'; })()" > /dev/null 2>&1

RESULT="["; FIRST=1
n=0
while IFS= read -r line; do
  text=$(printf '%s' "$line" | python3 -c "import sys,json; print(json.dumps(json.load(sys.stdin)['text']))")
  n=$((n+1))
  # clear the whole document first
  agent-browser eval "(() => { const ed = document.getElementById('editor'); ed.focus(); document.execCommand('selectAll', false, null); document.execCommand('delete', false, null); ed.dispatchEvent(new InputEvent('input', {bubbles:true, inputType:'deleteContentBackward'})); return 'cleared'; })()" > /dev/null 2>&1
  sleep 1
  agent-browser eval "(() => { const ed = document.getElementById('editor'); ed.focus({preventScroll:true}); let p = ed.querySelector('p'); if (!p) { p = document.createElement('p'); ed.appendChild(p); } p.textContent = $text; const r = document.createRange(); r.selectNodeContents(p); r.collapse(false); getSelection().removeAllRanges(); getSelection().addRange(r); ed.dispatchEvent(new KeyboardEvent('keydown', {key: 'a', bubbles: true})); ed.dispatchEvent(new InputEvent('input', {bubbles: true, inputType: 'insertText'})); return 'ok'; })()" > /dev/null 2>&1
  sleep 4
  RES=$(agent-browser eval "(() => { const list = document.querySelector('#proofPanel933 .proof-list933'); const cards = list ? [...list.querySelectorAll('.proof-card933')].map(c => c.textContent.replace(/\s+/g,' ').slice(0,110)) : []; const status = document.querySelector('#proofPanel933 .proof-status933'); return JSON.stringify({cards, status: status ? status.textContent : null}); })()" 2>/dev/null | head -1)
  if [ -z "$RES" ] || [ "$RES" = "null" ]; then RES='{"cards":[],"status":null}'; fi
  if [ "$FIRST" = "1" ]; then FIRST=0; else RESULT="$RESULT,"; fi
  RESULT="$RESULT{\"text\":$text,\"displayed\":$RES}"
done < "$IN"
RESULT="$RESULT]"
printf '%s' "$RESULT" > "$OUT"
echo "harvested $n sentences -> $OUT"
