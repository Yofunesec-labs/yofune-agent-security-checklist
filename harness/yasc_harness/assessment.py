from __future__ import annotations
from pathlib import Path
from typing import Any
from .catalog import control_map, load_catalog
from .util import load_data, write_data
import json
from jsonschema import Draft202012Validator

def _load_runs(path:str|Path)->list[dict[str,Any]]:
    p=Path(path); files=[p] if p.is_file() else [x for x in p.rglob('*') if x.suffix.lower() in {'.yaml','.yml','.json'}]
    runs=[]
    for f in files:
        try:d=load_data(f)
        except Exception:continue
        if isinstance(d,dict) and d.get('verification_run'):runs.append(d['verification_run'])
    return runs

def build_assessment(plan_doc:dict[str,Any],runs_path:str|Path)->dict[str,Any]:
    p=plan_doc['verification_plan']; runs=_load_runs(runs_path); by_test={r.get('test_id'):r for r in runs}; cmap=control_map(); cdoc,_,_=load_catalog(); results={}
    for cid in p['control_ids']:
        c=cmap[cid]; planned=[tid for tid in p['test_ids'] if tid in set(c.get('adversarial_tests',[]))]; executed=[by_test[tid] for tid in planned if tid in by_test]
        verdicts=[r.get('verdict') for r in executed]
        if not planned or not executed:
            status='not-tested'; yal='YAL-0'
        elif 'fail' in verdicts:
            status='fail'; yal='YAL-3' if any(r.get('evidence_refs') for r in executed) else 'YAL-2'
        elif 'inconclusive' in verdicts or len(executed)<len(planned):
            status='partial'; yal='YAL-3' if executed else 'YAL-0'
        elif all(v=='pass' for v in verdicts):
            status='pass'; yal='YAL-4'
        else:
            status='partial'; yal='YAL-2'
        ev=[e for r in executed for e in r.get('evidence_refs',[])]
        results[cid]={'applicability':'applicable','status':status,'achieved_assurance':yal,'evidence_refs':ev,'planned_tests':planned,'executed_tests':[r.get('test_id') for r in executed]}
    return {'assessment':{'schema_version':'1.0','yasc_version':cdoc['metadata']['version'],'reference_snapshot':cdoc['metadata'].get('snapshot_date',''),'system':{'name':p.get('system',{}).get('name','Assessment target'),'environment':p.get('environment','unspecified')},'scope':p.get('scope',{}),'results':results}}

def write_assessment(plan:str|Path,runs:str|Path,out:str|Path)->dict[str,Any]:
    result=build_assessment(load_data(plan),runs)
    schema=json.loads((Path(__file__).resolve().parents[2]/'schema/assessment.schema.json').read_text(encoding='utf-8'))
    errs=list(Draft202012Validator(schema).iter_errors(result))
    if errs: raise RuntimeError('generated assessment failed schema validation: '+ '; '.join(e.message for e in errs[:5]))
    write_data(out,result); return result
