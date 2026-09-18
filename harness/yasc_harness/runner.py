from __future__ import annotations
import re, traceback, json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from jsonschema import Draft202012Validator
from .adapters import make_agent_adapter, make_mcp_adapter
from .catalog import load_catalog, test_map
from .evidence import EvidenceCollector
from .util import get_path, load_data, write_data

def utcnow()->str: return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')

def _confusable_key(name:str)->str:
    # Conservative normalization for obvious separator/case collisions; not a full Unicode spoofing detector.
    return re.sub(r'[^a-z0-9]','',name.casefold())

def _assertion(spec: dict[str,Any], outputs: dict[str,Any]) -> tuple[bool,str]:
    typ=spec['type']; ref=outputs.get(spec.get('ref','last'))
    if typ=='no_tool_calls':
        calls=getattr(ref,'tool_calls',[]) if ref is not None else []; ok=len(calls)==0; return ok,f'tool_calls={len(calls)}'
    if typ=='has_tool_calls':
        calls=getattr(ref,'tool_calls',[]) if ref is not None else []; ok=len(calls)>0; return ok,f'tool_calls={len(calls)}'
    if typ=='text_matches':
        text=getattr(ref,'text','') if ref is not None else ''; ok=re.search(spec['pattern'],text,re.I) is not None; return ok,f'text={text[:160]!r}'
    if typ=='text_not_matches':
        text=getattr(ref,'text','') if ref is not None else ''; ok=re.search(spec['pattern'],text,re.I) is None; return ok,f'text={text[:160]!r}'
    if typ=='mcp_tool_names_unique':
        tools=ref or []; names=[t.get('name','') for t in tools]; ok=len(names)==len(set(names)); return ok,f'names={names}'
    if typ=='mcp_no_confusable_names':
        tools=ref or []; names=[t.get('name','') for t in tools]; keys=[_confusable_key(x) for x in names]; ok=len(keys)==len(set(keys)); return ok,f'names={names}'
    if typ=='json_path_equals':
        raw=getattr(ref,'raw',ref); actual=get_path(raw,spec['path']); ok=actual==spec.get('value'); return ok,f'{spec["path"]}={actual!r}'
    raise ValueError(f'unsupported assertion type: {typ}')

class TestRunner:
    __test__ = False
    def __init__(self, target_doc: dict[str,Any], scenarios: dict[str,dict[str,Any]], out_dir: str|Path, evidence_dir: str|Path):
        self.target_doc=target_doc['target']; self.scenarios=scenarios; self.out_dir=Path(out_dir); self.evidence_dir=Path(evidence_dir)
        self.out_dir.mkdir(parents=True,exist_ok=True); self.evidence_dir.mkdir(parents=True,exist_ok=True)
        self.agent=None; self.mcp=None
        if self.target_doc.get('agent'): self.agent=make_agent_adapter(self.target_doc['agent'])
        if self.target_doc.get('mcp'): self.mcp=make_mcp_adapter(self.target_doc['mcp'])
        self.tests=test_map(); self.controls,_,_=load_catalog()

    def close(self):
        for x in (self.agent,self.mcp):
            if x:
                try:x.close()
                except Exception:pass

    def _step(self, step: dict[str,Any], collector: EvidenceCollector, outputs: dict[str,Any]):
        action=step['action']; name=step.get('save_as','last')
        if action=='agent.send':
            if not self.agent: raise RuntimeError('scenario requires agent adapter but target has none')
            msg=step['message']; collector.event('agent.request',{'message':msg,'context':step.get('context')})
            res=self.agent.send(msg,context=step.get('context')); collector.event('agent.response',{'text':res.text,'tool_calls':res.tool_calls,'events':res.events,'metadata':res.metadata})
            outputs[name]=res; outputs['last']=res
        elif action=='agent.reset':
            if self.agent: self.agent.reset()
            collector.event('agent.reset',{})
        elif action=='mcp.initialize':
            if not self.mcp: raise RuntimeError('scenario requires MCP adapter but target has none')
            res=self.mcp.initialize(); collector.event('mcp.initialize',res); outputs[name]=res; outputs['last']=res
        elif action=='mcp.list_tools':
            if not self.mcp: raise RuntimeError('scenario requires MCP adapter but target has none')
            res=self.mcp.list_tools(); collector.event('mcp.tools.list',res); outputs[name]=res; outputs['last']=res
        elif action=='mcp.call_tool':
            if not self.mcp: raise RuntimeError('scenario requires MCP adapter but target has none')
            res=self.mcp.call_tool(step['name'],step.get('arguments',{})); collector.event('mcp.tools.call',{'name':step['name'],'arguments':step.get('arguments',{}),'result':res}); outputs[name]=res; outputs['last']=res
        else: raise ValueError(f'unsupported scenario action: {action}')

    def run_test(self, test_id: str, *, plan_id: str, environment: str='staging') -> dict[str,Any]:
        if test_id not in self.tests: raise ValueError(f'unknown test: {test_id}')
        test=self.tests[test_id]; scenario=self.scenarios.get(test_id)
        if not scenario: return {'test_id':test_id,'status':'not-automated','reason':'no executable scenario is registered'}
        if scenario.get('mode','automated')!='automated': return {'test_id':test_id,'status':'not-automated','reason':scenario.get('reason','scenario is guided/manual')}
        run_id=f"YVR-{test_id}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')}"
        collector=EvidenceCollector(self.evidence_dir,run_id,sensitivity=scenario.get('sensitivity','confidential'))
        outputs:dict[str,Any]={}; assertion_results=[]; started=utcnow(); verdict='inconclusive'; error=None
        trials=int(scenario.get('trials',1)); security_failures=0
        try:
            for trial in range(trials):
                if trial and scenario.get('reset_between_trials',True) and self.agent: self.agent.reset()
                collector.event('trial.start',{'trial':trial+1})
                for step in scenario.get('steps',[]): self._step(step,collector,outputs)
                trial_failed=False
                for a in scenario.get('assertions',[]):
                    ok,detail=_assertion(a,outputs); assertion_results.append({'trial':trial+1,'assertion':a,'passed':ok,'detail':detail}); collector.event('assertion',assertion_results[-1])
                    if not ok: trial_failed=True
                if trial_failed: security_failures+=1
            verdict='pass' if security_failures==0 else 'fail'
        except Exception as exc:
            error=f'{type(exc).__name__}: {exc}'; collector.event('runner.error',{'error':error,'traceback':traceback.format_exc(limit=8)}); verdict='inconclusive'
        manifest=collector.finalize(case_id=run_id)
        versions={'yasc':self.controls['metadata']['version'],'application':self.target_doc.get('version','unspecified'),'model':self.target_doc.get('model','unspecified'),'prompt_config_hash':self.target_doc.get('prompt_config_hash','unspecified'),'policy':self.target_doc.get('policy_version','unspecified'),'tooling':self.target_doc.get('tooling_versions',[])}
        run={'verification_run':{
            'schema_version':'1.0','run_id':run_id,'plan_id':plan_id,'test_id':test_id,'control_ids':test['controls'],
            'system':{'name':self.target_doc.get('name','unnamed-target')},'environment':environment,
            'scope':{'notes':scenario.get('scope','Executable scenario against configured target adapter.')},'versions':versions,
            'determinism':'deterministic' if self.target_doc.get('deterministic',False) else 'unknown',
            'oracle':{'source':'executable scenario assertions','failure_condition':test['expected_result']},
            'trials':{'n':trials,'security_failures':security_failures,'state_reset_between_trials':bool(scenario.get('reset_between_trials',True)),'variant_set':scenario.get('variant_set','scenario-defined')},
            'verdict':verdict,'observations':assertion_results + ([{'error':error}] if error else []),'measurements':{},
            'evidence_refs':[str((self.evidence_dir/run_id/'evidence-manifest.yaml').as_posix())],
            'integrity':{'collected_at':started,'collector':'YASC Verification Harness 1.0','artifact_hashes':[a['sha256'] for a in manifest['evidence_manifest']['artifacts']]},
            'quality':{'environment_fidelity':environment,'independence':'self-review','oracle_strength':'application-observation'},
            'revalidation_triggers':['material system/model/policy/tool/identity change']}}
        schema=json.loads((Path(__file__).resolve().parents[2]/'schema/verification-run.schema.json').read_text(encoding='utf-8'))
        errs=list(Draft202012Validator(schema).iter_errors(run))
        if errs: raise RuntimeError('generated verification-run failed schema validation: '+ '; '.join(e.message for e in errs[:5]))
        path=self.out_dir/f'{run_id}.yaml'; write_data(path,run)
        return {'test_id':test_id,'status':'executed','verdict':verdict,'run_id':run_id,'run_path':str(path),'evidence_dir':str(self.evidence_dir/run_id)}

    def run_plan(self, plan_doc: dict[str,Any], *, only: list[str]|None=None) -> dict[str,Any]:
        p=plan_doc['verification_plan']; selected=[x for x in p['test_ids'] if not only or x in set(only)]
        results=[]
        for tid in selected: results.append(self.run_test(tid,plan_id=p['plan_id'],environment=p.get('environment','staging')))
        return {'plan_id':p['plan_id'],'target':self.target_doc.get('name'),'results':results}
