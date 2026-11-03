"""Append supplementary proof without rewriting historical full-suite results."""
from pathlib import Path
import collections
import hashlib
import json
from inventory import DOC, OUT, table

RAW=DOC/'benchmarks/raw'
RUN='https://github.com/test-alexsun/RustWave/actions/runs/41566960948'


def read(p): return p.read_text(encoding='utf-8')
def put(p,s): p.write_text(s.rstrip()+'\n',encoding='utf-8')
def append(p,s): put(p,read(p).split('\n## Execution gaps continuation')[0]+'\n\n## Execution gaps continuation\n\n'+s)
def events(p):
    return [json.loads(s) for s in read(p).splitlines() if s.strip()]
def outcomes(p):
    return {e['Package']+'/'+e['Test']:e['Action'].upper().replace('SKIP','SKIPPED') for e in events(p) if e.get('Test') and e['Action'] in ('pass','fail','skip')}


def main():
    full=json.loads(read(OUT/'go-test-results.json'))
    manifest=json.loads(read(OUT/'go-test-manifest.json'))
    for r in full.values(): assert set(r['top']) == {t['id'] for t in manifest}
    sup={}
    rows=[]
    for mode in ('sqlite','postgres'):
        sup[mode]={}
        for kind,p in [('schema',RAW/'gaps01'/f'schema-{mode}.stdout'),('migration',RAW/'gaps01'/f'migration-{mode}.stdout'),('native',RAW/'gaps01/native'/f'native-{mode}.jsonl')]:
            o=outcomes(p);assert o and all(v=='PASS' for v in o.values()),(p,o)
            for id,status in o.items(): sup[mode][id]={'result':status,'evidence':str(p.relative_to(RAW))}
            rows.append([mode,kind,len([id for id in o if '/' not in id.split('/Test',1)[1]]),len(o),'PASS'])
    coverage=[]
    for mode,r in full.items():
        for kind in ('top','nested'):
            for id,status in r[kind].items():
                additional=sup[mode].get(id)
                # A postgres child skipped in the no-DSN suite has an exact same
                # ID executed in the original PG suite. Explicit cross-context proof.
                if not additional and status=='SKIPPED' and id.endswith('/postgres') and full['postgres']['nested'].get(id)=='PASS':
                    additional={'result':'PASS','evidence':'lf-go-test-postgres.stdout (same PostgreSQL child ID; cross-context)'}
                effective='PASS' if status=='PASS' or additional and additional['result']=='PASS' else 'BLOCKED'
                coverage.append(dict(mode=mode,id=id,kind=kind,full_suite=status,supplementary=additional,effective=effective))
    assert len([r for r in coverage if r['kind']=='top'])==256
    assert all(r['effective']=='PASS' for r in coverage)
    put(OUT/'supplementary-coverage.json',json.dumps(coverage,indent=2))
    covertext=table(['Mode','ID','Kind','Original full suite','Additional proof','Effective execution'],[[r['mode'],r['id'],r['kind'],r['full_suite'],r['supplementary']['evidence'] if r['supplementary'] else 'Original PASS',r['effective']] for r in coverage])
    put(OUT/'SUPPLEMENTARY_COVERAGE.md','# Mandatory Go ID execution coverage\n\n128 source-defined top-level IDs per mode remain unchanged. Observed child IDs are retained separately; no claim of independent exhaustive child discovery. Supplementary PASS closes execution coverage for the identical test ID; it does not modify historical SKIPPED. Database-independent native/schema tests are labelled twice for matrix accounting; this does not assert they access both DBs. The schema test internally generates both dialects in dry-run. PostgreSQL integration uses a DSN in both labelled runs. The response-headers PostgreSQL child uses existing exact-ID PG full-suite PASS, explicitly cross-context.\n\n'+covertext)
    browser=[]
    for version in ('browser-gaps01','browser-gaps02','browser-gaps03'):
        for profile in (('cpu-only','ram-only') if version=='browser-gaps03' else ('control','constrained','contention')):
            p=RAW/version/f'browser-{profile}.json'
            b=json.loads(read(p));assert len(b['trials'])==3
            for t in b['trials']:
                es=t.get('events',[])
                browser.append(dict(version=version,profile=profile,trial=t['trial'],status=t['status'],exit_code=t['exit_code'],duration_ms=t['duration_ms'],smoke_ms=t.get('smoke_ms'),error=t.get('error'),last=t.get('last'),before=t.get('before'),after=t.get('after'),samples=t.get('samples'),console_events=sum(e['method']=='Runtime.consoleAPICalled' for e in es),runtime_exceptions=[e['params'].get('exceptionDetails',{}).get('text') for e in es if e['method']=='Runtime.exceptionThrown'],network_failures=[e['params'] for e in es if e['method']=='Network.loadingFailed'],raw_sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    put(OUT/'browser-experiments.json',json.dumps(browser,indent=2))
    browser_table=table(['Version','Profile','Trial','Result','Exit','Duration s','Assertions','Last result/error','Network failures'],[[r['version'],r['profile'],r['trial'],r['status'],r['exit_code'],round(r['duration_ms']/1000,3),len((r['last'] or {}).get('progress',[])),r['error'] or (r['last'] or {}).get('text',''),len(r['network_failures'])] for r in browser])
    totals={v:dict(collections.Counter(t['status'] for t in browser if t['version']==v)) for v in ('browser-gaps01','browser-gaps02','browser-gaps03')}
    notes='''
External harness: browser_diagnostic.mjs builds pinned Vite input and adds progress logging only to the in-memory assert transform. Source remains read-only; no assertion, wait(100), expected result or upstream timeout was changed. CDP Runtime/Network/Page events are enabled before file navigation from about:blank. This attach order and instrumentation differ from the historical runner; findings cannot retroactively prove its precise cause. Each profile uses three fresh Chromium profiles, UTC/C.UTF-8, network none, identical built bundle within that profile. Control 2 CPU/2000 MiB; constrained 1 CPU/1400 MiB; contention same constrained limits plus a Bun CPU loop. Every series builds once; build time is separate. An idle sample captures cgroup CPU usage/throttling, current/peak RAM and memory.events, not just Bun RSS. cgroup resources include the harness and CPU stressor. Console and exceptions are recorded even where the smoke deliberately exercises ErrorBoundary; expected test errors alone are not an unexpected failure.

V1 tooling limitation: independent CDP-call timer was 2 s and prematurely failed some busy Runtime.evaluate requests; these are **audit harness failures**, not proof of the original 20-s timeout. V1 raw results and original harness snapshot are retained. V2 uses the unchanged **single 20-s smoke deadline** for pending evaluations, captures URL/readyState/result/progress and resources, and saves Chromium stderr even on failure. Startup deadline remains 10 s. No increase beyond the original smoke deadline.

V1 control produced PASS/FAIL/PASS under identical resource limits; the failure returned dataset.result=failed and `Error: Inbound JSON viewer is missing` before the first assert. Source browser-smoke.tsx:180–184 clicks the modal, waits a fixed 100 ms, then requires .jer-editor-container. This is direct evidence of a readiness-sensitive flaky smoke condition. It is not proof that the historical timeout had the same cause. Resource-limited CDP timeouts and per-profile outcomes must be assessed with the table and counters; no statistically quantified CPU/RAM causality claim from n=3. V3 additionally isolates CPU-only (1 CPU/2000 MiB) and RAM-only (2 CPU/1400 MiB), three runs each, against V2 control. The contention comparison keeps the constrained limits constant. This is a small diagnostic sample, not a statistical causal estimate.

Historical first LF browser FAIL and retry PASS remain unchanged. **FLAKY / BLOCKED** remains for the strict browser gate. The precise cause of the original timeout is still unresolved because original console/network telemetry was unavailable. These supplementary diagnostic successes never override historical outcomes or promote the stage to PASS.
'''
    notes+='\nV2 control and constrained profiles each passed 3/3. V2 contention returned dataset.result=failed twice on session clock advances without render-time reads, and passed once. Source browser-smoke.tsx:350–356 relies on a real-time 60-ms wait. This is a reproduced readiness/timer failure under controlled CPU contention; it is distinct from the historical 20-s timeout.\n'
    append(OUT/'BROWSER_DIAGNOSTICS.md',browser_table+'\n'+notes+'\nCounters and per-assertion progress: [browser-experiments.json](browser-experiments.json).')
    summary='''Native updater and root-writability tests PASS on non-container GitHub-hosted Ubuntu 24.04 VM, UID1001, Go1.27.3. Both tests use t.TempDir; no production services or VPS. Job preflight asserts nonroot and no /.dockerenv. '''+f'[Actions run]({RUN}).\n\n'
    summary+='Schema export PASS in separate raw/gaps01/schema-source, never original LF snapshot. It internally generates SQLite and PostgreSQL SQL; generated files are disposable evidence, not replacements for committed fixtures. Migration integration and migration children PASS with separate PostgreSQL18 tmpfs. Root test also retains its earlier nonroot Docker PASS. Original top-level full-suite results remain SQLite124PASS/4SKIPPED, PG125PASS/3SKIPPED, NOT_RUN0; SQLite child130PASS/3SKIPPED and PG child133PASS.\n\n'
    summary+='New execution accounting (separate from historical runs):\n\n'+table(['Scope','EXPECTED','EXECUTED','PASS','FAIL','SKIPPED','NOT_RUN','BLOCKED','FLAKY'],[['Go supplementary top-level',12,12,12,0,0,0,0,0],['Browser V1 (includes tool errors)',9,9,3,6,0,0,1,1],['Browser V2 corrected deadline',9,9,7,2,0,0,1,1],['Browser CPU/RAM isolated',6,6,6,0,0,0,0,0]])+'\nBLOCKED and FLAKY overlap terminal outcomes; never add them as extra test cases. V1 includes five premature CDP timeouts and one readiness failure. V2+isolated valid diagnostics total15 executions:13PASS/2FAIL, both failures in CPU-contention. No OOM or Network.loadingFailed in those15. CPU contention used95–100% of one core; observed final cgroup memory825–872MiB includes Chromium/harness/cache and is not backend RSS.\n\n'
    summary+=table(['Label','Supplement','Top-level IDs','All observed IDs','Result'],rows)
    summary+='\n[Full per-ID coverage](audit/SUPPLEMENTARY_COVERAGE.md): 128/128 top-level IDs per mode have PASS evidence after supplementation, with all observed child gaps covered. This is execution coverage, not Go↔Rust compatibility. Full-suite skips are historical facts; effective supplementary coverage is separate.\n\nBrowser diagnostic counts: '+json.dumps(totals)+'. V1 includes premature 2-s tool failures; V2 uses original20-s deadline. Control mixed outcomes prove readiness-sensitive **FLAKY**; historical timeout cause remains **BLOCKED**. [Diagnostic report](audit/BROWSER_DIAGNOSTICS.md).\n\nSTAGE_01 remains **PARTIAL**, Stage02 **NOT READY**. Go execution gaps are covered; strict browser no-flaky gate remains unresolved. Six baseline trials and source inventory were not rerun.\n'
    append(DOC/'TEST_INVENTORY.md',summary)
    append(DOC/'stages/STAGE_01_AUDIT.md',summary.replace('(audit/','(../audit/'))
    append(DOC/'PROGRESS.md',summary)
    append(DOC/'HANDOFF.md','Starting confirmed commit 4b9dfb4fc0c62582e38821b54e97b95aed0ceaa8; native workflow commit 8a976f2. Continue Stage01 browser gate only; Stage02 not started. Do not rerun results.py/finalize.py without gaps_report.py afterwards: base generators retain historical checkpoint sections.\n\n'+summary+'\nReproduce diagnostics only into a new evidence directory: python tools/audit-stage01/browser_experiment.py <new-name>. Supplement runner refuses existing evidence. Native workflow and JSON artifact evidence retained under ignored raw/gaps01/native. Do not rerun baseline or inventory.\n')
    ledger=json.loads(read(OUT/'final-test-ledger.json'))
    ledger['supplementary']={'native_run':RUN,'coverage':'supplementary-coverage.json','top_ids_expected':256,'top_ids_pass_evidence':256,'observed_child_ids':len([r for r in coverage if r['kind']=='nested']),'remaining_go_execution_gaps':0,'browser':totals,'flaky':['BROWSER'],'blocked':['Historical timeout cause unresolved; readiness-sensitive browser failures'],'stage':'PARTIAL'}
    ledger['supplementary_rows']=[dict(id='GO-supplementary-top',expected=12,executed=12,passed=12,failed=0,skipped=0,not_run=0,blocked=0,flaky=0)]
    for version,c in totals.items(): ledger['supplementary_rows'].append(dict(id=version,expected=sum(c.values()),executed=sum(c.values()),passed=c.get('PASS',0),failed=c.get('FAIL',0),skipped=0,not_run=0,blocked=1 if c.get('FAIL') else 0,flaky=1 if c.get('FAIL') and c.get('PASS') else 0))
    ledger['status_vocabulary']=['PASS','FAIL','SKIPPED','NOT_RUN','BLOCKED','FLAKY']
    for r in ledger['rows']:r.setdefault('flaky',1 if r['id']=='BROWSER-LF-attempts' else 0)
    put(OUT/'final-test-ledger.json',json.dumps(ledger,indent=2))
    hashes=[]
    for p in (RAW/'gaps01').glob('**/*'):
        if p.is_file() and (p.suffix in ('.stdout','.jsonl') or p.name=='environment.txt'): hashes.append([str(p.relative_to(RAW)),hashlib.sha256(p.read_bytes()).hexdigest()])
    put(OUT/'SUPPLEMENTARY_EVIDENCE.md','# Supplementary raw evidence hashes\n\n'+table(['File','SHA256'],hashes))
    commands=[]
    for folder in ('gaps01','browser-gaps01','browser-gaps02','browser-gaps03'):
        for r in json.loads(read(RAW/folder/'commands.json')):commands.append([folder,r['name'],r['utc'],r['exit'],r['seconds'],' '.join(r['command'])])
    append(OUT/'COMMANDS.md',table(['Evidence dir','ID','UTC','Exit','Seconds','Exact argv'],commands)+'\nNative commands and environment: [workflow](../../.github/workflows/stage01-execution-gaps.yml), '+f'[run]({RUN}). Download: gh run download 41566960948 -R test-alexsun/RustWave -n stage01-native-evidence. WSL local read-only enumeration returned E_ACCESSDENIED; no system distribution changed. First workflow push hit DNS failure; ordinary retry succeeded. First gh query defaulted to upstream and returned404; explicit -R test-alexsun/RustWave correctly retrieved target run. These tool errors are not test failures.\n')
    print(json.dumps({'go_top_ids':256,'effective_pass':256,'browser':totals,'stage':'PARTIAL'}))


if __name__=='__main__':main()
