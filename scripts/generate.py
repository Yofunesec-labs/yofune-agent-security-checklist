#!/usr/bin/env python3
from pathlib import Path
import csv, json, yaml, re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'generated'; OUT.mkdir(exist_ok=True)
SITE = ROOT/'site'; SITE.mkdir(exist_ok=True)
BASELINE = ROOT/'baseline'; BASELINE.mkdir(exist_ok=True)
VERIFY = ROOT/'verification-tests'; VERIFY.mkdir(exist_ok=True)
DOCS = ROOT/'docs'; DOCS.mkdir(exist_ok=True)

doc = yaml.safe_load((ROOT/'schema/controls.yaml').read_text(encoding='utf-8'))
tests_doc = yaml.safe_load((ROOT/'schema/tests.yaml').read_text(encoding='utf-8'))
controls = doc['controls']; domains = {d['id']:d for d in doc['domains']}; tests=tests_doc['tests']

with (OUT/'controls.csv').open('w', newline='', encoding='utf-8-sig') as f:
    cols=['id','domain','domain_title','title','severity','target_assurance','objective','threat','check','pass_criteria','tests','owasp','nist','evidence']
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader()
    for c in controls:
        w.writerow({'id':c['id'],'domain':c['domain'],'domain_title':domains[c['domain']]['title'],'title':c['title'],'severity':c['severity'],'target_assurance':c['target_assurance'],'objective':c['objective'],'threat':c['threat'],'check':c['check'],'pass_criteria':c['pass_criteria'],'tests':';'.join(c['adversarial_tests']),'owasp':';'.join(c['mappings']['owasp_agentic_2026']),'nist':';'.join(c['mappings']['nist_ai_rmf_functions']),'evidence':';'.join(c['evidence'])})

(OUT/'controls.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(SITE/'controls.json').write_text(json.dumps(doc,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
(OUT/'tests.json').write_text(json.dumps(tests_doc,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

lines=['# Generated YASC Control Catalog','',f"Version: `{doc['metadata']['version']}`  ",f"Snapshot: `{doc['metadata']['snapshot_date']}`",'']
for d in doc['domains']:
    lines += [f"## {d['id']} — {d['title']}",'']
    for c in [x for x in controls if x['domain']==d['id']]:
        lines += [f"### {c['id']} — {c['title']}",'',f"- Severity: `{c['severity']}`",f"- Target assurance: `{c['target_assurance']}`",f"- Objective: {c['objective']}",f"- Pass: {c['pass_criteria']}",'']
(OUT/'controls.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

# Domain-oriented baseline documents are generated from controls.yaml.
for d in doc['domains']:
    rows=[x for x in controls if x['domain']==d['id']]
    lines=[f"# {d['id']} — {d['title']}",f"> **Core question:** {d['question']}",f"> **Principle:** {d['principle']}",'','## Controls','']
    for c in rows:
        lines += [f"### {c['id']} — {c['title']}",f"**Severity:** `{c['severity']}`  ",f"**Target assurance:** `{c['target_assurance']}`",'', '**Security objective**  ',c['objective'],'','**Applies when**']
        lines += [f"- {x}" for x in c['applies_when']]
        lines += ['', '**Threat**  ',c['threat'],'','**Check**  ',c['check'],'','**Adversarial tests**']
        lines += [f"- `{x}`" for x in c['adversarial_tests']]
        lines += ['', '**Required evidence**']+[f"- {x}" for x in c['evidence']]
        o=', '.join(c['mappings'].get('owasp_agentic_2026',[])) or '—'; n=', '.join(c['mappings'].get('nist_ai_rmf_functions',[])) or '—'
        lines += ['', '**Pass criteria**  ',c['pass_criteria'],'','**Mappings**  ',f"OWASP Agentic 2026: {o}  ",f"NIST AI RMF functions: {n}",'','---','']
    (BASELINE/f"{d['id']}-{d['slug']}.md").write_text('\n'.join(lines),encoding='utf-8')

# Verification playbooks by category.
bycat={}
for t in tests: bycat.setdefault(t['category'],[]).append(t)
for cat, rows in sorted(bycat.items()):
    folder=VERIFY/cat; folder.mkdir(parents=True,exist_ok=True)
    lines=[f"# YASC Verification Tests — {cat}",'',f"Version: `{tests_doc['metadata']['version']}`  ",f"Reference snapshot: `{tests_doc['metadata']['snapshot_date']}`",'', '> Run only with explicit authorization and appropriate containment. Test definitions are procedures, not permission to target third parties.','']
    for t in rows:
        lines += [f"## {t['id']} — {t['title']}",'',f"**Severity:** `{t['severity']}`",'',f"**Purpose:** {t['purpose']}",'','### Preconditions']+[f"- {x}" for x in t['preconditions']]
        lines += ['','### Procedure']+[f"{i}. {x}" for i,x in enumerate(t['procedure'],1)]
        lines += ['','### Expected result',t['expected_result'],'','### Evidence']+[f"- {x}" for x in t['evidence']]
        lines += ['','### Controls']+[f"- `{x}`" for x in t['controls']]
        lines += ['','### Safety']+[f"- {x}" for x in t['safety']]+['','---','']
    (folder/'README.md').write_text('\n'.join(lines),encoding='utf-8')

# Human-readable full catalog.
lines=['# YASC Control and Verification Test Catalog','',f"**Version:** {doc['metadata']['version']}  ",f"**Reference snapshot:** {doc['metadata']['snapshot_date']}",'', 'This catalog is generated from `schema/controls.yaml` and `schema/tests.yaml`. The YAML files remain authoritative.','']
for d in doc['domains']:
    lines += [f"## {d['id']} — {d['title']}",'']
    for c in [x for x in controls if x['domain']==d['id']]:
        lines += [f"### {c['id']} — {c['title']}",'',f"**Severity:** `{c['severity']}` · **Target:** `{c['target_assurance']}`",'',f"**Objective:** {c['objective']}",f"**Threat:** {c['threat']}",f"**Check:** {c['check']}",f"**Pass criteria:** {c['pass_criteria']}",'', '**Tests:** '+', '.join(f'`{x}`' for x in c['adversarial_tests']),'','**Evidence:** '+', '.join(c['evidence']),'']
lines += ['---','','# Verification Tests','']
for cat,rows in sorted(bycat.items()):
    lines += [f"## {cat}",'']
    for t in rows:
        lines += [f"### {t['id']} — {t['title']}",'',f"**Severity:** `{t['severity']}`",'',f"**Purpose:** {t['purpose']}",'','**Procedure:**']+[f"{i}. {x}" for i,x in enumerate(t['procedure'],1)]
        lines += ['','**Expected:** '+t['expected_result'],'','**Evidence:** '+', '.join(t['evidence']),'','**Controls:** '+', '.join(f'`{x}`' for x in t['controls']),'']
(DOCS/'control-test-catalog.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

# Category index.
idx=['# Verification Tests','',f"YASC `{tests_doc['metadata']['version']}` defines **{len(tests)}** reusable tests.",'']
for cat,rows in sorted(bycat.items()): idx.append(f"- [{cat}]({cat}/README.md) — {len(rows)} tests")
(VERIFY/'README.md').write_text('\n'.join(idx)+'\n',encoding='utf-8')

print(f"Generated {len(controls)} controls and {len(tests)} tests into generated/, baseline/, verification-tests/, docs/, and site/")
