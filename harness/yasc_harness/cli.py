from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from jsonschema import Draft202012Validator
from .catalog import load_catalog
from .assessment import write_assessment
from .adapters import make_mcp_adapter
from .catalog import test_map
from .evidence import sha256
from .gate import gate_to_file
from .report import write_report
from .runner import TestRunner
from .scenarios import load_scenarios
from .util import load_data, write_data

ROOT=Path(__file__).resolve().parents[2]

def validate_schema(doc, schema_path: Path, label: str):
    schema=json.loads(schema_path.read_text(encoding='utf-8'))
    errs=sorted(Draft202012Validator(schema).iter_errors(doc),key=lambda e:list(e.path))
    if errs:
        for e in errs: print(f'{label}: {list(e.path)}: {e.message}',file=sys.stderr)
        raise SystemExit(2)


def cmd_scenario_init(args):
    tests=test_map()
    if args.test_id not in tests: raise SystemExit(f"unknown test: {args.test_id}")
    t=tests[args.test_id]
    doc={"schema_version":"1.0","scenarios":[{"test_id":args.test_id,"mode":"automated","scope":"Describe the exact authorized target path and fixtures.","trials":1,"reset_between_trials":True,"variant_set":"target-specific","sensitivity":"confidential","steps":[{"action":"agent.send","message":"REPLACE-WITH-AUTHORIZED-SYNTHETIC-PROBE","save_as":"attack"}],"assertions":[{"type":"no_tool_calls","ref":"attack"}],"notes":{"catalog_procedure":t.get("procedure",[]),"expected_result":t.get("expected_result","")}}]}
    write_data(args.out,doc); print(args.out)

def cmd_mcp_list(args):
    target=load_data(args.target); validate_schema(target,ROOT/'schema/target.schema.json','target')
    cfg=target['target'].get('mcp')
    if not cfg: raise SystemExit('target has no MCP adapter configuration')
    a=make_mcp_adapter(cfg)
    try: result=a.list_tools()
    finally: a.close()
    print(json.dumps(result,indent=2,ensure_ascii=False))

def cmd_mcp_call(args):
    target=load_data(args.target); validate_schema(target,ROOT/'schema/target.schema.json','target')
    cfg=target['target'].get('mcp')
    if not cfg: raise SystemExit('target has no MCP adapter configuration')
    arguments=json.loads(args.arguments)
    a=make_mcp_adapter(cfg)
    try: result=a.call_tool(args.name,arguments)
    finally: a.close()
    print(json.dumps(result,indent=2,ensure_ascii=False))

def cmd_summary(_):
    c,t,p=load_catalog(); print(json.dumps({'version':c['metadata']['version'],'domains':len(c['domains']),'controls':len(c['controls']),'tests':len(t['tests']),'profiles':len(p['profiles']),'harness':'1.0.0'},indent=2))

def cmd_plan_check(args):
    doc=load_data(args.plan); validate_schema(doc,ROOT/'schema/verification-plan.schema.json','verification-plan')
    c,t,_=load_catalog(); cids={x['id'] for x in c['controls']}; tids={x['id'] for x in t['tests']}; p=doc['verification_plan']
    uc=sorted(set(p['control_ids'])-cids); ut=sorted(set(p['test_ids'])-tids)
    if uc or ut: raise SystemExit(f'unknown references controls={uc} tests={ut}')
    print(f"OK: plan {p['plan_id']} — {len(p['control_ids'])} controls, {len(p['test_ids'])} tests")

def cmd_target_check(args):
    doc=load_data(args.target); validate_schema(doc,ROOT/'schema/target.schema.json','target'); print(f"OK: target {doc['target']['name']}")

def cmd_run(args):
    plan=load_data(args.plan); target=load_data(args.target); validate_schema(plan,ROOT/'schema/verification-plan.schema.json','verification-plan'); validate_schema(target,ROOT/'schema/target.schema.json','target')
    scenario_paths=args.scenarios or [ROOT/'harness/scenarios/core.yaml']
    for sp in scenario_paths:
        validate_schema(load_data(sp),ROOT/'schema/execution-scenarios.schema.json','execution-scenarios')
    scenarios=load_scenarios(scenario_paths)
    r=TestRunner(target,scenarios,args.out,args.evidence)
    try: summary=r.run_plan(plan,only=args.test)
    finally: r.close()
    if args.summary: write_data(args.summary,summary)
    print(json.dumps(summary,indent=2));
    if args.exit_nonzero_on_fail and any(x.get('verdict')=='fail' for x in summary['results']): raise SystemExit(20)

def _iter_runs(path:Path):
    files=[path] if path.is_file() else [x for x in path.rglob('*') if x.suffix.lower() in {'.yaml','.yml','.json'}]
    for p in files:
        try:d=load_data(p)
        except Exception:continue
        if isinstance(d,dict) and d.get('verification_run'): yield d['verification_run']

def cmd_coverage(args):
    p=load_data(args.plan)['verification_plan']; runs=list(_iter_runs(Path(args.runs))); planned=set(p['test_ids']); executed={r.get('test_id') for r in runs}; pc=set(p['control_ids']); cc={cid for r in runs for cid in r.get('control_ids',[])}
    v={}
    for r in runs:v[r.get('verdict','unknown')]=v.get(r.get('verdict','unknown'),0)+1
    report={'plan_id':p['plan_id'],'planned_tests':len(planned),'executed_planned_tests':len(planned&executed),'test_coverage':round(len(planned&executed)/len(planned),4) if planned else 1.0,'missing_tests':sorted(planned-executed),'unplanned_executed_tests':sorted(executed-planned),'planned_controls':len(pc),'controls_with_run_evidence':len(pc&cc),'control_run_coverage':round(len(pc&cc)/len(pc),4) if pc else 1.0,'verdict_counts':v,'run_count':len(runs)}
    if args.out:write_data(args.out,report)
    print(json.dumps(report,indent=2))

def cmd_gate(args):
    validate_schema(load_data(args.policy),ROOT/'schema/gate-policy.schema.json','gate-policy')
    result=gate_to_file(args.plan,args.runs,args.policy,args.out); print(json.dumps(result,indent=2));
    if result['gate']!='pass': raise SystemExit(10)

def cmd_assess(args):
    result=write_assessment(args.plan,args.runs,args.out); print(json.dumps(result,indent=2))

def cmd_report(args):
    gate=None
    if args.gate_result: gate=load_data(args.gate_result)
    hp,pp=write_report(args.plan,args.runs,args.html,pdf_out=args.pdf,gate=gate,title=args.title); print(hp); print(pp or '')

def cmd_manifest(args):
    base=Path(args.directory).resolve(); files=[p for p in sorted(base.rglob('*')) if p.is_file() and p.name!='evidence-manifest.yaml']
    if not files: raise SystemExit('evidence directory contains no files')
    from datetime import datetime,timezone
    now=datetime.now(timezone.utc).isoformat().replace('+00:00','Z'); arts=[]
    for i,p in enumerate(files,1):arts.append({'artifact_id':f'EV-{i:03d}','type':p.suffix.lstrip('.') or 'file','path':p.relative_to(base).as_posix(),'sha256':sha256(p),'size_bytes':p.stat().st_size,'sensitivity':args.sensitivity,'redaction':'caller-managed'})
    obj={'evidence_manifest':{'schema_version':'1.0','manifest_id':args.manifest_id or f'YEM-{now[:10]}','generated_at':now,'case_id':args.case_id,'collector':args.collector,'hash_algorithm':'sha256','artifacts':arts}}
    validate_schema(obj,ROOT/'schema/evidence-manifest.schema.json','evidence-manifest'); write_data(args.out,obj); print(args.out)

def cmd_verify_manifest(args):
    m=load_data(args.manifest); validate_schema(m,ROOT/'schema/evidence-manifest.schema.json','evidence-manifest'); base=Path(args.base_dir).resolve(); bad=[]
    for a in m['evidence_manifest']['artifacts']:
        p=base/a['path'];
        if not p.exists():bad.append((a['path'],'missing'));continue
        if sha256(p).lower()!=a['sha256'].lower():bad.append((a['path'],'hash-mismatch'))
    if bad:
        for x in bad:print(f'{x[0]}: {x[1]}',file=sys.stderr)
        raise SystemExit(3)
    print(f"OK: {len(m['evidence_manifest']['artifacts'])} evidence artifacts verified")

def build_parser():
    p=argparse.ArgumentParser(prog='yasc',description='YASC Verification Harness 1.0')
    s=p.add_subparsers(dest='cmd',required=True)
    x=s.add_parser('summary');x.set_defaults(func=cmd_summary)
    x=s.add_parser('scenario-init');x.add_argument('test_id');x.add_argument('--out',required=True);x.set_defaults(func=cmd_scenario_init)
    x=s.add_parser('mcp-list');x.add_argument('--target',required=True);x.set_defaults(func=cmd_mcp_list)
    x=s.add_parser('mcp-call');x.add_argument('--target',required=True);x.add_argument('--name',required=True);x.add_argument('--arguments',default='{}');x.set_defaults(func=cmd_mcp_call)
    x=s.add_parser('plan-check');x.add_argument('plan');x.set_defaults(func=cmd_plan_check)
    x=s.add_parser('target-check');x.add_argument('target');x.set_defaults(func=cmd_target_check)
    x=s.add_parser('run');x.add_argument('--plan',required=True);x.add_argument('--target',required=True);x.add_argument('--scenarios',action='append');x.add_argument('--test',action='append');x.add_argument('--out',default='runs');x.add_argument('--evidence',default='evidence');x.add_argument('--summary');x.add_argument('--exit-nonzero-on-fail',action='store_true');x.set_defaults(func=cmd_run)
    x=s.add_parser('coverage');x.add_argument('--plan',required=True);x.add_argument('--runs',required=True);x.add_argument('--out');x.set_defaults(func=cmd_coverage)
    x=s.add_parser('gate');x.add_argument('--plan',required=True);x.add_argument('--runs',required=True);x.add_argument('--policy',required=True);x.add_argument('--out');x.set_defaults(func=cmd_gate)
    x=s.add_parser('assess');x.add_argument('--plan',required=True);x.add_argument('--runs',required=True);x.add_argument('--out',required=True);x.set_defaults(func=cmd_assess)
    x=s.add_parser('report');x.add_argument('--plan',required=True);x.add_argument('--runs',required=True);x.add_argument('--html',required=True);x.add_argument('--pdf');x.add_argument('--gate-result');x.add_argument('--title');x.set_defaults(func=cmd_report)
    x=s.add_parser('manifest');x.add_argument('directory');x.add_argument('--case-id',required=True);x.add_argument('--out',required=True);x.add_argument('--manifest-id');x.add_argument('--collector',default='YASC verifier');x.add_argument('--sensitivity',choices=['public','internal','confidential','restricted','unspecified'],default='confidential');x.set_defaults(func=cmd_manifest)
    x=s.add_parser('verify-manifest');x.add_argument('manifest');x.add_argument('--base-dir',required=True);x.set_defaults(func=cmd_verify_manifest)
    return p

def main(argv=None):
    args=build_parser().parse_args(argv); args.func(args)

if __name__=='__main__':main()
