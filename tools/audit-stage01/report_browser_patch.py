"""Versioned candidate baseline; never promote release gate automatically."""
from pathlib import Path
import collections, hashlib, json, subprocess
from inventory import DOC, OUT, ROOT, table
RAW=DOC/'benchmarks/raw/patched-v1'
TOOLS=ROOT/'tools/audit-stage01'
SHA='d709bad01dc0ceacb20012a3afdf528eddfd061f'
def read(p):return p.read_text(encoding='utf-8')
def put(p,s):p.write_text(s.rstrip()+'\n',encoding='utf-8')
def append(p,s):put(p,read(p).split('\n## Versioned test-only patch V1')[0]+'\n\n## Versioned test-only patch V1\n\n'+s)

def main():
    identity=json.loads(read(TOOLS/'browser-smoke-v1.identity.json'))
    assert hashlib.sha256((TOOLS/'browser-smoke-v1.patch').read_bytes()).hexdigest()==identity['patch_sha256']
    assertion_check=json.loads(read(OUT/'browser-patch-v1-assertion-check.json'));assert assertion_check['status']=='PASS'
    records=json.loads(read(RAW/'results03/commands.json'));byname={r['name']:r for r in records}
    expected=[f'patched-{p}-{n}' for p in ['normal','cpu-only','ram-only','contention'] for n in range(1,6)]
    trials=[]
    for name in expected:
        f=RAW/'results03'/(name+'.json')
        if name not in byname or not f.exists():
            trials.append(dict(id=name,status='NOT_RUN'));continue
        b=json.loads(read(f));assert b['patch_sha256'] in {identity['patch_sha256'],identity.get('tested_patch_sha256')} and len(b['trials'])==1
        t=b['trials'][0];outcomes=(t.get('last') or {}).get('progress',[]);trace=(t.get('last') or {}).get('readiness',[])
        if t['status']=='PASS':
            assert len(outcomes)==59 and all(a['pass'] and a['message']==identity['assertions'][i]['message'] for i,a in enumerate(outcomes))
            assert {'modal-viewer-committed','real-clock-registered','real-clock-callback','real-clock-dom-advanced'} <= {x['label'] for x in trace}
            assert byname[name]['exit']==0
        trials.append(dict(id=name,profile=b['profile'],status=t['status'],command=byname[name],trial=t,raw_sha256=hashlib.sha256(f.read_bytes()).hexdigest(),stdout_sha256=hashlib.sha256((RAW/'results03'/(name+'.stdout')).read_bytes()).hexdigest(),stderr_sha256=hashlib.sha256((RAW/'results03'/(name+'.stderr')).read_bytes()).hexdigest()))
    observed=collections.Counter(t['status'] for t in trials)
    counts={status:observed.get(status,0) for status in ['PASS','FAIL','SKIPPED','NOT_RUN','BLOCKED','FLAKY']}
    # Every original blob must still match; only the approved test file differs in the disposable copy.
    git=['git','-c','safe.directory='+ROOT.as_posix()]
    tree=subprocess.check_output(git+['ls-tree','-rz',SHA],cwd=ROOT)
    changed=[];checked=0
    for row in tree.split(b'\0'):
        if not row:continue
        meta,name=row.split(b'\t');mode,kind,sha=meta.split()
        if kind!=b'blob':continue
        rel=name.decode();data=(DOC/'benchmarks/raw/source-lf'/rel).read_bytes()
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==sha.decode(),rel
        copy=(RAW/'source'/rel).read_bytes()
        if copy!=data:changed.append(rel)
        checked+=1
    assert checked==1772 and changed==['frontend/tests/browser-smoke.tsx'],changed
    provenance=dict(identity=identity,source_blobs_checked=checked,original_mismatches=0,temporary_copy_changes=changed,runner='tools/audit-stage01/patched_browser_runner.mjs',patched_test_sha256=hashlib.sha256((RAW/'source/frontend/tests/browser-smoke.tsx').read_bytes()).hexdigest(),patched_test_line_endings='CRLF (Windows Git core.autocrlf=true; explicitly reproduced by prepare script)',runner_sha256=hashlib.sha256((TOOLS/'patched_browser_runner.mjs').read_bytes()).hexdigest(),tool_image='sha256:29642d96c0925e8cc86d66cc09b74f77c5174f64968334fe40418ee40ef8643e',bun='1.4.2',chromium='156.0.8078.73',timezone='UTC',locale='C.UTF-8',deadline_ms=20000,assertion_ast_check=assertion_check)
    put(OUT/'browser-patch-v1-results.json',json.dumps(dict(provenance=provenance,expected=expected,counts=counts,trials=trials),indent=2))
    summary=table(['Run ID','Status','CLI exit','Smoke seconds','Assertion outcomes'],[[t['id'],t['status'],t.get('command',{}).get('exit','—'),round(t.get('trial',{}).get('smoke_ms',0)/1000,3),len((t.get('trial',{}).get('last') or {}).get('progress',[]))] for t in trials])
    text=f'''Candidate identity **{identity['patched_id']}**; original **{identity['original_id']}**. Patch SHA256 `{identity['patch_sha256']}`. Published patch uses zero-context diff to avoid whitespace-only context lines flagged by git diff --check. The20 runs used the full-context representation; both apply to byte-identical TSX, verified in browser-patch-v1-packaging.json. Both hashes and raw tested patch are retained. This is a packaging-only change, not a browser retest or code change. This is an authorized test-only candidate, not an unchanged upstream smoke. Upstream SHA `{SHA}`. Only the temporary copy of frontend/tests/browser-smoke.tsx is changed. All1772 original blobs match; other1771 temporary-copy files and all fixtures match. Original tests/run-browser.mjs remains byte-identical; validation uses a separate versioned external CDP supervisor, whose hash is recorded in browser-patch-v1-results.json.

Twenty independent containers/browser processes with clean profiles, five per profile: normal2CPU/2000MiB; CPU-only1CPU/2000MiB; RAM-only2CPU/1400MiB; contention1CPU/1400MiB plus one controlled CPU loop during browser lifetime. Pinned image/Bun/Chromium/UTC/locale/fixtures identical. One immutable compiled bundle is reused; first invocation includes build time, smoke duration excludes it. Network none. Startup10s and outer smoke20s deadlines unchanged; deadline begins before navigation in this supervisor. Internal readiness bound19s does not extend outer20s. Every invocation has saved stdout/stderr, actual process exit, CDP events/exceptions/errors, snapshots, resource counters (throttling and memory.events) and timeout details.

{summary}

Counts: {json.dumps(counts)}. Full59 assertion identities and outcomes are retained per run. AST verification confirms all59 original assert argument expressions/expected values and their order match after explicit CRLF-to-LF whitespace normalization. Windows Git applied CRLF only to the changed test file; four multiline argument expressions differ solely at line breaks. Literal values are unchanged. Runtime manifests match the same59 message identities. Registered/delivered native timer events and DOM advancement are separately captured; Date.now and native scheduling are not replaced.

### Changes and equivalence argument

The modal fixed100ms wait becomes bounded readiness for an opened, visible dialog with a committed JSON-viewer/string element; the original value/read-only/mutation assertions remain. The clock fixed60ms wait becomes bounded confirmation of registration of the actual20ms native interval, callback delivery, state update and visible DOM time advancement; the original greater-than assertion remains. Test-only interval observation delegates to native setInterval and restores the wrapper in finally. No production hook or API behavior is patched. This candidate therefore retains a real-timer test rather than substituting a synthetic clock.

Timing acceptance **does change**: a slow but correctly committed update may pass within the bounded readiness window instead of being sampled after100/60ms. This removes unsupported fixed-sleep synchronization assumptions, not an explicitly documented application latency SLA. That change needs explicit baseline acceptance; identical assertions alone do not prove identical temporal semantics. Other legacy waits remain;20 passes cannot prove universal absence of flakes.

### Historical outcomes and preparation failures

Original immutable smoke most recently passed3/3 but retains its historical20s timeout FAIL. Earlier external instrumentation demonstrated viewer readiness and clock-contention FLAKY; those results remain distinct and unchanged. The historical20s timeout has no proven root cause; this patch does not claim to explain it.

Auto-review first timed out before execution; one permitted identical retry proceeded. Preparation results/ contains20 Docker exit125 mount failures (new read-only copy lacked node_modules mountpoint): no browser test executed. results02/ contains20 external-runner ReferenceError failures before page navigation (html scope defect): browser processes started but59 assertions were NOT_RUN. These tool FAIL logs and their failed runner snapshot are retained. Mountpoint and runner scope were corrected; results03/ is the requested20-case assertion validation. The initial AST checker also failed to load the TypeScript compiler API (the pinned TypeScript7 package has no legacy JS API); the installed Prettier TypeScript parser was used instead. Its first strict source-text comparison detected four CRLF-only multiline whitespace differences; explicit CRLF normalization resolved those with unchanged literal values. These checker failures are retained as audit-tool findings, not application assertion failures. No failed browser assertion was retried to obtain a green result. Further environment/programming errors now abort the series rather than repeatedly failing remaining cases.

### Gate recommendation — no automatic promotion

**STAGE_01 PARTIAL; browser gate BLOCKED pending explicit acceptance of a new mandatory test baseline.** Historical original FLAKY remains FAIL under unchanged GATE_POLICY. The adoption proposal is to register this precise patch+runner+assertion manifest as the new mandatory test identity, with the preserved original history and the explicit temporal-semantics change above. This is a baseline revision, not an exemption or relabelling historical FAIL as PASS. If any candidate trial failed or is missing, those gaps additionally block adoption. Final Stage01 closure requires explicit baseline approval plus review of all current mandatory evidence; no automatic Stage02 transition.

Reproduce from the immutable LF archive with prepare_browser_patch.py (refuses an existing copy), then validate_browser_patch.py (refuses existing evidence), AST check_browser_patch.cjs, and report_browser_patch.py. Use fresh evidence paths for any future run. Patch and identity live in tools/audit-stage01/. No Go tests, native tests, inventory or baseline measurements were repeated.
'''
    put(OUT/'BROWSER_PATCH_V1.md','# Test-only browser baseline V1 proposal\n\n'+text+'\n## Full assertion manifest\n\n'+table(['ID','Unchanged expected assertion'],[[a['id'],a['message']] for a in identity['assertions']]))
    for p in [OUT/'BROWSER_DIAGNOSTICS.md',DOC/'stages/STAGE_01_AUDIT.md',DOC/'TEST_INVENTORY.md',DOC/'PROGRESS.md',DOC/'HANDOFF.md']:
        link='' if p.parent==OUT else '../audit/' if p.parent.name=='stages' else 'audit/'
        append(p,summary+f'\nCandidate `{identity["patched_id"]}`; patch SHA256 `{identity["patch_sha256"]}`. Counts {json.dumps(counts)}. All59 assertions and real native timer evidence preserved; original1772 blobs unchanged. Temporal wait semantics changed explicitly. STAGE_01 PARTIAL; browser gate BLOCKED pending explicit new-baseline acceptance. Historical FAIL/FLAKY remain, original20s timeout root cause unresolved. [Proposal, equivalence limits and preparation errors]({link}BROWSER_PATCH_V1.md). No Stage02 work.\n')
    ledger=json.loads(read(OUT/'final-test-ledger.json'))
    ledger['patched_v1']={'identity':identity,'expected':20,'executed':20-counts.get('NOT_RUN',0),'counts':counts,'candidate_evidence':'browser-patch-v1-results.json','adoption':'PENDING_EXPLICIT_APPROVAL','browser_gate':'BLOCKED','stage':'PARTIAL','preparation':{'mount_fail_exit125':20,'runner_reference_error_exit1':20,'assertions_executed_in_preparation':0}}
    put(OUT/'final-test-ledger.json',json.dumps(ledger,indent=2))
    commandrows=[]
    for folder in ['results','results02','results03']:
        for r in json.loads(read(RAW/folder/'commands.json')):commandrows.append([folder,r['name'],r['utc'],r['exit'],r['seconds'],' '.join(r['command'])])
    append(OUT/'COMMANDS.md',table(['Folder','ID','UTC','Exit','Seconds','argv'],commandrows))
    print(json.dumps(dict(counts=counts,original_blobs=checked,changed_temporary_files=changed,stage='PARTIAL')))

if __name__=='__main__':main()
