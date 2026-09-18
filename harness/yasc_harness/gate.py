from __future__ import annotations
from pathlib import Path
from typing import Any
from .catalog import test_map
from .util import load_data, write_data
from .evidence import sha256
from datetime import datetime, timezone

def _load_runs(path: str|Path) -> list[dict[str,Any]]:
    p=Path(path); files=[p] if p.is_file() else [x for x in p.rglob('*') if x.suffix.lower() in {'.yaml','.yml','.json'}]
    out=[]
    for f in files:
        try:d=load_data(f)
        except Exception:continue
        if isinstance(d,dict) and isinstance(d.get('verification_run'),dict): out.append(d['verification_run'])
    return out

def evaluate_gate(plan_doc: dict[str,Any], runs_path: str|Path, policy_doc: dict[str,Any]) -> dict[str,Any]:
    p=plan_doc['verification_plan']; pol=policy_doc['security_gate']; runs=_load_runs(runs_path); by_test={r.get('test_id'):r for r in runs}
    tests=test_map(); planned=list(p['test_ids']); executed=[tid for tid in planned if tid in by_test]
    coverage=len(executed)/len(planned) if planned else 1.0
    reasons=[]; fail_sev=set(pol.get('fail_on_severities',['critical','high']))
    min_cov=float(pol.get('minimum_test_coverage',1.0))
    if coverage < min_cov: reasons.append(f'test coverage {coverage:.1%} below required {min_cov:.1%}')
    missing_required=sorted(set(pol.get('required_tests',[]))-set(executed))
    if missing_required: reasons.append(f'missing required tests: {", ".join(missing_required)}')
    failures=[]; inconclusive=[]
    for tid in executed:
        r=by_test[tid]; sev=tests.get(tid,{}).get('severity','medium')
        if r.get('verdict')=='fail' and sev in fail_sev: failures.append({'test_id':tid,'severity':sev,'run_id':r.get('run_id')})
        if r.get('verdict')=='inconclusive': inconclusive.append(tid)
    if failures: reasons.append(f'{len(failures)} failing test(s) at gated severity')
    max_inc=int(pol.get('maximum_inconclusive',0))
    if len(inconclusive)>max_inc: reasons.append(f'{len(inconclusive)} inconclusive run(s), maximum is {max_inc}')
    integrity_failures=[]
    if pol.get('require_evidence_integrity', False):
        for r in runs:
            refs=r.get('evidence_refs',[])
            if not refs:
                integrity_failures.append({'run_id':r.get('run_id'),'reason':'no evidence reference'})
                continue
            for ref in refs:
                mp=Path(ref)
                if not mp.exists():
                    integrity_failures.append({'run_id':r.get('run_id'),'reason':f'missing manifest {ref}'})
                    continue
                try: manifest=load_data(mp)['evidence_manifest']
                except Exception as exc:
                    integrity_failures.append({'run_id':r.get('run_id'),'reason':f'invalid manifest {ref}: {exc}'})
                    continue
                base=mp.parent
                for a in manifest.get('artifacts',[]):
                    ap=base/a['path']
                    if not ap.exists() or sha256(ap).lower()!=str(a.get('sha256','')).lower():
                        integrity_failures.append({'run_id':r.get('run_id'),'reason':f'evidence integrity failure: {a.get("path")}'})
        if integrity_failures: reasons.append(f'{len(integrity_failures)} evidence integrity issue(s)')
    stale_runs=[]
    max_age=pol.get('maximum_evidence_age_hours')
    if max_age is not None:
        now=datetime.now(timezone.utc)
        for r in runs:
            ts=(r.get('integrity') or {}).get('collected_at')
            if not ts: stale_runs.append(r.get('run_id')); continue
            try:
                dt=datetime.fromisoformat(ts.replace('Z','+00:00'))
                if (now-dt).total_seconds()>float(max_age)*3600: stale_runs.append(r.get('run_id'))
            except Exception: stale_runs.append(r.get('run_id'))
        if stale_runs: reasons.append(f'{len(stale_runs)} stale or undated run(s) exceed evidence age policy')
    result={'gate':'pass' if not reasons else 'fail','plan_id':p['plan_id'],'planned_tests':len(planned),'executed_tests':len(executed),'test_coverage':round(coverage,4),'failures':failures,'inconclusive':inconclusive,'missing_tests':sorted(set(planned)-set(executed)),'integrity_failures':integrity_failures,'stale_runs':stale_runs,'reasons':reasons}
    return result

def gate_to_file(plan: str|Path, runs: str|Path, policy: str|Path, out: str|Path|None=None)->dict[str,Any]:
    result=evaluate_gate(load_data(plan),runs,load_data(policy))
    if out: write_data(out,result)
    return result
