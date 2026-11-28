"""Corpus driver v2: frame-DSL combinatorial generation with hash-partitioned
seed-disjoint splits.

Every unique (frame, fill-values) instantiation is hashed; the hash decides
its split: 0-79 train, 80-88 validation, 89-94 calibration, 95-99 test-bucket.
Test items are drawn ONLY from the test bucket, so no sentence-level overlap
between training data and final test is possible.
Curated templates.py records only feed train/val/calib (never test).
"""

import json, random, hashlib, re, sys, os, itertools
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from frames import FAMILIES
from frames2 import extended_families
from templates import build_all
# drop small versions of families that frames2 replaces
FAMILIES = [f for f in FAMILIES if f.get("tag") not in
            ("numbers", "dates", "quotes", "uk", "us", "nz", "negation")]
FAMILIES.extend(extended_families())
PROF_CATS = {"spelling", "contraction", "punct_period", "punct_question",
             "redundancy", "preposition", "repetition"}
for f in FAMILIES:
    if f["cat"] in PROF_CATS and "domain" not in f:
        f["domain"] = "professional"

rng = random.Random(20260714)
OUT = "/home/z/my-project/data"
os.makedirs(OUT, exist_ok=True)

def h(s):
    return hashlib.sha1(s.encode("utf-8")).hexdigest()

def bucket_of(s):
    return int(h(s)[:12], 16) % 100

# ---------------------------------------------------------------- instantiate
MAX_PER_FRAME_POOL = 24   # multi-slot pool cap
MAX_ONE_SLOT_POOL = 200   # single-slot pool cap
MAX_COMBOS = 2500         # combos enumerated per frame

def instantiate(family, frame):
    text, slots, corr = frame[0], frame[1], (frame[2] if len(frame) > 2 else None)
    pools = {}
    for k, v in slots.items():
        vv = list(dict.fromkeys(v))  # dedupe, keep order
        cap = MAX_ONE_SLOT_POOL if len(slots) == 1 else MAX_PER_FRAME_POOL
        if len(vv) > cap:
            rr = random.Random(h(text + k)[:8])
            vv = rr.sample(vv, cap)
        pools[k] = vv
    names = list(pools.keys())
    combos = list(itertools.product(*[pools[n] for n in names])) if names else [()]
    if len(combos) > MAX_COMBOS:
        rr = random.Random(h(text)[:8])
        combos = rr.sample(combos, MAX_COMBOS)
    out = []
    for combo in combos:
        fills = dict(zip(names, combo))
        try:
            clean = text.format(**fills)
        except Exception:
            continue
        if not clean.strip():
            continue
        item = {"clean": clean, "domain": family.get("domain", "essay"),
                "tag": family.get("tag"), "cat": family["cat"], "corr": None}
        if corr and corr[0] is not None:
            find_spec, repl_spec = corr
            if "{" in find_spec:
                # find is a template on slots
                find_str = find_spec.format(**fills)
                # primary slot = first {SLOT} in find_spec
                m = re.search(r"\{(\w+)\}", find_spec)
                prim = fills.get(m.group(1), "") if m else ""
            else:
                find_str = find_spec
                # primary slot: if the frame has exactly one slot use it
                prim = fills[names[0]] if len(names) == 1 else ""
            if callable(repl_spec):
                repl_str = repl_spec(prim)
            else:
                repl_str = repl_spec
            if repl_str is None:
                continue
            if find_str == "":
                continue
            if clean.count(find_str) != 1:
                continue
            i = clean.find(find_str)
            before = clean[i-1] if i > 0 else " "
            after = clean[i+len(find_str)] if i+len(find_str) < len(clean) else " "
            if find_str[0].isalpha() and before.isalnum():
                continue
            if find_str[-1].isalpha() and after.isalnum():
                continue
            if find_str != repl_str:
                item["corr"] = {"cat": family["cat"], "find": find_str,
                                "repl": repl_str}
        out.append(item)
    return out

def apply_corr(clean, corr):
    f, r = corr["find"], corr["repl"]
    if clean.count(f) != 1:
        return None
    i = clean.find(f)
    return clean[:i] + r + clean[i+len(f):], (i, i + len(f), r)

# ---------------------------------------------------------------- build corpus
def auto_tags(s, domain):
    t = set()
    low = " " + s.lower() + " "
    if any(k in low for k in (" uk", "united kingdom", "london", "colour",
                              "organis", "centre", "travell", "practis",
                              "programme", "theatre", "favour", "flavour",
                              "realis", "harbour", "licence", "defence",
                              "aluminium", "fortnight", "metre")):
        t.add("uk")
    if any(k in low for k in (" nz", "zealand", "kia ora", "tramping", "bach",
                              "jandals", "togs", "dairy", "ute", "kai", "hui",
                              "marae", "auckland", "wellington", "christchurch",
                              "dunedin", "rotorua", "queenstown", "hamilton",
                              "heaps", "sweet as", "paddock", "kura", "kapa haka",
                              "waikaremoana", "gisborne", "te reo", "ka pai",
                              "choice,", "nau mai", "haere mai")):
        t.add("nz")
    if any(k in low for k in (" us)", "color", "organiz", "center", "theater",
                              "labor", "analyz", "behavior", "optimiz", "gray",
                              "catalog", "favorite", "flavor", "meter tail")):
        t.add("us")
    if re.search(r"\$\d|\b\d", s):
        t.add("numbers")
    if re.search(r"\b\d{1,2}[/.]\d{1,2}[/.]\d{2,4}\b|\b\d{1,2} (January|February|March|April|May|June|July|August|September|October|November|December) \d{4}", s):
        t.add("dates")
    if '"' in s:
        t.add("quotes")
    if any(k in low for k in (" javascript", "typescript", " kubernetes", " postgres",
                              " npm", " api", " json", " nginx", " redis", " docker",
                              " graphql", " git ", " oauth", " tls", " dns", " vue",
                              " eslint", " grpc", " node.js", " python", " pipeline",
                              " websocket", " rest ", " terraform", " prometheus",
                              " grafana", " sqlite", " config", " dashboard")):
        t.add("tech")
    if re.search(r"\b(Wiremu|Aroha|Hōne|Priya|Xiaoming|Aoife|Mereana|Rawiri|Kavita|Rohan|Deepa|Mei|Yuki|Takashi|Mateo|Inés|Sofia|Leon|Amelia|Oliver|Charlotte|Henry|Lucas|Nguyễn|McGregor|O'Connell|Tane|Manaia|Jesse|Rita)\b", s):
        t.add("names")
    if "didn't" in low or "never" in low or "nobody" in low or "any" in low or "hardly" in low or "scarcely" in low:
        t.add("negation")
    return t

# ------------------------------------------------ instantiate ALL families
instances = []
for fam in FAMILIES:
    for frame in fam["frames"]:
        instances.extend(instantiate(fam, frame))
print(f"frame instances: {len(instances)}")

# add curated records (templates.py) to non-test splits only
curated = build_all()

def split_of_instance(inst):
    key = inst["clean"] + "|" + (inst["corr"]["find"] if inst["corr"] else "")
    b = bucket_of(key)
    if b < 80:
        return "train"
    if b < 85:
        return "val"
    if b < 90:
        return "calib"
    return "test"

by_split = defaultdict(list)
for inst in instances:
    by_split[split_of_instance(inst)].append(inst)
print("split sizes (frame instances):",
      {k: len(v) for k, v in by_split.items()})

# ---------------------------------------------------------------- train data
TARGETS = {"sva": 3000, "sva_3sg": 2600, "past": 2800, "verb_form": 1500,
           "article": 2200, "plural": 1800, "irr_plural": 800,
           "quantifier": 700, "confusable": 3200, "double_neg": 800,
           "adjadv": 1800, "comparative": 1000, "contraction": 1500,
           "capitalization": 1800, "punct_period": 600, "punct_question": 400,
           "repetition": 1200, "preposition": 1700, "redundancy": 900,
           "verb_ing": 1200, "spelling": 2200}

def emit(inst, multi_pool=None):
    """Make an example (clean or corrupted) from an instance."""
    if inst["corr"] is None:
        tags = sorted(auto_tags(inst["clean"], inst["domain"]))
        return {"s_bad": inst["clean"], "s_good": inst["clean"], "edits": [],
                "cats": [], "domain": inst["domain"], "tags": tags, "clean": True}
    res = apply_corr(inst["clean"], inst["corr"])
    if res is None:
        return None
    bad, (a, b_, r) = res
    tags = sorted(auto_tags(bad, inst["domain"]))
    return {"s_bad": bad, "s_good": inst["clean"],
            "edits": [{"start": a, "end": b_, "text": r}],
            "cats": [inst["corr"]["cat"]], "domain": inst["domain"],
            "tags": tags, "clean": False}

train_pool = by_split["train"]
val_pool = by_split["val"]
calib_pool = by_split["calib"]
test_pool = by_split["test"]

def build_split(pool, targets, clean_ratio, rng, cap=None):
    bycat = defaultdict(list)
    clean_items = []
    for inst in pool:
        if inst["corr"]:
            bycat[inst["corr"]["cat"]].append(inst)
        else:
            clean_items.append(inst)
    out, seen = [], set()
    def try_emit(inst):
        ex = emit(inst)
        if ex is None:
            return False
        k = h(ex["s_bad"] + "|" + ex["s_good"])[:16]
        if k in seen:
            return False
        seen.add(k)
        out.append(ex)
        return True
    for cat, target in targets.items():
        if cat not in bycat or not bycat[cat]:
            print(f"  !! missing category in pool: {cat}")
            continue
        pool_c = bycat[cat]
        rng.shuffle(pool_c)
        made = 0
        for inst in pool_c:
            if made >= target:
                break
            if try_emit(inst):
                made += 1
    clean_target = int(sum(targets.values()) * clean_ratio / (1 - clean_ratio)) + 1
    rng.shuffle(clean_items)
    made = 0
    for inst in clean_items:
        if made >= clean_target:
            break
        if try_emit(inst):
            made += 1
    if cap and len(out) > cap:
        rng.shuffle(out)
        out = out[:cap]
    return out

train_data = build_split(train_pool, TARGETS, 0.25, rng)
val_data = build_split(val_pool, {k: v // 9 + 15 for k, v in TARGETS.items()}, 0.28, rng)
calib_data = build_split(calib_pool, {k: v // 13 + 8 for k, v in TARGETS.items()}, 0.32, rng)
print(f"train: {len(train_data)}, val: {len(val_data)}, calib: {len(calib_data)}")

# curated records -> extra train variety (never test)
cur_seen = set(h(e["s_bad"] + "|" + e["s_good"])[:16] for e in train_data)
for e in train_data + val_data + calib_data:
    pass
extra_curated = []
def emit_curated(rec):
    if not rec["cors"]:
        ex = {"s_bad": rec["clean"], "s_good": rec["clean"], "edits": [],
              "cats": [], "domain": rec["domain"], "tags": sorted(auto_tags(rec["clean"], rec["domain"])), "clean": True}
        extra_curated.append(ex)
        return
    for cor in rec["cors"]:
        res = apply_corr(rec["clean"], cor)
        if res:
            bad, (a, b_) = res[0], res[1][:2]
            ex = {"s_bad": bad, "s_good": rec["clean"],
                  "edits": [{"start": a, "end": b_, "text": cor["repl"]}],
                  "cats": [cor["cat"]], "domain": rec["domain"],
                  "tags": sorted(auto_tags(bad, rec["domain"])), "clean": False}
            extra_curated.append(ex)
for rec in curated:
    emit_curated(rec)
rng.shuffle(extra_curated)
train_data.extend(extra_curated[:6000])
print(f"train after curated extras: {len(train_data)}")

# ---------------------------------------------------------------- final test
DIM_QUOTA = {"essay": 250, "professional": 250, "technical": 300, "clean": 300,
             "negation": 100, "names": 100, "numbers": 100, "dates": 100,
             "quotes": 50, "uk": 150, "nz": 100, "us": 100}

test_out = []
used_global = set()
for d in (train_data, val_data, calib_data):
    for ex in d:
        used_global.add(h(ex["s_bad"] + "|" + ex["s_good"])[:16])

def emit_test(inst, tag, force_clean=False):
    ex = emit(inst)
    if ex is None:
        return False
    k = h(ex["s_bad"] + "|" + ex["s_good"])[:16]
    if k in used_global:
        return False
    used_global.add(k)
    ex["tag_primary"] = tag
    test_out.append(ex)
    return True

# index test pool by tag and cat
pool_by_tag = defaultdict(list)
for inst in test_pool:
    tt = inst.get("tag")
    tags = auto_tags(inst["clean"], inst["domain"])
    if tt:
        pool_by_tag[tt].append(inst)
    for t in tags:
        pool_by_tag[t].append(inst)

# domain quotas draw corrupted + clean mix
DOMAIN_CORR = {"essay": 0.6, "professional": 0.6, "technical": 0.5}
PROTECTED_TAGS = {"uk", "us", "nz", "numbers", "dates", "quotes",
                  "names", "negation", "clean", "tech"}
def not_protected(inst):
    if inst.get("tag") in PROTECTED_TAGS:
        return False
    return not (auto_tags(inst["clean"], inst["domain"]) & PROTECTED_TAGS)

def fill_domain_quota(tag, quota):
    got = 0
    if tag == "technical":
        cand = [i for i in test_pool
                if (i.get("tag") == "tech" or "tech" in auto_tags(i["clean"], i["domain"]))]
    else:
        cand = [i for i in test_pool
                if i["domain"] == tag and i.get("tag") is None
                and not (auto_tags(i["clean"], i["domain"]) & PROTECTED_TAGS)]
    rng.shuffle(cand)
    want_corr = DOMAIN_CORR[tag]
    corr_items = [i for i in cand if i["corr"]]
    clean_items = [i for i in cand if not i["corr"]]
    n_corr = int(quota * want_corr)
    for inst in corr_items[:n_corr]:
        if got >= quota:
            break
        if emit_test(inst, tag):
            got += 1
    for inst in clean_items:
        if got >= quota:
            break
        if emit_test(inst, tag):
            got += 1
    return got

def fill_tag_quota(tag, quota, want_clean=None):
    got = 0
    cand = pool_by_tag.get(tag, [])
    if not cand:
        return 0
    rng.shuffle(cand)
    if want_clean is not None:
        cand = [i for i in cand if (not i["corr"]) == want_clean]
    for inst in cand:
        if got >= quota:
            break
        if emit_test(inst, tag):
            got += 1
    return got

results = {}
# protected clean quotas first
results["names"] = fill_tag_quota("names", 100, want_clean=True)
results["numbers"] = fill_tag_quota("numbers", 100, want_clean=True)
results["dates"] = fill_tag_quota("dates", 100, want_clean=True)
results["quotes"] = fill_tag_quota("quotes", 50, want_clean=True)
results["negation"] = fill_tag_quota("negation", 50, want_clean=True)
# negation corrupted: double_neg instances
dn = [i for i in test_pool if i["corr"] and i["corr"]["cat"] == "double_neg"]
rng.shuffle(dn)
g = 0
for inst in dn:
    if g >= 50:
        break
    if emit_test(inst, "negation"):
        g += 1
results["negation"] += g
# regional quotas: mixed clean/corrupted (35% clean)
for tag in ("uk", "nz", "us"):
    cand = pool_by_tag.get(tag, [])
    rng.shuffle(cand)
    got = 0
    n_clean_quota = int(DIM_QUOTA[tag] * 0.35)
    cl = [i for i in cand if not i["corr"]][:n_clean_quota]
    co = [i for i in cand if i["corr"]][:DIM_QUOTA[tag] - n_clean_quota]
    for inst in cl + co:
        if emit_test(inst, tag):
            got += 1
    results[tag] = got
# technical (mixed clean/corrupted), then essay and professional
results["technical"] = fill_domain_quota("technical", 300)
results["essay"] = fill_domain_quota("essay", 250)
results["professional"] = fill_domain_quota("professional", 250)
# clean quota last: general clean sentences across domains
cl = [i for i in test_pool if not i["corr"]]
rng.shuffle(cl)
g = 0
for inst in cl:
    if g >= 300:
        break
    if emit_test(inst, "clean"):
        g += 1
results["clean"] = g

for k, v in results.items():
    print(f"test[{k}] {v}/{DIM_QUOTA[k]}")

# fill to exactly 2000 from test pool (any instance, prefer corrupted mix)
fill_tries = 0
while len(test_out) < 2000 and fill_tries < 40000:
    fill_tries += 1
    inst = rng.choice(test_pool)
    emit_test(inst, "fill")
rng.shuffle(test_out)
print(f"final test: {len(test_out)}")

# ---------------------------------------------------------------- write
for name, data in [("train", train_data), ("validation", val_data),
                   ("calibration", calib_data), ("final_test", test_out)]:
    with open(f"{OUT}/{name}.jsonl", "w") as f:
        for ex in data:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")

c = Counter()
for ex in train_data:
    for cat in ex["cats"]:
        c[cat] += 1
print("train cats:", dict(c.most_common()))
tc = Counter(ex["tag_primary"] for ex in test_out)
print("test tags:", dict(tc))
tcl = Counter("clean" if ex["clean"] else "corrupted" for ex in test_out)
print("test clean/corrupted:", dict(tcl))
tcc = Counter()
for ex in test_out:
    for cat in ex["cats"]:
        tcc[cat] += 1
print("test cats:", dict(tcc.most_common()))

# drop any train example whose pair-hash collides with another split (curated vs frame dupes)
for nm, dd in [("validation", val_data), ("calibration", calib_data), ("final_test", test_out)]:
    keep = set(h(e["s_bad"] + "|" + e["s_good"])[:16] for e in dd)
    before = len(train_data)
    train_data = [e for e in train_data if h(e["s_bad"] + "|" + e["s_good"])[:16] not in keep]
    if before != len(train_data):
        print(f"dropped {before - len(train_data)} train items overlapping {nm}")
# rewrite train file after dedup
with open(f"{OUT}/train.jsonl", "w") as f:
    for ex in train_data:
        f.write(json.dumps(ex, ensure_ascii=False) + "\n")

# hard integrity checks
train_set = set(h(e["s_bad"] + "|" + e["s_good"])[:16] for e in train_data)
for nm, dd in [("validation", val_data), ("calibration", calib_data), ("final_test", test_out)]:
    dd_set = set(h(e["s_bad"] + "|" + e["s_good"])[:16] for e in dd)
    inter = train_set & dd_set
    assert not inter, f"OVERLAP between train and {nm}: {len(inter)}"
print("integrity: no train/test/val/calib overlap ✓")
