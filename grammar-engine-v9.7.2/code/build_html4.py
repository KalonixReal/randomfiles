#!/usr/bin/env python3
"""Build notepad-v9.7.2-grammar.html on the release-v9.5.0 shell.

Surgical replacement inside the grammarReleaseWorker script + main app script:
  1. W94_DATA blob        -> new export (threshold 1.0: tagger dormant by measurement)
  2. W94_RULES blob       -> rules v2.9 (fresh-set recall round)
  3. W94_WEIGHTS_B64 blob  -> gru3 int8 weights (neural component, retained)
  4. embedded engine94.js body -> new engine94.js body (identical IIFE boundary,
     shell's custom nspell/worker glue preserved untouched)
  5. proofPanelStyle933 segment -> v9.3.4 ORIGINAL segment verbatim
     (restores: spelling wavy squiggle + background-tint highlight instead of
     solid underline; the always-on i::before tint over marked words)
  6. proofHoverMarks933 block (hover overlay marks) -> removed entirely
     (v9.3.4 did not have hover marks)
"""
import hashlib
import json

SRC = '/home/z/my-project/upload/release-v9.5.0.html'
ORIG = '/home/z/my-project/download/notepad-v9.3.4-ORIGINAL.html'
OUT = '/home/z/my-project/download/notepad-v9.7.2-grammar.html'
NEW_JS = '/home/z/my-project/scripts/engine94.js'
OLD_JS = '/home/z/my-project/scripts/engine94_v950_original.js'

f = open(SRC, 'rb').read().decode('utf-8')
print('base file bytes:', len(f))

# ---- 1. engine body replacement -------------------------------------------
old_js = open(OLD_JS).read()
new_js = open(NEW_JS).read()
marker = '\n// worker protocol'
cut_old = old_js.find(marker)
cut_new = new_js.find(marker)
assert cut_old > 0 and cut_new > 0
old_prefix = old_js[:cut_old]
new_prefix = new_js[:cut_new]
assert f.count(old_prefix) == 1, f'old engine body not unique: {f.count(old_prefix)}'
f = f.replace(old_prefix, new_prefix)
print(f'engine body replaced: {len(old_prefix)} -> {len(new_prefix)} bytes')

# ---- 2. blob replacement ----------------------------------------------------
dec = json.JSONDecoder()


def replace_const(f, var, new_text):
    tag = 'const ' + var + ' = '
    i = f.find(tag)
    assert i > 0, var
    if var == 'W94_WEIGHTS_B64':
        j = f.find('";', i + len(tag))
        f = f[:i + len(tag) + 1] + new_text + f[j:]
    else:
        _obj, end = dec.raw_decode(f, i + len(tag))
        f = f[:i + len(tag)] + new_text + f[end:]
    return f


data = open('/home/z/my-project/scripts/export_out/engine94_data.json').read()
data_obj = json.loads(data)
data_obj['threshold'] = 1.0  # measured: rules-only wins every split; tagger dormant
rules = open('/home/z/my-project/scripts/export_out/engine94_rules.json').read()
weights = open('/home/z/my-project/scripts/export_out/engine94_weights.b64').read().strip()

f = replace_const(f, 'W94_DATA', json.dumps(data_obj, separators=(',', ':')))
f = replace_const(f, 'W94_RULES', rules)
f = replace_const(f, 'W94_WEIGHTS_B64', weights)

# ---- 2b. NZ/Maori lexicon into both Hunspell dictionaries ------------------
import sys as _sys
if '/home/z/my-project/scripts' not in _sys.path:
    _sys.path.insert(0, '/home/z/my-project/scripts')
from engine import NZ_SUPPRESS_SET

TECH_WORDS = ['config', 'configs', 'wifi', 'apis', 'https', 'yaml', 'postgresql',
    'mongodb', 'redis', 'graphql', 'grpc', 'kubernetes', 'npm', 'nginx', 'ipv4',
    'ipv6', 'cdn', 'backend', 'frontend', 'fullstack', 'microservices', 'serverless',
    'devops', 'sysadmin', 'repo', 'repos', 'changelog', 'whitelist', 'blocklist',
    'allowlist', 'checkbox', 'datepicker', 'dropdown', 'popup', 'toolbar', 'sidebar',
    'workaround', 'signup', 'login', 'logout', 'namespace', 'deprecated', 'grep',
    'regex', 'regexes', 'wildcard', 'boolean', 'hashmap', 'linkedlist', 'utf8',
    'localhost', 'username', 'keypair', 'subnet', 'bandwidth', 'throughput',
    'uptime', 'downtime', 'outage', 'toolchain', 'makefile', 'cmake', 'webpack',
    'vite', 'rollup', 'eslint', 'prettier', 'jest', 'mocha', 'pytest', 'junit',
    'selenium', 'playwright', 'puppeteer', 'cypress', 'gitlab', 'bitbucket',
    'vscode', 'neovim', 'zsh', 'ksh', 'powershell', 'cron', 'systemd', 'lsof',
    'sed', 'awk', 'curl', 'wget', 'gzip', 'bzip2', 'zipfile', 'tarball',
    'middleware', 'api', 'cli', 'gui', 'http', 'json', 'xml', 'sql', 'sqlite',
    'mysql', 'docker', 'pip', 'javascript', 'typescript', 'macos', 'iphone',
    'ipad', 'android', 'linux', 'unix', 'ubuntu', 'debian', 'vpn', 'ssh', 'tcp',
    'udp', 'dns', 'unicode', 'ascii']

NZ_EXTRA = ['tangi', 'kahawai', 'Kalonix', 'kōwhai', 'taniwha', 'tāmati',
            'Ōhope', 'Ngāruawāhia', 'Tutukākā', 'Ōtago', 'tōtara', 'korimako',
            'pōhutukawa', 'kōrero', 'mōrena', 'kaiora', 'whānau', 'rūnanga',
            'Ngāti', 'whakapapa', 'manaakitanga', 'kaitiakitanga', 'kotahitanga',
            'rangimārie', 'mokopuna', 'kaumātua', 'pēpi', 'whakairo', 'pounamu',
            'whanaunga', 'mahi', 'kapa', 'haka', 'pōtae', 'tamariki', 'tangata',
            'whenua', 'moana', 'maunga', 'waka']
nz_words = sorted(set(NZ_SUPPRESS_SET) | set(NZ_EXTRA) | set(TECH_WORDS))

def inject_nz(f):
    dec2 = json.JSONDecoder()
    i = f.find('const SPELL_ASSETS = ')
    obj, end = dec2.raw_decode(f, i + len('const SPELL_ASSETS = '))
    for lang in obj:
        dic = obj[lang]['dic']
        lines = dic.split('\n')
        try:
            count = int(lines[0].strip().lstrip('\ufeff'))
        except ValueError:
            count = None
        have = {l.split('/')[0].lower() for l in lines[1:] if l}
        add = [w for w in nz_words if w.lower() not in have]
        if not add:
            continue
        newlines = lines + add
        if count is not None:
            newlines[0] = str(count + len(add))
        obj[lang]['dic'] = '\n'.join(newlines)
        print(f'{lang} dic: +{len(add)} NZ words (total {count + len(add)})')
    return f[:i + len('const SPELL_ASSETS = ')] + json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + f[end:]

f = inject_nz(f)

# ---- 5. restore the v9.3.4 suggestions UI: panel CSS -----------------------
PANEL_A = 'const proofPanelStyle933=document.createElement("style");proofPanelStyle933.textContent='
PANEL_B = 'document.head.append(proofPanelStyle933);'

def cut_segment(text, a, b, name):
    i = text.find(a)
    assert i > 0, name + ' start not found'
    j = text.find(b, i) + len(b)
    assert j > len(b), name + ' end not found'
    assert text.count(a) == 1, name + ' not unique'
    return i, j

oi, oj = cut_segment(ORIG_txt := open(ORIG, 'rb').read().decode('utf-8', 'replace'), PANEL_A, PANEL_B, 'orig panel')
orig_segment = ORIG_txt[oi:oj]
si, sj = cut_segment(f, PANEL_A, PANEL_B, 'shell panel')
f = f[:si] + orig_segment + f[sj:]
print(f'proofPanelStyle933 segment restored to v9.3.4: {sj-si} -> {len(orig_segment)} bytes')

# ---- 6. remove the hover marks block (not in v9.3.4) -------------------------
HOV_A = 'const proofHoverMarks933=[];'
HOV_B = 'canvasWrap.addEventListener("pointerleave",clearProofHover933);'
hi = f.find(HOV_A)
assert hi > 0, 'hover block start not found'
he = f.find(HOV_B, hi) + len(HOV_B)
assert f.count(HOV_A) == 1, 'hover start not unique'
f = f[:hi] + f[he + 1:] if f[he:he + 1] == '\n' else f[:hi] + f[he:]
print(f'hover marks block removed: {he-hi} bytes')

out = f.encode('utf-8')
open(OUT, 'wb').write(out)
h = hashlib.sha256(out).hexdigest()
print(f'wrote {OUT}: {len(out)} bytes sha256={h[:16]}')

# ---- 3. round-trip verification ---------------------------------------------
g = open(OUT, 'rb').read().decode('utf-8', 'replace')
ok = True
for var, src in [('W94_DATA', json.dumps(data_obj, separators=(',', ':'))),
                 ('W94_RULES', rules),
                 ('W94_WEIGHTS_B64', weights)]:
    n = g.count(src)
    print(f'{var}: occurrences of new blob = {n}')
    ok = ok and n == 1
assert new_prefix in g and old_prefix not in g
assert 'SPELL_ASSETS' in g and 'nspell' in g, 'shell glue lost!'
assert g.count('grammarReleaseWorker') == 2
# UI restoration checks
assert '#harperProofLayer85 i::before' in g, 'v9.3.4 tint CSS missing'
assert '::highlight(notepad-proof-spelling){background-color:rgba' in g, 'v9.3.4 spelling highlight missing'
assert 'proof-hover933' not in g, 'hover CSS still present!'
assert 'proofHoverMarks933' not in g, 'hover JS still present!'
assert 'clearProofHover933' not in g, 'hover JS still present!'
# wavy squiggle CSS (unchanged harperCSS85) still intact
assert g.count("underline wavy") >= 2, 'wavy underline CSS missing'
print('round-trip structure OK' if ok else 'ROUND-TRIP FAILED')
