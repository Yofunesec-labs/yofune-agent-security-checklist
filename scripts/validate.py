#!/usr/bin/env python3
from pathlib import Path
import json, sys
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
controls_doc = yaml.safe_load((ROOT/'schema/controls.yaml').read_text(encoding='utf-8'))
tests_doc = yaml.safe_load((ROOT/'schema/tests.yaml').read_text(encoding='utf-8'))
schema = json.loads((ROOT/'schema/controls.schema.json').read_text(encoding='utf-8'))
tests_schema = json.loads((ROOT/'schema/tests.schema.json').read_text(encoding='utf-8'))
assessment_schema = json.loads((ROOT/'schema/assessment.schema.json').read_text(encoding='utf-8'))
assessment_doc = yaml.safe_load((ROOT/'templates/assessment.yaml').read_text(encoding='utf-8'))
profiles_schema = json.loads((ROOT/'schema/profiles.schema.json').read_text(encoding='utf-8'))
profiles_doc = yaml.safe_load((ROOT/'schema/profiles.yaml').read_text(encoding='utf-8'))
verification_run_schema = json.loads((ROOT/'schema/verification-run.schema.json').read_text(encoding='utf-8'))
verification_run_doc = yaml.safe_load((ROOT/'templates/verification-run.yaml').read_text(encoding='utf-8'))
assurance_case_schema = json.loads((ROOT/'schema/assurance-case.schema.json').read_text(encoding='utf-8'))
assurance_case_doc = yaml.safe_load((ROOT/'templates/assurance-case.yaml').read_text(encoding='utf-8'))
verification_plan_schema = json.loads((ROOT/'schema/verification-plan.schema.json').read_text(encoding='utf-8'))
verification_plan_doc = yaml.safe_load((ROOT/'templates/verification-plan.yaml').read_text(encoding='utf-8'))
evidence_manifest_schema = json.loads((ROOT/'schema/evidence-manifest.schema.json').read_text(encoding='utf-8'))
evidence_manifest_doc = yaml.safe_load((ROOT/'templates/evidence-manifest.yaml').read_text(encoding='utf-8'))
conformance_claim_schema = json.loads((ROOT/'schema/conformance-claim.schema.json').read_text(encoding='utf-8'))
conformance_claim_doc = yaml.safe_load((ROOT/'templates/conformance-claim.yaml').read_text(encoding='utf-8'))

target_schema = json.loads((ROOT/'schema/target.schema.json').read_text(encoding='utf-8'))
target_doc = yaml.safe_load((ROOT/'templates/target.yaml').read_text(encoding='utf-8'))
gate_schema = json.loads((ROOT/'schema/gate-policy.schema.json').read_text(encoding='utf-8'))
gate_doc = yaml.safe_load((ROOT/'templates/gate-policy.yaml').read_text(encoding='utf-8'))
scenario_schema = json.loads((ROOT/'schema/execution-scenarios.schema.json').read_text(encoding='utf-8'))
scenario_doc = yaml.safe_load((ROOT/'harness/scenarios/core.yaml').read_text(encoding='utf-8'))

errors = sorted(Draft202012Validator(schema).iter_errors(controls_doc), key=lambda e: list(e.path))
if errors:
    for e in errors:
        print(f"controls schema error at {list(e.path)}: {e.message}", file=sys.stderr)
    sys.exit(1)

test_errors = sorted(Draft202012Validator(tests_schema).iter_errors(tests_doc), key=lambda e: list(e.path))
if test_errors:
    for e in test_errors:
        print(f"tests schema error at {list(e.path)}: {e.message}", file=sys.stderr)
    sys.exit(1)

assessment_errors = sorted(Draft202012Validator(assessment_schema).iter_errors(assessment_doc), key=lambda e: list(e.path))
if assessment_errors:
    for e in assessment_errors:
        print(f"assessment template schema error at {list(e.path)}: {e.message}", file=sys.stderr)
    sys.exit(1)

profile_errors = sorted(Draft202012Validator(profiles_schema).iter_errors(profiles_doc), key=lambda e: list(e.path))
if profile_errors:
    for e in profile_errors:
        print(f"profiles schema error at {list(e.path)}: {e.message}", file=sys.stderr)
    sys.exit(1)

verification_run_errors = sorted(Draft202012Validator(verification_run_schema).iter_errors(verification_run_doc), key=lambda e: list(e.path))
if verification_run_errors:
    for e in verification_run_errors:
        print(f"verification-run template schema error at {list(e.path)}: {e.message}", file=sys.stderr)
    sys.exit(1)

assurance_case_errors = sorted(Draft202012Validator(assurance_case_schema).iter_errors(assurance_case_doc), key=lambda e: list(e.path))
if assurance_case_errors:
    for e in assurance_case_errors:
        print(f"assurance-case template schema error at {list(e.path)}: {e.message}", file=sys.stderr)
    sys.exit(1)

verification_plan_errors = sorted(Draft202012Validator(verification_plan_schema).iter_errors(verification_plan_doc), key=lambda e: list(e.path))
if verification_plan_errors:
    for e in verification_plan_errors:
        print(f"verification-plan template schema error at {list(e.path)}: {e.message}", file=sys.stderr)
    sys.exit(1)

evidence_manifest_errors = sorted(Draft202012Validator(evidence_manifest_schema).iter_errors(evidence_manifest_doc), key=lambda e: list(e.path))
if evidence_manifest_errors:
    for e in evidence_manifest_errors:
        print(f"evidence-manifest template schema error at {list(e.path)}: {e.message}", file=sys.stderr)
    sys.exit(1)


for label, schema_doc, instance in [
    ('target template', target_schema, target_doc),
    ('gate-policy template', gate_schema, gate_doc),
    ('execution scenarios', scenario_schema, scenario_doc),
    ('secure mock target', target_schema, yaml.safe_load((ROOT/'examples/targets/mock-secure.yaml').read_text(encoding='utf-8'))),
    ('insecure mock target', target_schema, yaml.safe_load((ROOT/'examples/targets/mock-insecure.yaml').read_text(encoding='utf-8'))),
    ('MCP stdio target', target_schema, yaml.safe_load((ROOT/'examples/targets/mcp-stdio.yaml').read_text(encoding='utf-8'))),
    ('OpenAI Responses target', target_schema, yaml.safe_load((ROOT/'examples/targets/openai-responses.yaml').read_text(encoding='utf-8'))),
    ('Anthropic Messages target', target_schema, yaml.safe_load((ROOT/'examples/targets/anthropic-messages.yaml').read_text(encoding='utf-8'))),
    ('LangGraph target', target_schema, yaml.safe_load((ROOT/'examples/targets/langgraph.yaml').read_text(encoding='utf-8'))),
    ('CrewAI target', target_schema, yaml.safe_load((ROOT/'examples/targets/crewai.yaml').read_text(encoding='utf-8'))),
    ('smoke gate policy', gate_schema, yaml.safe_load((ROOT/'examples/gate-policy.yaml').read_text(encoding='utf-8'))),
    ('MCP gate policy', gate_schema, yaml.safe_load((ROOT/'examples/gate-policy-mcp.yaml').read_text(encoding='utf-8'))),
    ('MCP execution scenario', scenario_schema, yaml.safe_load((ROOT/'examples/scenarios/mcp.yaml').read_text(encoding='utf-8'))),
]:
    errs = sorted(Draft202012Validator(schema_doc).iter_errors(instance), key=lambda e: list(e.path))
    if errs:
        for e in errs: print(f"{label} schema error at {list(e.path)}: {e.message}", file=sys.stderr)
        sys.exit(1)

for label, plan_path in [('smoke plan', ROOT/'examples/plans/smoke.yaml'), ('MCP smoke plan', ROOT/'examples/plans/mcp-smoke.yaml')]:
    instance = yaml.safe_load(plan_path.read_text(encoding='utf-8'))
    errs = sorted(Draft202012Validator(verification_plan_schema).iter_errors(instance), key=lambda e: list(e.path))
    if errs:
        for e in errs: print(f"{label} schema error at {list(e.path)}: {e.message}", file=sys.stderr)
        sys.exit(1)

conformance_claim_errors = sorted(Draft202012Validator(conformance_claim_schema).iter_errors(conformance_claim_doc), key=lambda e: list(e.path))
if conformance_claim_errors:
    for e in conformance_claim_errors:
        print(f"conformance-claim template schema error at {list(e.path)}: {e.message}", file=sys.stderr)
    sys.exit(1)

controls = controls_doc['controls']; domains = controls_doc['domains']; tests = tests_doc['tests']
control_ids = [c['id'] for c in controls]; domain_ids = {d['id'] for d in domains}; test_ids = [t['id'] for t in tests]

def unique(name, vals):
    dup = {x for x in vals if vals.count(x) > 1}
    if dup:
        raise SystemExit(f"duplicate {name}: {sorted(dup)}")
unique('control IDs', control_ids); unique('test IDs', test_ids)

for c in controls:
    if c['domain'] not in domain_ids: raise SystemExit(f"{c['id']}: unknown domain {c['domain']}")
    for tid in c['adversarial_tests']:
        if tid not in test_ids: raise SystemExit(f"{c['id']}: unknown test {tid}")
for t in tests:
    for cid in t['controls']:
        if cid not in control_ids: raise SystemExit(f"{t['id']}: unknown control {cid}")

# Require symmetric control↔test relationships.
test_map = {t['id']: set(t['controls']) for t in tests}
for c in controls:
    for tid in c['adversarial_tests']:
        if c['id'] not in test_map[tid]:
            raise SystemExit(f"{c['id']}: test {tid} does not map back to control")

for profile in profiles_doc['profiles']:
    for cid in profile['baseline_controls']:
        if cid not in control_ids:
            raise SystemExit(f"profile {profile['id']}: unknown control {cid}")

vr = verification_run_doc['verification_run']
if vr['test_id'] not in test_ids:
    raise SystemExit(f"verification-run template: unknown test {vr['test_id']}")
for cid in vr.get('control_ids', []):
    if cid not in control_ids:
        raise SystemExit(f"verification-run template: unknown control {cid}")

ac = assurance_case_doc['assurance_case']
for cid in ac['control_ids']:
    if cid not in control_ids:
        raise SystemExit(f"assurance-case template: unknown control {cid}")

vp = verification_plan_doc['verification_plan']
for cid in vp['control_ids']:
    if cid not in control_ids:
        raise SystemExit(f"verification-plan template: unknown control {cid}")
for tid in vp['test_ids']:
    if tid not in test_ids:
        raise SystemExit(f"verification-plan template: unknown test {tid}")

cc = conformance_claim_doc['conformance_claim']
for row in cc['control_results']:
    if row['control_id'] not in control_ids:
        raise SystemExit(f"conformance-claim template: unknown control {row['control_id']}")

scenario_ids=[x['test_id'] for x in scenario_doc['scenarios']]
if len(scenario_ids)!=len(set(scenario_ids)): raise SystemExit('duplicate execution scenario test IDs')
if set(scenario_ids)!=set(test_ids): raise SystemExit(f'execution scenario registry does not cover test catalog: missing={sorted(set(test_ids)-set(scenario_ids))} extra={sorted(set(scenario_ids)-set(test_ids))}')

if len(domains) != 10: raise SystemExit(f"expected 10 domains, got {len(domains)}")
if not (40 <= len(controls) <= 60): raise SystemExit(f"control count outside stable baseline design range: {len(controls)}")

print(f"OK: {len(domains)} domains, {len(controls)} controls, {len(tests)} tests, plan/evidence/conformance/target/gate/scenario artifacts verified")
