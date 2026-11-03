"""Fail-closed Stage 01 test accounting; retains every observed subtest.

Never treats go test exit 0 as absence of skips. Top-level expected IDs are
independent source-discovered manifest; runtime subtests reported separately.
"""
from inventory import ROOT, DOC, OUT, read, table
import collections
import hashlib
import json
import re

RAW=DOC/'benchmarks/raw'


def parse_go(path,expected):
    events=[]
    errors=[]
    if path.exists():
        for n,line in enumerate(read(path).splitlines(),1):
            try: events.append(json.loads(line))
            except json.JSONDecodeError: errors.append(n)
    state={}; output=collections.defaultdict(list); package_fail=[]
    for e in events:
        key=e.get('Package','')+'/'+e.get('Test','')
        if e.get('Test'):
            if e['Action'] in ('pass','fail','skip'): state[key]=e['Action'].upper().replace('SKIP','SKIPPED')
            if e['Action']=='run': state[key]='NOT_RUN'
            if 'Output' in e: output[key].append(e['Output'])
        elif e['Action']=='fail': package_fail.append(e.get('Package'))
    top={t['id']:state.get(t['id'],'NOT_RUN') for t in expected}
    nested={k:v for k,v in state.items() if k not in top}
    counts=dict(collections.Counter(top.values()))
    nested_counts=dict(collections.Counter(nested.values()))
    issues=[]
    for key,value in state.items():
        if value in ('SKIPPED','FAIL'):
            # Keep skip reason only. Failure logs may contain tokens/body fixtures.
            reason='See ignored raw test output; summarized in stage report.'
            if value=='SKIPPED':
                lines=[l.strip() for l in output[key] if '--- SKIP' not in l and '=== RUN' not in l]
                reason=' '.join(lines[-2:])
            issues.append([key,value,reason])
    fail=bool(errors or package_fail or any(v!='PASS' for v in top.values()) or any(v!='PASS' for v in nested.values()))
    return dict(top=top,nested=nested,counts=counts,nested_counts=nested_counts,issues=issues,package_fail=package_fail,malformed_lines=errors,gate='BLOCKED' if fail else 'PASS')


def main():
    expected=json.loads(read(OUT/'go-test-manifest.json'))
    results={mode:parse_go(RAW/('lf-go-test-'+mode+'.stdout'),expected) for mode in ('sqlite','postgres')}
    first_attempt={mode:parse_go(RAW/('go-test-'+mode+'.stdout'),expected) for mode in ('sqlite','postgres')}
    # Negative checks demonstrate the local accounting, not a future CI release gate.
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        p=__import__('pathlib').Path(tmp)/'negative.jsonl'
        p.write_text(json.dumps(dict(Package='p',Test='TestA',Action='skip'))+'\n')
        assert parse_go(p,[dict(id='p/TestA')])['gate']=='BLOCKED'
        assert parse_go(p,[dict(id='p/TestMissing')])['gate']=='BLOCKED'
    result_rows=[]
    for t in expected:
        result_rows.append([t['id'],t['source'],results['sqlite']['top'][t['id']],results['postgres']['top'][t['id']]])
    text='# Test inventory and execution accounting\n\nPinned source `d709bad01dc0ceacb20012a3afdf528eddfd061f`. '
    text+=f'Expected top-level Go test IDs: **{len(expected)} per DB mode**, independently extracted before execution in [manifest](audit/go-test-manifest.json). Test package includes data-free unit tests too: DB mode indicates environment, not proof each test accesses that DB. '
    text+='`go test -json -count=1 -p=2 -race ./...` for SQLite; PostgreSQL without race as upstream CI, with GOWAVE_TEST_POSTGRES. Locale C.UTF-8, TZ UTC, Go 1.27.3 Linux amd64, resource-limited local Docker. Source and fixtures unmodified.\n\n'
    text+=table(['Mode','Top-level PASS','FAIL','SKIPPED','NOT_RUN','Observed subtests','Subtest results','Fail-closed gate'],[
        [mode,*[r['counts'].get(k,0) for k in ('PASS','FAIL','SKIPPED','NOT_RUN')],len(r['nested']),json.dumps(r['nested_counts']),r['gate']] for mode,r in results.items()])
    text+='\n## Preserved first CRLF archive attempt (not pinned-reference evidence)\n\nSee [archive integrity](audit/ARCHIVE_INTEGRITY.md). These failures remain in the ledger; corrected LF results above supersede their input provenance, not erase them.\n\n'
    text+=table(['Mode','PASS','FAIL','SKIPPED','NOT_RUN'],[[m,*[r['counts'].get(k,0) for k in ('PASS','FAIL','SKIPPED','NOT_RUN')]] for m,r in first_attempt.items()])
    text+='\nTop-level and child counts must not be added as independent scenarios. Runtime child IDs are retained in [execution ledger](audit/go-test-results.json); a parent PASS never hides a child SKIPPED. Dynamically generated subtest IDs are observed, not an independently complete future parity manifest. Package failures and malformed output also block PASS. The parser negative tests reject an explicit skip and a missing mandatory ID. No ignored/xfail/todo capability exists in the Go runner; missing terminal results are NOT_RUN.\n\n'
    text+=table(['Expected ID','Source','SQLite','PostgreSQL'],result_rows)
    text+='\n## Every observed skip/failure\n\n'
    for mode,r in results.items():
        text+=f'### {mode}\n\n'+table(['ID','Status','Reason'],r['issues'])
        text+=f'\nPackage failures: {r["package_fail"]}; malformed JSON lines: {r["malformed_lines"]}.\n'
    text+='''
## Fixtures and test scope

Eight committed fixture files are listed with sizes/hashes in [FIXTURES.md](audit/FIXTURES.md): subscription HTTP gzip, subscription render golden gzip/matrix, crypto, YAML, ordered JSON, JS semantics, Prometheus vectors. Inline fixtures live in *_test.go, including testdb migration/seeding, fake HTTP/TLS node servers, HTTP probes, restore COPY dumps, installer helpers. They are not missing merely because there is no standalone fixture file. Existing nodes tests use mocks, not a deployed GoWave node. Source root tests require POSIX tools; Windows-host Go compilation is not the reference execution environment.

All Go test sources and packages are indexed in [GO_PACKAGES.md](audit/GO_PACKAGES.md). Default testdb SQLite has one in-memory connection and migrations/seeds; GOWAVE_TEST_POSTGRES switches testdb.Open to unique PG schemas. Some tests directly instantiate SQLite despite PG mode, so dual environment execution is not automatically dual DB coverage for every assertion. Database migration tests explicitly iterate engines and skip PG without DSN. CLI SQLite→PG integration needs DSN. No live external node is required by the default suite; separate real RPC/SSH/OAuth/provider integrations remain future NOT_TESTED.

Conditional skips in source: TestExportSchema requires GOWAVE_EXPORT_SCHEMA=1; its regeneration is deliberately not enabled because source fixtures must not change. RootOnlyWritable rejects service-owned files but skips root. ApplyUpdateRequestsRootHelper skips container environment. RepeatedHealthChecksDeduplicateStartJobs skips if real time crosses a minute: this is a determinism defect for future strict gates, not an acceptable blanket exemption. Exact observed skips above take precedence over this static list.

Contract route coverage enumerates Chi routes against 218 command definitions. Probe/mutation tests capture seeded handler responses with GOWAVE_PROBE_OUT; scripts/validate-contract.cjs validates these against locked Zod schemas. This is Go self/contract testing, not Go↔Rust differential compatibility. It does not execute every UI state or every negative input.

Frontend unit source files: entities/ssh-vault/encoding.test.ts; shared/lib/dependencies.test.ts, hardening.test.ts, virtual-layout.test.ts. Browser smoke: tests/run-browser.mjs + browser-smoke.tsx; uses Chromium and browser layout/crypto/locale assertions, not a complete authenticated backend flow. Scripts/tests/installer.sh exercises installer behavior with controlled stubs; real systemd/Docker migration is not run on host. scripts/tests/response-rule-headers.cjs validates header extension schemas. Branding/export/validator checks are separate command IDs below.

## Execution commands

Commands/exit codes/durations are recorded in [COMMANDS.md](audit/COMMANDS.md). Raw logs, exported probes, compiler cache and binaries stay in ignored docs/benchmarks/raw; only non-secret status/IDs/checksums are committed. Reproduce with Python tools/audit-stage01/inventory.py, run.py (Docker permissions), features.py, results.py; start from the git archive specified in the stage report. The benchmark is a separate script and must run without simultaneous compilation.

Fixture regeneration against original Remnawave/Node 24.21.0 is NOT_RUN; native installer execution, live provider/node/SSH sessions, full UI network traces and future Rust/architecture matrix are NOT_RUN/NOT_TESTED, explicitly outside Go unit evidence. Native updater test skips remain a Stage 01 execution gap, not a PASS.
'''
    frontend=[]
    for p in sorted((ROOT/'frontend/src').rglob('*.test.ts')):
        for match in re.finditer(r'\btest\(\s*\'([^\']+)\'',read(p)):
            frontend.append(dict(name=match[1],source=p.relative_to(ROOT).as_posix()))
    statuses={}
    result_path=RAW/'lf-frontend-test.stderr'
    if result_path.exists():
        for line in read(result_path).splitlines():
            match=re.match(r'^\((pass|fail|skip|todo)\) (.*?)(?: \[[\d.]+ms\])?$',line)
            if match:statuses[match[2]]=match[1].upper().replace('SKIP','SKIPPED')
    front_counts=collections.Counter(statuses.get(t['name'],'NOT_RUN') for t in frontend)
    text+='\n## Frontend unit manifest / actual IDs\n\n'+str(dict(front_counts))+'; expected '+str(len(frontend))+' source-defined names. Results from corrected lf-frontend-test; no assumed passes from build.\n\n'
    text+=table(['ID','Source','Test name','Result'],[[f'BUN-{i:03}',t['source'],t['name'],statuses.get(t['name'],'NOT_RUN')] for i,t in enumerate(frontend,1)])
    supplemental=RAW/'lf-go-nonroot.stdout'
    if supplemental.exists():
        nonroot=parse_go(supplemental,[t for t in expected if t['name']=='TestRootOnlyWritableRejectsServiceAccountFiles'])
        text+='\n## Supplemental nonroot test\n\n'+str(nonroot['counts'])+'. Run as UID/GID 10001 in isolated Docker; covers source root-dependent skip without removing that skip from full-run statistics. Native updater still needs a non-container Linux environment.\n'
    (DOC/'TEST_INVENTORY.md').write_text(text,encoding='utf-8')
    (OUT/'go-test-results.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    (OUT/'first-attempt-results.json').write_text(json.dumps(first_attempt,indent=2)+'\n',encoding='utf-8')
    (OUT/'frontend-test-manifest.json').write_text(json.dumps(frontend,indent=2)+'\n',encoding='utf-8')
    commandfile=RAW/'commands.json'
    if commandfile.exists():
        records=json.loads(read(commandfile))
        extra=RAW/'extra/commands.json'
        if extra.exists(): records+=json.loads(read(extra))
        records.sort(key=lambda r:r['utc'])
        rows=[]
        for r in records:
            args=[a.replace(str(ROOT),'$ROOT') for a in r['command']]
            rows.append([r['name'],r['utc'],r['exit'],r['seconds'],' '.join(args)])
        text='# Stage 01 command evidence\n\nLocal Docker execution, archived pinned source; `$ROOT` = repository absolute path. Arguments are shown for audit, not as a shell-escaped copy/paste command; run.py supplies argv directly. Network access is allowed only for dependency/build acquisition, test containers use the isolated internal network. Original upstream source is not edited.\n\n'+table(['ID','UTC start','Exit','Seconds','argv'],rows)
        logs=list(RAW.glob('*.stdout'))+list(RAW.glob('*.stderr'))+list((RAW/'extra').glob('*.stdout'))+list((RAW/'extra').glob('*.stderr'))
        text+='\n## Raw evidence hashes\n\n'+table(['File','SHA-256'],[[p.relative_to(RAW).as_posix(),hashlib.sha256(p.read_bytes()).hexdigest()] for p in sorted(logs)])
        (OUT/'COMMANDS.md').write_text(text,encoding='utf-8')
    print(json.dumps({mode:dict(counts=r['counts'],subtests=r['nested_counts'],gate=r['gate']) for mode,r in results.items()}))


if __name__=='__main__': main()
