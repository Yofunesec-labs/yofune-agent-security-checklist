from __future__ import annotations
import base64, html
from collections import Counter
from pathlib import Path
from typing import Any
from .catalog import test_map, control_map, load_catalog
from .assessment import build_assessment
from .util import load_data

ROOT=Path(__file__).resolve().parents[2]

def _runs(path: str|Path)->list[dict[str,Any]]:
    p=Path(path); files=[p] if p.is_file() else [x for x in p.rglob('*') if x.suffix.lower() in {'.yaml','.yml','.json'}]
    out=[]
    for f in files:
        try:d=load_data(f)
        except Exception:continue
        if isinstance(d,dict) and d.get('verification_run'): out.append(d['verification_run'])
    return sorted(out,key=lambda r:r.get('test_id',''))

def _logo_uri()->str:
    p=ROOT/'assets/brand/yofune-mark-transparent.png'
    if not p.exists(): return ''
    return 'data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode()

def build_html(plan_doc: dict[str,Any], runs_path: str|Path, *, gate_result:dict[str,Any]|None=None, title:str|None=None)->str:
    runs=_runs(runs_path); tests=test_map(); controls=control_map(); cdoc,_,_=load_catalog(); p=plan_doc['verification_plan']; by={r['test_id']:r for r in runs}
    counts=Counter(r.get('verdict','unknown') for r in runs); planned=p['test_ids']; coverage=len(set(planned)&set(by))/len(planned) if planned else 1
    assessment=build_assessment(plan_doc,runs_path)['assessment']
    control_rows=[]
    for cid in p['control_ids']:
        c=controls.get(cid,{})
        ar=assessment['results'].get(cid,{})
        status=ar.get('status','not-tested'); cls={'pass':'pass','fail':'fail','partial':'warn'}.get(status,'muted')
        control_rows.append(f"<tr><td><code>{html.escape(cid)}</code><br><span class='muted'>{html.escape(c.get('title',''))}</span></td><td>{html.escape(c.get('severity',''))}</td><td class='{cls}'>{html.escape(status.upper())}</td><td>{html.escape(ar.get('achieved_assurance','YAL-0'))}</td><td class='small'>{html.escape(', '.join(ar.get('executed_tests',[])))}</td></tr>")
    rows=[]
    for tid in planned:
        r=by.get(tid); t=tests.get(tid,{})
        verdict=r.get('verdict') if r else 'not-tested'
        cls={'pass':'pass','fail':'fail','inconclusive':'warn'}.get(verdict,'muted')
        controls_txt=', '.join(t.get('controls',[]))
        evidence='<br>'.join(html.escape(Path(x).name) for x in (r.get('evidence_refs',[]) if r else []))
        rows.append(f"<tr><td><code>{html.escape(tid)}</code><br><span class='muted'>{html.escape(t.get('title',''))}</span></td><td>{html.escape(t.get('severity',''))}</td><td class='{cls}'>{html.escape(verdict.upper())}</td><td>{html.escape(controls_txt)}</td><td class='small'>{evidence}</td></tr>")
    scope=p.get('scope',{})
    scope_parts=[]
    for label,key in [('Included','included'),('Excluded','excluded'),('High-impact actions','high_impact_actions'),('Trust boundaries','trust_boundaries')]:
        vals=scope.get(key,[]) if isinstance(scope,dict) else []
        if vals: scope_parts.append('<b>'+label+':</b><ul>'+''.join('<li>'+html.escape(str(v))+'</li>' for v in vals)+'</ul>')
    scope_html=''.join(scope_parts) or html.escape(str(scope))
    gate_html=''
    if gate_result:
        cls='pass' if gate_result.get('gate')=='pass' else 'fail'
        reasons='; '.join(gate_result.get('reasons',[])) or 'All configured security-gate conditions were satisfied.'
        gate_html=f"<div class='gate {cls}'><b>CI Security Gate: {gate_result.get('gate','unknown').upper()}</b><br>{html.escape(reasons)}</div>"
    return f'''<!doctype html><html><head><meta charset="utf-8"><title>{html.escape(title or 'YASC Assessment Report')}</title><style>
@page {{ size:A4; margin:16mm 14mm 18mm; @bottom-center {{ content:"Yofune Security Research | yofunesec.com | contact@yofunesec.com"; font-size:8px; color:#6e7984; }} }}
:root{{--brand:#344658;--muted:#6e7984;--line:#dce2e7;--pass:#157347;--fail:#b02a37;--warn:#946200}}body{{font-family:Arial,"Noto Sans",sans-serif;color:#222;margin:0;line-height:1.45}}header{{display:flex;gap:18px;align-items:center;border-bottom:3px solid var(--brand);padding-bottom:14px;margin-bottom:20px}}header img{{width:74px;height:74px;object-fit:contain}}h1{{color:var(--brand);margin:0;font-size:26px}}h2{{color:var(--brand);margin-top:26px}}.muted{{color:var(--muted)}}.cards{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:18px 0}}.card{{border:1px solid var(--line);padding:12px;border-radius:6px}}.card b{{display:block;font-size:22px;color:var(--brand)}}table{{width:100%;border-collapse:collapse;font-size:10px}}thead{{display:table-header-group}}tr{{break-inside:avoid;page-break-inside:avoid}}th,td{{border-bottom:1px solid var(--line);padding:7px;vertical-align:top;text-align:left}}th{{background:#f3f5f7;color:var(--brand)}}.pass{{color:var(--pass);font-weight:bold}}.fail{{color:var(--fail);font-weight:bold}}.warn{{color:var(--warn);font-weight:bold}}.small{{font-size:8px;word-break:break-all}}.gate{{padding:12px;border-left:5px solid;margin:14px 0;background:#f7f8f9}}.gate.pass{{border-color:var(--pass)}}.gate.fail{{border-color:var(--fail)}}code{{font-size:9px}}footer{{margin-top:28px;border-top:1px solid var(--line);padding-top:10px;color:var(--muted);font-size:9px}}
</style></head><body><header><img src="{_logo_uri()}"><div><h1>{html.escape(title or 'YASC Assessment Report')}</h1><div class="muted">Yofune Agent Security Checklist v{html.escape(cdoc['metadata']['version'])}</div><div class="muted">{html.escape(p.get('system',{}).get('name','Assessment target'))} | Plan {html.escape(p['plan_id'])}</div></div></header>{gate_html}
<div class="cards"><div class="card"><span>Planned tests</span><b>{len(planned)}</b></div><div class="card"><span>Executed</span><b>{len(runs)}</b></div><div class="card"><span>Coverage</span><b>{coverage:.0%}</b></div><div class="card"><span>Failures</span><b>{counts.get('fail',0)}</b></div></div>
<h2>Scope</h2><div>{scope_html}</div><h2>Control assessment</h2><table><thead><tr><th>Control</th><th>Severity</th><th>Status</th><th>Assurance</th><th>Executed tests</th></tr></thead><tbody>{''.join(control_rows)}</tbody></table>
<h2>Verification results</h2><table><thead><tr><th>Test</th><th>Severity</th><th>Verdict</th><th>Mapped controls</th><th>Evidence</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
<h2>Interpretation</h2><p>This report is a bounded statement about the configured target, plan, environment, executable scenarios, and collected evidence. A PASS is not a universal claim that the agent is secure. Material changes to model, policy, identity, tools, MCP servers, memory, or deployment state can require revalidation.</p>
</body></html>'''

def write_report(plan: str|Path, runs: str|Path, html_out: str|Path, *, pdf_out: str|Path|None=None, gate:dict[str,Any]|None=None, title:str|None=None)->tuple[Path,Path|None]:
    doc=load_data(plan); content=build_html(doc,runs,gate_result=gate,title=title); hp=Path(html_out); hp.parent.mkdir(parents=True,exist_ok=True); hp.write_text(content,encoding='utf-8')
    pp=None
    if pdf_out:
        try:
            from weasyprint import HTML
        except Exception as exc:
            raise RuntimeError('PDF generation requires WeasyPrint (pip install yasc-verification-harness[pdf])') from exc
        pp=Path(pdf_out); pp.parent.mkdir(parents=True,exist_ok=True); HTML(string=content,base_url=str(ROOT)).write_pdf(str(pp))
    return hp,pp
