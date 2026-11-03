"""Separate original smoke outcomes from changed-semantics external tests."""
from pathlib import Path
import json, hashlib
from inventory import DOC, OUT, table
RAW=DOC/'benchmarks/raw'

def read(p): return p.read_text(encoding='utf-8')
def write(p,s):p.write_text(s.rstrip()+'\n',encoding='utf-8')
def append(p,s):write(p,read(p).split('\n## Readiness and controlled-clock investigation')[0]+'\n\n## Readiness and controlled-clock investigation\n\n'+s)

def main():
    records=json.loads(read(RAW/'readiness02/commands.json'))
    reference=next(t for t in json.loads(read(OUT/'browser-experiments.json')) if t['status']=='PASS')['last']['progress']
    originals=[r for r in records if r['name'].startswith('original-')]
    assert len(originals)==3
    experiments=[]
    for profile in ['control','cpu-only','ram-only','contention']:
        p=RAW/'readiness02'/f'browser-{profile}.json'
        data=json.loads(read(p));assert len(data['trials'])==3
        for t in data['trials']:
            if t['status']=='PASS':assert len(t['last']['progress'])==59 and all(a['pass'] for a in t['last']['progress']) and [a['message'] for a in t['last']['progress']]==[a['message'] for a in reference]
            experiments.append(dict(profile=profile,trial=t['trial'],status=t['status'],exit_code=t['exit_code'],duration_ms=t['duration_ms'],smoke_ms=t.get('smoke_ms'),last=t.get('last'),error=t.get('error'),events=t['events'],samples=t['samples'],before=t.get('before'),after=t.get('after'),raw_sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    evidence={'identity':'External DOM-readiness and controlled-clock test; not original-smoke PASS','original_runs':originals,'external_trials':experiments,'stage':'PARTIAL','browser_gate':'BLOCKED'}
    write(OUT/'browser-readiness.json',json.dumps(evidence,indent=2))
    original_pass=sum(r['exit']==0 for r in originals); external_pass=sum(r['status']=='PASS' for r in experiments)
    rows=[['Original unchanged',3,3,original_pass,3-original_pass,0,0],['External changed-semantics',12,12,external_pass,12-external_pass,0,0],['Initial daemon-unavailable attempt',15,0,0,0,0,15]]
    summary=table(['Identity','Expected trials','Executed','PASS','FAIL','SKIPPED','NOT_RUN'],rows)
    summary+='''
The first readiness01 attempt failed before starting any container: Docker Desktop Linux Engine named pipe absent. Seven Docker invocations failed to launch the planned 3 original + 12 external trials; classify all 15 trials NOT_RUN/environment BLOCKED, not failed assertions. Installed Docker Desktop was started; successful docker info preceded readiness02. No production/VPS use. Historical results, baseline and Go tests were not rerun.

Original smoke runs execute unmodified `bun run test:browser` and pinned tests/run-browser.mjs. Exercised environment: Linux amd64 Docker tool image, Bun1.4.2, Chromium156.0.8078.73, UTC/C.UTF-8, 2CPU/2000MiB, network none. Upstream documents Bun and local Chromium, not a minimum CPU/RAM SLA; these limits are the documented audit environment, not an invented upstream support guarantee. Three successes cannot erase historical flakiness or establish all-environment stability.

External matrix: normal2CPU/2000MiB, CPU-only1CPU/2000MiB, RAM-only2CPU/1400MiB, contention1CPU/1400MiB plus one CPU-loop process. Three fresh profiles each, same pinned source/dependencies/fixtures. Per-profile bundle builds once; reported trial duration excludes build. The original runner builds every invocation, so command durations are not directly comparable. Source remains read-only and 1772 blobs are reverified. No old evidence is overwritten.
'''
    analysis='''
### Root cause and evidence boundaries

1. **Upstream smoke synchronization defect: modal readiness.** browser-smoke.tsx:180–184 flushes a click, sleeps100ms, then requires `.jer-editor-container`. InboundCheckboxCard opens a Mantine modal. Locked Mantine Transition/use-transition schedules state changes through requestAnimationFrame (including a second frame) and timers; Transition returns null in exited state. A timer expiring is not proof these frame callbacks/React commits completed. Previous control run returned `dataset.result=failed` / “Inbound JSON viewer is missing” before the first assertion. The exact failing condition is DOM absence at the query. Which individual frame/commit was delayed in that historical run was not recorded; the state-machine race is established, not its precise scheduler trace. No evidence of a production JSON-viewer functional defect.

2. **Upstream smoke synchronization defect: clock readiness.** ClockFixture calls useTime(20). The hook registers setInterval in useEffect, then calls setNow(Date.now()); React must commit that update before the span changes. The smoke sleeps60ms and compares span text to firstTime. In two previous CPU-contention runs that comparison was false. Cgroup throttled periods increased59/59 and50/50 over their sample windows. The precise failed condition is no visible clock advance at assertion time; whether interval delivery, effect registration or commit was late cannot be distinguished from old assertion-only traces. Real-time scheduling is not a correctness barrier, and CPU quotas amplify this race. This supports an upstream **test harness** defect, not an established useTime production defect.

3. **External tool defects.** Prior V1 used a premature2-second CDP call timeout and produced five tool failures; retained separately. Later harness uses a single20-second deadline. New diagnostic runner attaches Runtime/Network/Page before navigation, logs each assert and resource counters. It changes navigation/observation timing and cannot be treated as an exact original-run replay. Browser missing CDP completion has several possible causes; the original20-second timeout remains **unresolved**, not attributed to the modal or clock without evidence.

4. **Environment.** CPU contention/throttling changes rendering/timer scheduling; previous corrected15 trials had no OOM or Network.loadingFailed. The unavailable Docker daemon was a separate startup blocker, corrected by starting Desktop. No browser or application test executed during that failed launch attempt.

### Separate external harness and semantic changes

browser_deterministic.mjs uses an in-memory Vite transform only on browser-smoke.tsx. Original files and production build behavior are unchanged. All original assertions remain intact and each successful run must record exactly59 PASS assertions. Modal wait is replaced with MutationObserver + requestAnimationFrame predicate readiness for the viewer and string-value element. The outer20-second smoke deadline remains; readiness failure remains a failure, not a skip.

Clock test temporarily fixes Date.now at100000, captures the20ms interval in an isolated browser context, waits for registration, and drives three20ms ticks through the real registered callback inside flushSync. It requires exactly one matching interval; ambiguous timer identity fails. It waits for committed DOM time advance, executes the unchanged assertion, then restores global clock/timer APIs. The registration/advance code fails on missing or ambiguous interval registration. Debug console probes are stripped by the pinned production build; no AUDIT_CLOCK console events were observed. Assertion progress is retained independently in window.__auditProgress and CDP snapshots. This observability limit is explicit; no clock console evidence is invented. This tests state propagation under controlled test time; **it does not test real timer delivery under contention**, and its PASS is not an original-smoke PASS. Other original waits/animations remain real-time; whole-suite mathematical determinism is not claimed.

Scope of resolution: two known readiness hazards are removed in this separate harness, subject to the observed matrix results. Scheduling, rendering and other legacy fixed waits can still vary. Bounded repeat success is evidence of observed reproducibility, not proof that all possible flakes are eliminated. No production CSPRNG, Go source, React source, fixtures, GATE_POLICY or20-second timeout was changed.

### Gate decision

**STAGE_01 PARTIAL; browser gate BLOCKED; historical FLAKY=FAIL.** New external results cannot close the original mandatory gate. Closing it without an exception requires an authorized upstream test-harness correction and original-gate revalidation; that changes the pinned test reference and is outside this audit-only change. The exact historical timeout cause remains unresolved. Stop at Stage01; no Stage02 work.
'''
    append(OUT/'BROWSER_DIAGNOSTICS.md',summary+analysis+'\n[CDP events, progress and counters](browser-readiness.json).')
    for p in [DOC/'stages/STAGE_01_AUDIT.md',DOC/'TEST_INVENTORY.md',DOC/'PROGRESS.md',DOC/'HANDOFF.md']:
        link='../audit/' if p.parent.name=='stages' else 'audit/'
        append(p,summary+'\nModal100ms and clock60ms waits are upstream smoke readiness races. A separate DOM/controlled-clock harness preserves assertions but changes wait semantics; it is not replacement evidence for the original smoke. Historical20s timeout root cause remains unresolved. STAGE_01 PARTIAL, browser gate BLOCKED, Stage02 NOT READY. Full analysis and limits: [browser diagnostics]('+link+'BROWSER_DIAGNOSTICS.md). Reproduce only into a new evidence directory with tools/audit-stage01/readiness_run.py; do not rerun baseline/Go/native/inventory. Starting delivery commit d694945c8bfde9d44b720c0ee0c807ea1db91ead.\n')
    ledger=json.loads(read(OUT/'final-test-ledger.json'))
    ledger['readiness_investigation']={'original':{'expected':3,'executed':3,'pass':original_pass,'fail':3-original_pass,'skipped':0,'not_run':0},'external_distinct_test':{'expected':12,'executed':12,'pass':external_pass,'fail':12-external_pass,'skipped':0,'not_run':0},'daemon_unavailable':{'expected':15,'executed':0,'not_run':15,'blocked':15},'historical_flaky':'FAIL','browser_gate':'BLOCKED','stage':'PARTIAL','evidence':'browser-readiness.json'}
    write(OUT/'final-test-ledger.json',json.dumps(ledger,indent=2))
    commandrows=[]
    for folder in ['readiness01','readiness02']:
        for r in json.loads(read(RAW/folder/'commands.json')):commandrows.append([folder,r['name'],r['utc'],r['exit'],r['seconds'],' '.join(r['command'])])
    append(OUT/'COMMANDS.md',table(['Folder','ID','UTC','Exit','Seconds','argv'],commandrows))
    print(json.dumps(ledger['readiness_investigation']))

if __name__=='__main__': main()
