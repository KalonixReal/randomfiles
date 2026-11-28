# -*- coding: utf-8 -*-
"""Creates a TEST COPY of the shipped HTML with:
1. an auto-dismiss for the connect-notebook dialog (file pickers cannot run headless)
2. window.__npType(text) typing hook + window.__npSuggestions() reader
The shipped file is NOT modified; the test copy is used only for browser verification.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, "..", "download", "notepad-v9.5.0-grammar.html"))
TEST = os.path.abspath(os.path.join(HERE, "notepad-test-copy.html"))

HOOK = r"""
<script>
/* TEST HARNESS ONLY — not part of the shipped build. */
(function(){
  const dismissed = new WeakSet();
  const killDialogs = () => {
    document.querySelectorAll('[role=dialog]').forEach(d => {
      if (!dismissed.has(d) && d.offsetParent !== null) {
        const t = d.textContent || '';
        if (t.includes('Connect your notebook')) {
          dismissed.add(d);
          d.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape', keyCode: 27, bubbles: true}));
          setTimeout(() => { d.remove(); }, 60);
        }
      }
    });
  };
  new MutationObserver(() => killDialogs()).observe(document.body, {childList: true, subtree: true});
  setInterval(killDialogs, 900);
  window.__npType = (text) => {
    const ed = document.getElementById('editor');
    ed.focus({preventScroll: true});
    const sel = window.getSelection();
    sel.removeAllRanges();
    let node = ed.querySelector('p, h1, div') || ed;
    const r = document.createRange();
    r.selectNodeContents(node);
    r.collapse(false);
    sel.addRange(r);
    document.execCommand('insertText', false, text);
    return ed.textContent.slice(0, 120);
  };
  window.__npSuggestions = () => {
    const list = document.querySelector('#proofPanel933 .proof-list933');
    const items = list ? [...list.querySelectorAll('.proof-card-apply933, button')].map(b => b.textContent.trim()) : [];
    return JSON.stringify({text: (document.getElementById('editor') || {}).textContent || '',
                           panelText: list ? list.textContent.slice(0, 600) : '',
                           buttons: items.slice(0, 12)});
  };
  window.__npProofRecords = () => {
    // reach into the running app: last published record via the panel records map
    const panel = document.getElementById('proofPanel933');
    return JSON.stringify({list: document.querySelector('#proofPanel933 .proof-list933')?.children.length || 0});
  };
})();
</script>
"""

def main():
    s = open(SRC, encoding="utf-8").read()
    s = s.replace("</body>", HOOK + "\n</body>", 1) if "</body>" in s else s + HOOK
    open(TEST, "w", encoding="utf-8").write(s)
    print("test copy:", TEST, os.path.getsize(TEST), "bytes")


if __name__ == "__main__":
    main()
