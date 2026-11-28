# -*- coding: utf-8 -*-
"""Builds notepad-v9.5.0-grammar.html from the original v9.3.4 build.

Engine94 v2 becomes the sole grammar/proof source (measured: Harper adds no
unique TPs on dev/calib while adding unique FPs; see report). The suggestion
panel is re-skinned as a Grammarly-style assistant:

  1. Script blocks: engine94Data (JSON), engine94Rules (rules2 JSON),
     engine94Weights (base64 int8), engine94Worker (worker JS).
  2. App patch after LocalGrammar933:
     - Engine94 worker client (start/lint/scan with caches)
     - publishProof933 wrapped: record.lints REPLACED by Engine94 findings
     - renderProofPanel933 replaced by the Grammarly-style renderer
       (score ring, category chips, cards with Accept/Dismiss, stats footer)
     - CSS injected for the new panel look
  3. Updated model/license notice.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, "..", "work"))
SRC = os.path.join(WORK, "notepad-v9.3.4.html")
OUT = os.path.abspath(os.path.join(HERE, "..", "download", "notepad-v9.5.0-grammar.html"))

data = json.load(open(os.path.join(HERE, "export_out", "engine94_data.json")))
rules = json.load(open(os.path.join(HERE, "export_out", "engine94_rules.json")))
weights_b64 = open(os.path.join(HERE, "export_out", "engine94_weights.b64")).read().strip()
worker_js = open(os.path.join(HERE, "engine94.js")).read()

NOTICE = ("Notepad Grammar Engine 94 v2 (this build): 110 deterministic English "
          "grammar rules plus a distilled compact GRU edit tagger (int8-quantised, "
          "~1.4 MB) trained offline for this project, with protected-span and "
          "meaning-preservation guards. Engine findings replace the embedded "
          "Harper/T5 proofing layers in this build (measured decision, see the "
          "project report). Trained on synthetic rule-generated corruptions plus "
          "authored natural sentences prepared for this project; no user notebook "
          "data was used for training. Engine code, rules, vocabulary and "
          "quantised weights are embedded in this file and run entirely offline "
          "in your browser. License: MIT (engine code and trained weights "
          "released for this project). Evaluation report and model card: see the "
          "project report.")

CSS = r"""
<style id="g94Style">
#proofContents933{display:flex;flex-direction:column;min-height:0;flex:1;padding:0}
#proofContents933 > header, #proofContents933 .proof-filters933,
#proofContents933 .proof-summary933, #proofContents933 .proof-list933{display:none !important}
#proofPanel933{--g94-green:#147d64;--g94-red:#e5484d;--g94-blue:#0957c7;
  --g94-amber:#d98207;--g94-purple:#7c3aed;--g94-ink:#1f2430;--g94-mute:#6b7280;
  --g94-bg:#ffffff;--g94-soft:#f6f7f9;--g94-line:#e8e9ed}
.g94-root{display:flex;flex-direction:column;flex:1;min-height:0;overflow:hidden;
  background:var(--g94-bg);color:var(--g94-ink);font:13px/1.45 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.g94-head{display:flex;gap:12px;align-items:center;padding:14px 14px 10px;border-bottom:1px solid var(--g94-line)}
.g94-ring{flex:0 0 62px;width:62px;height:62px;border-radius:50%;display:grid;place-items:center;position:relative}
.g94-ring svg{position:absolute;inset:0;transform:rotate(-90deg)}
.g94-ring .num{font:700 17px/1 system-ui,sans-serif}
.g94-ring .lbl{font:600 8px/1 system-ui,sans-serif;color:var(--g94-mute);letter-spacing:.4px;margin-top:2px}
.g94-hsum{flex:1;min-width:0}
.g94-hsum .t{font:700 15px/1.2 inherit}
.g94-hsum .s{color:var(--g94-mute);font-size:12px;margin-top:3px}
.g94-fixall{border:0;background:var(--g94-green);color:#fff;border-radius:999px;
  padding:7px 12px;font:700 12px/1 system-ui,sans-serif;cursor:pointer}
.g94-fixall:disabled{background:#b9d6cd;cursor:default}
.g94-chips{display:flex;gap:6px;padding:10px 14px;border-bottom:1px solid var(--g94-line);
  flex-wrap:wrap}
.g94-chip{border:1px solid var(--g94-line);background:#fff;border-radius:999px;
  padding:5px 10px;font:600 11px/1 system-ui,sans-serif;color:var(--g94-mute);cursor:pointer}
.g94-chip .n{color:var(--g94-ink);font-weight:800;margin-left:4px}
.g94-chip.on{background:var(--g94-ink);border-color:var(--g94-ink);color:#fff}
.g94-chip.on .n{color:#fff}
.g94-list{flex:1;overflow-y:auto;padding:8px 10px 14px}
.g94-card{border:1px solid var(--g94-line);border-left:4px solid var(--g94-red);
  border-radius:10px;background:#fff;padding:10px 12px;margin:0 0 10px;cursor:pointer;
  transition:box-shadow .15s ease}
.g94-card:hover{box-shadow:0 4px 16px rgba(31,36,48,.09)}
.g94-card[data-cat="spelling"]{border-left-color:var(--g94-blue)}
.g94-card[data-cat="punctuation"]{border-left-color:var(--g94-amber)}
.g94-card[data-cat="grammar"]{border-left-color:var(--g94-red)}
.g94-cat{display:flex;align-items:center;gap:6px;font:700 10px/1 system-ui,sans-serif;
  text-transform:uppercase;letter-spacing:.6px;color:var(--g94-mute);margin-bottom:7px}
.g94-cat .dot{width:7px;height:7px;border-radius:50%;background:var(--g94-red)}
.g94-card[data-cat="spelling"] .dot{background:var(--g94-blue)}
.g94-card[data-cat="punctuation"] .dot{background:var(--g94-amber)}
.g94-line{display:flex;align-items:center;flex-wrap:wrap;gap:6px}
.g94-bad{color:var(--g94-red);font-weight:700}
.g94-good{color:var(--g94-green);font-weight:800}
.g94-msg{color:var(--g94-mute);font-size:11.5px;margin-top:6px}
.g94-accept{margin-left:auto;border:0;background:var(--g94-green);color:#fff;
  border-radius:999px;padding:6px 12px;font:700 12px/1 system-ui,sans-serif;cursor:pointer;
  white-space:nowrap}
.g94-accept:hover{background:#0f6a54}
.g94-ghost{border:0;background:transparent;color:var(--g94-mute);border-radius:6px;
  padding:4px 8px;font:600 11px/1 system-ui,sans-serif;cursor:pointer}
.g94-ghost:hover{background:var(--g94-soft);color:var(--g94-ink)}
.g94-foot{display:flex;gap:14px;padding:9px 14px;border-top:1px solid var(--g94-line);
  color:var(--g94-mute);font-size:11px;flex-wrap:wrap}
.g94-clean{display:flex;flex-direction:column;align-items:center;gap:12px;
  padding:46px 18px;text-align:center}
.g94-clean .ok{width:64px;height:64px;border-radius:50%;background:#e7f4ef;
  display:grid;place-items:center}
.g94-clean .ok svg{width:30px;height:30px}
.g94-clean .t{font:800 15px/1.3 inherit}
.g94-clean .s{color:var(--g94-mute);font-size:12px}
.g94-more{width:100%;border:1px dashed var(--g94-line);background:#fff;color:var(--g94-mute);
  border-radius:8px;padding:8px;font:600 12px/1 system-ui,sans-serif;cursor:pointer}
.g94-scan{padding:22px 16px;color:var(--g94-mute);font-size:12px}
</style>
"""

APP_PATCH = r"""
/* ---- Engine94 v2: sole grammar engine + Grammarly-style suggestion panel ---- */
const Engine94=(()=>{let worker=null,startup=null,sequence=0;const pending=new Map;
function stop(){try{worker?.terminate()}catch(e){}worker=null;startup=null;for(const item of pending.values()){clearTimeout(item.timer);item.reject(Error("Grammar engine stopped"))}pending.clear()}
function start(){if(startup)return startup;let target;
try{const dataBlock=document.getElementById("engine94Data").textContent;
const weights=document.getElementById("engine94Weights").textContent.trim();
const rulesBlock=document.getElementById("engine94Rules").textContent;
const workerSrc=document.getElementById("engine94Worker").textContent;
const code="const W94_DATA="+dataBlock+";\nconst W94_RULES="+rulesBlock+";\nconst W94_WEIGHTS_B64="+JSON.stringify(weights)+";\n"+workerSrc;
const url=URL.createObjectURL(new Blob([code],{type:"text/javascript"}));
target=worker=new Worker(url);URL.revokeObjectURL(url)}catch(error){stop();throw error}
target.onmessage=({data:d})=>{const item=pending.get(d.id);if(!item)return;clearTimeout(item.timer);pending.delete(d.id);d.error?item.reject(Error(d.error)):item.resolve(d.result)};
target.onerror=()=>{if(worker===target)stop()};
startup=(async()=>{await send("init","");return target})().catch(error=>{if(worker===target)stop();throw error});
return startup}
function send(type,text){const target=worker;if(!target)return Promise.reject(Error("Grammar engine not started"));
return new Promise((resolve,reject)=>{const id=++sequence;pending.set(id,{resolve:resolve,reject:reject,timer:setTimeout(()=>{pending.delete(id);reject(Error("The grammar engine timed out"))},9e3)});try{target.postMessage({id:id,type:type,text:text})}catch(error){pending.delete(id);reject(error)}})}
async function lint(text){await start();return await send("lint",text)}
const cache94=new WeakMap;
async function scan(record){const cached=cache94.get(record.block);
if(cached&&cached.text===record.text&&cached.file===record.file&&cached.tab===record.tab)return cached.findings;
let findings=[];try{findings=await lint(record.text)}catch(error){return[]}
cache94.set(record.block,{text:record.text,file:record.file,tab:record.tab,findings:findings});
return findings}
window.addEventListener("pagehide",()=>stop());
return{lint:lint,scan:scan,stop:stop}})();
/* Engine94 replaces the proofing lints (measured decision; see report). */
const publishProof933Original933=publishProof933;
publishProof933=function(record){
if(!record||!liveProof933()||!record.text||record.text.length>4e3){if(record){record.lints=[];publishProof933Original933(record)}return}
const block=record.block,text=record.text;
if(record.__engine94){publishProof933Original933(record);return}
Engine94.scan(record).then(findings=>{
const current=harperCache85.get(block);
if(!current||current!==record||!validProseRecord85(record)||current.text!==text)return;
record.lints=Array.isArray(findings)?findings.slice():[];
record.__engine94=true;
publishProof933Original933(record);
paintHarperView85()}).catch(()=>{record.lints=[];publishProof933Original933(record)})};
/* ---- Grammarly-style panel renderer ---- */
const g94Labels={grammar:"Grammar",spelling:"Spelling",punctuation:"Punctuation"};
const g94Colors={grammar:"#e5484d",spelling:"#0957c7",punctuation:"#d98207"};
let g94Filter="all",g94Limit=40,g94Built=false;
function g94Cat(lint){const t=lint.type94||"";if(t==="spelling")return"spelling";if(t==="punct"||t==="punctuation"||t==="negation")return"punctuation";return"grammar"}
function g94Build(){if(g94Built)return;g94Built=true;
const host=document.getElementById("proofContents933");if(!host)return;
const root=document.createElement("div");root.className="g94-root";root.id="g94Root";
root.innerHTML=`
<div class="g94-head">
  <div class="g94-ring"><svg width="62" height="62" viewBox="0 0 62 62">
    <circle cx="31" cy="31" r="27" fill="none" stroke="#e8e9ed" stroke-width="6"/>
    <circle id="g94RingArc" cx="31" cy="31" r="27" fill="none" stroke="#2ca06c" stroke-width="6"
      stroke-linecap="round" stroke-dasharray="169.6" stroke-dashoffset="169.6"/>
  </svg><div><div class="num" id="g94Score">–</div><div class="lbl">SCORE</div></div></div>
  <div class="g94-hsum"><div class="t" id="g94SumTitle">Checking…</div><div class="s" id="g94SumSub"></div></div>
  <button class="g94-fixall" id="g94FixAll" type="button">Fix all</button>
</div>
<div class="g94-chips" id="g94Chips"></div>
<div class="g94-list" id="g94List"></div>
<div class="g94-foot" id="g94Foot"></div>`;
host.appendChild(root);
root.querySelector("#g94FixAll").onclick=()=>{try{fixProofTab933()}catch(e){}}}
function g94Items(){
const prefs=proofPrefs84(),grammar=prefs.grammar!==false;
const enabled=proofPanelEnabled933(),ready=proofTabReady933();
const items=[];const counts={all:0,grammar:0,spelling:0,punctuation:0};
if(enabled&&proofPresented933){
const records=[...proofPanelRecords933.values()].filter(record=>harperCache85.get(record.block)===record&&currentProseOwner85(record));
records.sort((a,b)=>a.block.compareDocumentPosition(b.block)&Node.DOCUMENT_POSITION_FOLLOWING?-1:1);
for(const record of records){for(const lint of record.lints.slice().sort((a,b)=>a.start-b.start)){
const decoration=lintDecoration85(lint,grammar);if(!decoration)continue;
if(!lint.suggestions?.length)continue;
const cat=g94Cat(lint);counts.all++;counts[cat]++;
items.push({record:record,lint:lint,cat:cat})}}}
return{enabled:enabled,ready:ready,items:items,counts:counts}}
function g94Words(){try{const txt=(editor.innerText||"").trim();return txt?txt.split(/\s+/).filter(Boolean).length:0}catch(e){return 0}}
function g94Score(words,issues){if(!words)return 100;const density=issues/words;
return Math.max(0,Math.min(100,Math.round(100*Math.exp(-3.5*density))))}
function renderPanelG94(){
g94Build();const root=document.getElementById("g94Root");if(!root)return;
const{enabled,ready,items,counts}=g94Items();
const words=g94Words();
const score=g94Score(words,counts.all);
const scoreEl=document.getElementById("g94Score");if(scoreEl)scoreEl.textContent=String(score);
const arc=document.getElementById("g94RingArc");
if(arc){const C=2*Math.PI*27;arc.style.strokeDashoffset=String(C*(1-score/100));
arc.setAttribute("stroke",score>=90?"#2ca06c":score>=70?"#f5a623":"#e5484d")}
const title=document.getElementById("g94SumTitle");
const sub=document.getElementById("g94SumSub");
if(!enabled){title.textContent="Suggestions unavailable here";sub.textContent=""}
else if(!ready){title.textContent="Checking this tab…";sub.textContent="Running Engine94"}
else{title.textContent=counts.all===0?"Looks good!":"Writing score";
sub.textContent=counts.all===0?"No writing issues found":counts.all+(counts.all===1?" issue":" issues")+" found in this tab"}
const fixBtn=document.getElementById("g94FixAll");
if(fixBtn)fixBtn.disabled=!ready||counts.all===0;
const chips=document.getElementById("g94Chips");
if(chips){chips.innerHTML="";
const defs=[["all","All"],["grammar","Grammar"],["spelling","Spelling"],["punctuation","Punctuation"]];
for(const[key,label]of defs){
const b=document.createElement("button");b.type="button";b.className="g94-chip"+(g94Filter===key?" on":"");
b.innerHTML=label+'<span class="n">'+counts[key]+"</span>";
b.onclick=()=>{g94Filter=key;renderPanelG94()};chips.appendChild(b)}}
const list=document.getElementById("g94List");
if(list){list.innerHTML="";
if(!enabled){list.innerHTML='<div class="g94-scan">Writing suggestions are unavailable here.</div>'}
else if(!ready){list.innerHTML='<div class="g94-scan">Checking this tab…</div>'}
else if(!counts.all){
list.innerHTML=`<div class="g94-clean"><div class="ok"><svg viewBox="0 0 24 24" fill="none">
<circle cx="12" cy="12" r="11" fill="#2ca06c"/><path d="M6.5 12.5l3.5 3.5 7-8" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
<div class="t">No writing issues found</div><div class="s">Engine94 checked ${words} words</div></div>`}
else{
const shown=items.filter(it=>g94Filter==="all"||it.cat===g94Filter).slice(0,g94Limit);
let n=0;
for(const{record:record,lint:lint,cat:cat}of shown){
n++;
const replacement=lint.suggestions&&lint.suggestions[0]!==undefined?lint.suggestions[0]:"";
const card=document.createElement("article");card.className="g94-card";card.dataset.cat=cat;
const catRow=document.createElement("div");catRow.className="g94-cat";
catRow.innerHTML='<span class="dot"></span>'+(g94Labels[cat]||"Grammar");
const line=document.createElement("div");line.className="g94-line";
const bad=document.createElement("span");bad.className="g94-bad";bad.textContent=lint.problem||"";
const good=document.createElement("span");good.className="g94-good";
good.textContent=replacement!==""?String(replacement):"(remove)";
const arrow=document.createElement("span");arrow.textContent="→";arrow.style.color="#9aa1ad";
line.append(bad,arrow,good);
const accept=document.createElement("button");accept.type="button";accept.className="g94-accept";
accept.textContent=replacement!==""?"Use "+String(replacement).slice(0,18):"Remove";
accept.onclick=(e)=>{e.stopPropagation();if(applyLiveProof933(record,lint,replacement))editor.focus({preventScroll:true})};
line.appendChild(accept);
const msg=document.createElement("div");msg.className="g94-msg";msg.textContent=lint.message||"";
const actions=document.createElement("div");actions.className="g94-msg";
const dismiss=document.createElement("button");dismiss.type="button";dismiss.className="g94-ghost";dismiss.textContent="Dismiss";
dismiss.onclick=(e)=>{e.stopPropagation();if(currentProofCard933(record,lint))dismissLiveProof933(record,lint)};
const dismissAll=document.createElement("button");dismissAll.type="button";dismissAll.className="g94-ghost";dismissAll.textContent="Dismiss all";
dismissAll.onclick=(e)=>{e.stopPropagation();dismissProofOccurrences933(record,lint)};
actions.append(dismiss,dismissAll);
if(cat==="spelling"){const add=document.createElement("button");add.type="button";add.className="g94-ghost";add.textContent="Add to dictionary";add.onclick=(e)=>{e.stopPropagation();addProofWord933(record,lint)};actions.appendChild(add)}
card.onclick=()=>{if(!validProseRecord85(record))return;
const target=proseTarget85(record,lint.start,lint.end);if(!target)return;
record.block.scrollIntoView({block:"center",inline:"nearest"});
editor.focus({preventScroll:true});
const selection=getSelection();selection.removeAllRanges();selection.addRange(target.range)};
card.append(catRow,line,msg,actions);list.appendChild(card)}
const total=g94Filter==="all"?counts.all:counts[g94Filter];
if(total>shown.length){const more=document.createElement("button");more.type="button";more.className="g94-more";more.textContent="Show "+(total-shown.length)+" more";more.onclick=()=>{g94Limit+=40;renderPanelG94()};list.appendChild(more)}}}
const foot=document.getElementById("g94Foot");
if(foot){const sentences=Math.max(1,Math.round(words/18));const minutes=Math.max(1,Math.round(words/200));
foot.innerHTML="<span>"+words+" words</span><span>"+sentences+" sentences</span><span>~"+minutes+" min read</span><span>Engine94 · offline</span>"}}
const renderProofPanel933OriginalG94=renderProofPanel933;
renderProofPanel933=function(){try{renderPanelG94()}catch(e){try{renderProofPanel933OriginalG94()}catch(_){}}};
"""


def main():
    s = open(SRC, "r", encoding="utf-8").read()

    # 0) inject CSS before </head>
    assert s.count("</head>") == 1
    s = s.replace("</head>", CSS + "\n</head>", 1)

    # 1) script blocks after harperLicense85
    m = re.search(r'<script type="text/plain" id="harperLicense85">.*?</script>', s, re.S)
    assert m, "harperLicense85 anchor missing"
    blocks = (
        '<script type="application/json" id="engine94Data">'
        + json.dumps(data, separators=(",", ":"))
        + '</script>\n'
        + '<script type="application/json" id="engine94Rules">'
        + json.dumps(rules, separators=(",", ":"))
        + '</script>\n'
        + '<script type="application/octet-stream" id="engine94Weights">'
        + weights_b64 + '</script>\n'
        + '<script type="text/plain" id="engine94Worker">'
        + worker_js.replace("</script", "<\\/script") + '</script>\n'
    )
    s = s[:m.end()] + "\n" + blocks + s[m.end():]

    # 2) app patch after LocalGrammar933 definition
    anchor = 'window.addEventListener("pagehide",()=>stop());return{correct:correct,stop:stop}})();'
    assert s.count(anchor) == 1
    s = s.replace(anchor, anchor + APP_PATCH)

    # 3) notices
    m = re.search(r'<script type="application/json" id="proof933-notices">(.*?)</script>', s, re.S)
    notices = json.loads(m.group(1).strip())
    notices = notices + [NOTICE]
    s = s.replace(m.group(0),
                   '<script type="application/json" id="proof933-notices">'
                   + json.dumps(notices, separators=(",", ":")) + "</script>")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(s)
    size = os.path.getsize(OUT)
    print(f"built {OUT}: {size:,} bytes ({size/1e6:.1f} MB)")
    assert size < 100_000_000, "size limit exceeded"
    return OUT


if __name__ == "__main__":
    main()
