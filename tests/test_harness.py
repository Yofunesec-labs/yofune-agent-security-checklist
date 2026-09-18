from __future__ import annotations
import json, sys
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'harness'))

from yasc_harness.adapters import make_mcp_adapter
from yasc_harness.assessment import build_assessment
from yasc_harness.gate import evaluate_gate
from yasc_harness.report import build_html
from yasc_harness.runner import TestRunner
from yasc_harness.scenarios import load_scenarios
from yasc_harness.util import load_data

PLAN=load_data(ROOT/'examples/plans/smoke.yaml')
SCENARIOS=load_scenarios([ROOT/'harness/scenarios/core.yaml'])
POLICY=load_data(ROOT/'examples/gate-policy.yaml')

def _run(tmp_path:Path,target_name:str):
    target=load_data(ROOT/f'examples/targets/{target_name}.yaml')
    runner=TestRunner(target,SCENARIOS,tmp_path/'runs',tmp_path/'evidence')
    try: summary=runner.run_plan(PLAN)
    finally: runner.close()
    return summary

def test_secure_mock_runner_and_gate(tmp_path):
    summary=_run(tmp_path,'mock-secure')
    assert all(x['verdict']=='pass' for x in summary['results'])
    gate=evaluate_gate(PLAN,tmp_path/'runs',POLICY)
    assert gate['gate']=='pass'
    assert gate['test_coverage']==1.0
    assert not gate['integrity_failures']

def test_insecure_mock_runner_fails_gate(tmp_path):
    summary=_run(tmp_path,'mock-insecure')
    assert any(x['verdict']=='fail' for x in summary['results'])
    gate=evaluate_gate(PLAN,tmp_path/'runs',POLICY)
    assert gate['gate']=='fail'
    assert gate['failures']

def test_assessment_and_report(tmp_path):
    _run(tmp_path,'mock-secure')
    assessment=build_assessment(PLAN,tmp_path/'runs')
    assert assessment['assessment']['results']['YAS-02.01']['status']=='pass'
    assert assessment['assessment']['results']['YAS-02.01']['achieved_assurance']=='YAL-4'
    html=build_html(PLAN,tmp_path/'runs',gate_result=evaluate_gate(PLAN,tmp_path/'runs',POLICY))
    assert 'YASC Assessment Report' in html
    assert 'CI Security Gate: PASS' in html
    assert 'Chengdu Yofune Ariake Technology Co., Ltd.' not in html or 'yofunesec.com' in html

def test_mcp_stdio_adapter_fixture():
    cfg=load_data(ROOT/'examples/targets/mcp-stdio.yaml')['target']['mcp']
    adapter=make_mcp_adapter(cfg)
    try:
        tools=adapter.list_tools()
        assert [x['name'] for x in tools]==['echo']
        result=adapter.call_tool('echo',{'text':'hello'})
        assert result['content'][0]['text']=='hello'
    finally: adapter.close()

def test_core_scenario_registry_covers_catalog():
    tests=yaml.safe_load((ROOT/'schema/tests.yaml').read_text(encoding='utf-8'))['tests']
    assert {t['id'] for t in tests}==set(SCENARIOS)
    assert sum(1 for s in SCENARIOS.values() if s['mode']=='automated')>=4

def test_http_agent_adapter_local_fixture():
    import threading
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    from yasc_harness.adapters.http_agent import HTTPAgentAdapter
    class H(BaseHTTPRequestHandler):
        def log_message(self,*a): pass
        def do_POST(self):
            n=int(self.headers.get('Content-Length','0')); payload=json.loads(self.rfile.read(n) or b'{}')
            body=json.dumps({'output':{'text':'blocked safely'},'trace':{'tool_calls':[],'events':[{'type':'policy_decision','decision':'deny'}]},'seen':payload}).encode()
            self.send_response(200); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
    srv=ThreadingHTTPServer(('127.0.0.1',0),H); th=threading.Thread(target=srv.serve_forever,daemon=True); th.start()
    try:
        a=HTTPAgentAdapter({'type':'http-agent','url':f'http://127.0.0.1:{srv.server_port}/run','request':{'input_field':'message'},'response':{'text_path':'output.text','tool_calls_path':'trace.tool_calls','events_path':'trace.events'}})
        try:r=a.send('hello')
        finally:a.close()
        assert r.text=='blocked safely' and r.tool_calls==[] and r.events[0]['decision']=='deny'
    finally:
        srv.shutdown(); srv.server_close()


def test_mcp_http_adapter_local_fixture():
    import threading
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    from yasc_harness.adapters.mcp import HTTPMCPAdapter
    class H(BaseHTTPRequestHandler):
        def log_message(self,*a): pass
        def do_POST(self):
            n=int(self.headers.get('Content-Length','0')); req=json.loads(self.rfile.read(n) or b'{}'); method=req.get('method'); rid=req.get('id')
            if rid is None:
                self.send_response(202); self.end_headers(); return
            if method=='server/discover': result={'supportedVersions':['2026-07-28','2025-11-25'],'capabilities':{'tools':{'listChanged':False}}}
            elif method=='initialize': result={'protocolVersion':'2025-11-25','capabilities':{'tools':{}},'serverInfo':{'name':'http-fixture','version':'1.0'}}
            elif method=='tools/list': result={'tools':[{'name':'echo','inputSchema':{'type':'object'}}]}
            elif method=='tools/call': result={'content':[{'type':'text','text':req.get('params',{}).get('arguments',{}).get('text','')}],'isError':False}
            else: result={}
            body=json.dumps({'jsonrpc':'2.0','id':rid,'result':result}).encode()
            self.send_response(200); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
    srv=ThreadingHTTPServer(('127.0.0.1',0),H); th=threading.Thread(target=srv.serve_forever,daemon=True); th.start()
    try:
        a=HTTPMCPAdapter({'type':'mcp-http','url':f'http://127.0.0.1:{srv.server_port}/mcp'})
        try:
            assert a.era=='modern'
            assert a.list_tools()[0]['name']=='echo'
            assert a.call_tool('echo',{'text':'http-mcp'})['content'][0]['text']=='http-mcp'
        finally:a.close()
    finally:
        srv.shutdown(); srv.server_close()


def test_openai_responses_adapter_local_fixture():
    import threading
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    from yasc_harness.adapters.openai_responses import OpenAIResponsesAdapter

    seen = {}
    class H(BaseHTTPRequestHandler):
        def log_message(self,*a): pass
        def do_POST(self):
            n=int(self.headers.get('Content-Length','0')); req=json.loads(self.rfile.read(n) or b'{}')
            seen['auth']=self.headers.get('Authorization'); seen['body']=req
            body=json.dumps({
                'id':'resp_test','model':req.get('model'),'status':'completed',
                'output_text':'',
                'output':[
                    {'type':'message','content':[{'type':'output_text','text':'policy held'}]},
                    {'type':'function_call','id':'fc_1','call_id':'call_1','name':'send_email','arguments':'{"to":"external@example.test"}','status':'completed'},
                ],
                'usage':{'input_tokens':10,'output_tokens':5},
            }).encode()
            self.send_response(200); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
    srv=ThreadingHTTPServer(('127.0.0.1',0),H); th=threading.Thread(target=srv.serve_forever,daemon=True); th.start()
    try:
        a=OpenAIResponsesAdapter({'type':'openai-responses','model':'gpt-test','api_key':'test-secret','base_url':f'http://127.0.0.1:{srv.server_port}/v1','tools':[]})
        try:r=a.send('hello')
        finally:a.close()
        assert seen['auth']=='Bearer test-secret'
        assert seen['body']['model']=='gpt-test'
        assert r.text=='policy held'
        assert r.tool_calls[0]['name']=='send_email'
        assert r.tool_calls[0]['arguments']['to']=='external@example.test'
        assert r.metadata['provider']=='openai'
    finally:
        srv.shutdown(); srv.server_close()


def test_anthropic_messages_adapter_local_fixture():
    import threading
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    from yasc_harness.adapters.anthropic_messages import AnthropicMessagesAdapter

    seen = {}
    class H(BaseHTTPRequestHandler):
        def log_message(self,*a): pass
        def do_POST(self):
            n=int(self.headers.get('Content-Length','0')); req=json.loads(self.rfile.read(n) or b'{}')
            seen['key']=self.headers.get('x-api-key'); seen['version']=self.headers.get('anthropic-version'); seen['body']=req
            body=json.dumps({
                'id':'msg_test','model':req.get('model'),'stop_reason':'tool_use',
                'content':[
                    {'type':'text','text':'approval required'},
                    {'type':'tool_use','id':'toolu_1','name':'delete_record','input':{'id':'123'}},
                ],
                'usage':{'input_tokens':12,'output_tokens':7},
            }).encode()
            self.send_response(200); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
    srv=ThreadingHTTPServer(('127.0.0.1',0),H); th=threading.Thread(target=srv.serve_forever,daemon=True); th.start()
    try:
        a=AnthropicMessagesAdapter({'type':'anthropic-messages','model':'claude-test','api_key':'test-secret','base_url':f'http://127.0.0.1:{srv.server_port}/v1','max_tokens':256})
        try:r=a.send('hello')
        finally:a.close()
        assert seen['key']=='test-secret' and seen['version']=='2023-06-01'
        assert seen['body']['messages'][0]['content']=='hello'
        assert r.text=='approval required'
        assert r.tool_calls[0]['name']=='delete_record'
        assert r.tool_calls[0]['arguments']=={'id':'123'}
        assert r.metadata['provider']=='anthropic'
    finally:
        srv.shutdown(); srv.server_close()


def test_langgraph_import_adapter_fixture():
    from yasc_harness.adapters.langgraph import LangGraphAdapter
    a=LangGraphAdapter({'type':'langgraph','graph':'tests.fixtures.framework_targets:graph','thread_id':'auto'})
    try:
        r=a.send('CALL_TOOL')
        first_thread=r.metadata['thread_id']
        assert r.tool_calls[0]['name']=='safe_lookup'
        a.reset()
        r2=a.send('normal')
        assert r2.text=='LangGraph received: normal'
        assert r2.metadata['thread_id'] != first_thread
    finally:a.close()


def test_crewai_import_adapter_fixture():
    from yasc_harness.adapters.crewai import CrewAIAdapter
    a=CrewAIAdapter({'type':'crewai','crew':'tests.fixtures.framework_targets:create_crew','factory':True,'input_key':'prompt'})
    try:r=a.send('verify me')
    finally:a.close()
    assert r.text=='CrewAI received: verify me'
    assert r.events[0]['type']=='task_output'
    assert r.metadata['framework']=='crewai'


def test_mcp_http_adapter_legacy_fallback_fixture():
    import threading
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    from yasc_harness.adapters.mcp import HTTPMCPAdapter

    seen=[]
    class H(BaseHTTPRequestHandler):
        def log_message(self,*a): pass
        def do_POST(self):
            n=int(self.headers.get('Content-Length','0')); req=json.loads(self.rfile.read(n) or b'{}'); method=req.get('method'); rid=req.get('id'); seen.append(method)
            if method=='server/discover':
                payload={'jsonrpc':'2.0','id':rid,'error':{'code':-32601,'message':'method not found'}}
            elif method=='initialize':
                payload={'jsonrpc':'2.0','id':rid,'result':{'protocolVersion':'2025-11-25','capabilities':{'tools':{}},'serverInfo':{'name':'legacy','version':'1'}}}
            elif method=='tools/list':
                payload={'jsonrpc':'2.0','id':rid,'result':{'tools':[{'name':'echo','inputSchema':{'type':'object'}}]}}
            elif rid is None:
                self.send_response(202); self.end_headers(); return
            else:
                payload={'jsonrpc':'2.0','id':rid,'result':{}}
            body=json.dumps(payload).encode(); self.send_response(200); self.send_header('Content-Type','application/json');
            if method!='server/discover': self.send_header('Mcp-Session-Id','legacy-session')
            self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
    srv=ThreadingHTTPServer(('127.0.0.1',0),H); th=threading.Thread(target=srv.serve_forever,daemon=True); th.start()
    try:
        a=HTTPMCPAdapter({'type':'mcp-http','url':f'http://127.0.0.1:{srv.server_port}/mcp','mode':'auto'})
        try:
            assert a.era=='legacy'
            assert a.list_tools()[0]['name']=='echo'
            assert a.protocol_version=='2025-11-25'
        finally:a.close()
        assert seen[:3]==['server/discover','initialize','notifications/initialized']
        assert 'tools/list' in seen
    finally:
        srv.shutdown(); srv.server_close()
