# -*- coding: utf-8 -*-
"""Builds the new single-file Notepad HTML (v9.4.0-grammar) from the original
v9.3.4 build by surgical insertion:

1. Three new script blocks: engine94Data (JSON), engine94Rules (JSON),
   engine94Weights (base64 int8) and engine94Worker (worker JS source).
2. App patch after the LocalGrammar933 module:
   - Engine94 worker client (start/lint/scan with stale-result guards)
   - wrap publishProof933 so every published Harper record is also scanned
     by Engine94 and non-overlapping findings are merged (Harper wins overlaps)
   - wrap Harper85.ask with the measured Harper false-positive filter
3. Model/license notice appended to proof933-notices.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, "..", "work"))
SRC = os.path.join(WORK, "notepad-v9.3.4.html")
OUT = os.path.abspath(os.path.join(HERE, "..", "download", "notepad-v9.4.0-grammar.html"))

data = json.load(open(os.path.join(HERE, "export_out", "engine94_data.json")))
rules = json.load(open(os.path.join(HERE, "export_out", "engine94_rules.json")))
weights_b64 = open(os.path.join(HERE, "export_out", "engine94_weights.b64")).read().strip()
worker_js = open(os.path.join(HERE, "engine94.js")).read()

NOTICE = ("Notepad Grammar Engine 94 (this build): deterministic English grammar rules, "
          "a distilled compact GRU edit-tagger (int8-quantised, ~0.76 MB) trained offline for "
          "this project, and a measured Harper false-positive suppression layer. "
          "Trained on synthetic rule-generated corruptions plus authored natural sentences "
          "prepared for this project; no user notebook data was used for training. "
          "Engine code, rules, vocabulary and quantised weights are embedded in this file and "
          "run entirely offline in your browser. License: MIT (engine code and trained weights "
          "released for this project). Evaluation report and model card: see the project report.")

# ---------- JS app patch ----------
APP_PATCH = r"""
/* ---- Engine94: trained grammar tagger + deterministic rules, alongside Harper ---- */
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
/* Wrap Harper85.ask with the measured false-positive suppression layer. */
const HarperAskOriginal85=Harper85.ask.bind(Harper85);
Harper85.ask=async function(type,text){const findings=await HarperAskOriginal85(type,text);
if(type!=="lint"||!Array.isArray(findings))return findings;
return harperFilter94(findings,text)};
function harperFilter94(findings,text){
const MAORI_DET=new Set(["Te","Ng\u0101","Nga","He","Ki","A","O","I","Na","Kein"]);
const NZ_WORDS=new Set(["hui","marae","waka","ama","kai","kaupapa","whanau","iwi","hapu","koha","korero","mihi","waiata","hangi","kumara","pavlova","tramping","tramp","jandals","togs","paddock","kauri","pohutukawa","rimu","tui","weka","kereru","weta","kina","tuatara","moa","Aotearoa","kainga","Whanganui","Rotorua","Taupo","Taranaki","Waikato","Northland","Coromandel","Wairarapa","Maramarua","Waihou","Ngaio","Kapiti","Hokitika","fitout","prizegiving","wetsuits","tamariki","rangatahi","kaumatua","wananga","whenua","moana","awa","maunga","rohe","kura","Matariki","Puanga","Tangaroa","Tamaki","Aroha","Anahera","Ihirangi","Hemi","Rewa","Tama","Sione","Mei","Amita","Srinivasan","Sandhu","Chandra","Fatima","Yusuf","Alvaro","Nadia","Kenji","Priya","Kofi","Ihaia","Selma","rostered","annum","relocks","relock","whaikorero","shoulda","yous","fiord","fiords","wether","heatpump","aeroengineer","Taup\u014d","\u0100pirana","Ng\u0101","M\u0101ori","Taup\u014d","Taupo","Apirana"]);
const INFORMAL_START=new Set(["we","them","yous","that","no","yeah","nah","hey","aye","im","ive","id","cant","wont","dont","doesnt","aint","gonna","wasnt","arent","wouldnt","couldnt","shouldnt","shes","hes","theyre","youre","lets","hows","whats","sweet","choice","true","fair","righto","wanna","kinda","dunno","gotta","lemme","gimme"]);
const out=[];let m;const tokRe=/[A-Za-z]+/g;const toks=[];while((m=tokRe.exec(text)))toks.push([m[0],m.index]);
for(const h of findings){const kind=(h.kind||"").toLowerCase();const rule=h.rule||"";
const frag=text.slice(h.start,h.end);
if(kind==="enhancement"||kind==="style"||kind==="miscellaneous")continue;
if(["spelling","typo","wordchoice"].includes(kind)&&/^[A-Z0-9]{2,6}$/.test(frag))continue;
if(kind==="capitalization"&&h.start===0){const rep=(h.suggestions&&h.suggestions[0])||"";
if(rep&&rep[0]===rep[0].toLowerCase()&&rep[0].toUpperCase()===rep[0])continue;
const first=text.slice(0,h.end).trim().split(" ")[0].toLowerCase();
if(INFORMAL_START.has(first))continue}
if(kind==="capitalization"&&h.start>0&&(text[h.start-1]==="."||text[h.start-1]==="/")&&!/\s/.test(text.slice(Math.max(0,h.start-2),h.start)))continue;
if(["spelling","typo"].includes(kind)&&/^[A-Z][a-z]{2,}('s)?$/.test(frag)){
let idx=-1;for(let i=0;i<toks.length;i++)if(toks[i][1]===h.start){idx=i;break}
if(idx>0){const prev=toks[idx-1][0].toLowerCase();
if(!(prev==="."||prev==="mr"||prev==="mrs"||prev==="ms"||prev==="dr"))continue;
if(MAORI_DET.has(frag)&&idx+1<toks.length&&/^[A-Z]/.test(toks[idx+1][0]))continue}}
if(["spelling","typo"].includes(kind)&&frag.includes(" ")){}
const base=frag.endsWith("'s")?frag.slice(0,-2):frag;
if(["spelling","typo","wordchoice"].includes(kind)&&(NZ_WORDS.has(frag)||NZ_WORDS.has(base)||NZ_WORDS.has(frag.toLowerCase())))continue;
if(rule==="WhomSubjectOfVerb"){const pre=text.slice(Math.max(0,h.start-30),h.end+2);
if(/(?:^|\s)(?:to|for|with|from|by|of)\s+whom\b/i.test(pre))continue}
out.push(h)}
return out}
/* Merge Engine94 findings into every published Harper record (Harper wins overlaps). */
const publishProof933Original933=publishProof933;
publishProof933=function(record){publishProof933Original933(record);
if(!record.lints.length||!liveProof933()||!record.text||record.text.length>4e3||record.__engine94)return;
const block=record.block,text=record.text;
Engine94.scan(record).then(findings=>{
if(!findings||!findings.length||!liveProof933())return;
const current=harperCache85.get(block);
if(!current||current!==record||!validProseRecord85(record)||current.text!==text)return;
const additions=findings.filter(f=>{const fEnd=f.end,fStart=f.start;
const clashes=current.lints.some(l=>fStart<l.end&&l.start<fEnd);
return !clashes}).map(f=>({start:f.start,end:f.end,problem:f.problem,kind:f.kind||"grammar",message:f.message,suggestions:f.suggestions}));
if(!additions.length)return;
record.__engine94=true;
mergeLiveLints933(current,additions);
publishProof933Original933(current);
paintHarperView85()}).catch(()=>{})};
"""


def main():
    s = open(SRC, "r", encoding="utf-8").read()

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
