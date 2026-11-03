"""Final Stage 01 report from preserved execution records, never inferred passes."""
from pathlib import Path
import datetime
import hashlib
import json
import statistics
from inventory import DOC, OUT, table

RAW = DOC / 'benchmarks/raw'


def put(path, text):
    path.write_text(text.rstrip() + '\n', encoding='utf-8')


def section(path, title, text):
    old = path.read_text(encoding='utf-8').split('\n## ' + title)[0]
    put(path, old.rstrip() + '\n\n## ' + title + '\n\n' + text)


def main():
    go = json.loads((OUT/'go-test-results.json').read_text())
    records = json.loads((RAW/'commands.json').read_text()) + json.loads((RAW/'extra/commands.json').read_text())
    commands = {r['name']: r for r in records}
    assert commands['lf-image-build']['exit'] == 0
    assert commands['lf-image-inspect']['exit'] == 0
    assert commands['lf-browser']['exit'] == 1
    assert commands['lf-browser-idle']['exit'] == 0
    assert commands['lf-frontend-test']['exit'] == 0
    assert (RAW/'lf-frontend-test.stderr').read_text(encoding='utf-8').count('(pass) ') == 24
    assert commands['lf-go-nonroot']['exit'] == 0
    nonroot=[json.loads(line) for line in (RAW/'lf-go-nonroot.stdout').read_text().splitlines()]
    assert any(e.get('Test')=='TestRootOnlyWritableRejectsServiceAccountFiles' and e['Action']=='pass' for e in nonroot)
    b = json.loads((RAW/'baseline.json').read_text())
    assert all(len(b['modes'][m]) == 3 for m in ('sqlite', 'postgres'))
    assert all(b['metrics_disabled'][m]['pass'] for m in ('sqlite', 'postgres'))
    for m in ('sqlite', 'postgres'):
        trial = b['modes'][m][0]
        assert [trial[k]['status'] for k in ('metrics_unauthorized','metrics_authorized','metrics_health','metrics_wrong_method')] == [401,200,200,'CONNECTION_ERROR']
    ledger = []
    for mode, r in go.items():
        c = r['counts']
        ledger.append(dict(id='GO-'+mode, expected=128, executed=c.get('PASS',0)+c.get('FAIL',0),
                           passed=c.get('PASS',0), failed=c.get('FAIL',0), skipped=c.get('SKIPPED',0),
                           not_run=c.get('NOT_RUN',0), blocked=sum(v for k,v in c.items() if k!='PASS')))
    ledger += [dict(id='BUN-unit',expected=24,executed=24,passed=24,failed=0,skipped=0,not_run=0,blocked=0),
               dict(id='GO-nonroot-supplement',expected=1,executed=1,passed=1,failed=0,skipped=0,not_run=0,blocked=0),
               dict(id='BROWSER-LF-attempts',expected=2,executed=2,passed=1,failed=1,skipped=0,not_run=0,blocked=1),
               dict(id='BUILDX-history-logs-optional',expected=1,executed=0,passed=0,failed=0,skipped=0,not_run=1,blocked=0)]
    # Command-level checks are distinct from unit IDs and child assertions.
    checks = ['lf-go-fmt-gate','lf-go-fmt-diff','lf-go-vet','lf-go-build','lf-frontend-check',
              'lf-frontend-typecheck','lf-frontend-build','lf-installer','lf-response-headers',
              'lf-contract-export','lf-contract-probes','lf-branding','lf-image-build','lf-image-inspect']
    assert all(commands[k]['exit']==0 for k in checks)
    ledger.append(dict(id='COMMAND-checks',expected=len(checks),executed=len(checks),passed=len(checks),failed=0,skipped=0,not_run=0,blocked=0))
    ledger.append(dict(id='BASELINE-trials',expected=6,executed=6,passed=6,failed=0,skipped=0,not_run=0,blocked=0))
    put(OUT/'final-test-ledger.json', json.dumps({'definition':'EXECUTED=PASS+FAIL. BLOCKED is an overlapping gate count, never an extra terminal status. Do not add parent, child, command and trial rows as equivalent test cases.', 'rows':ledger, 'browser_attempts':[{'id':k,'exit':commands[k]['exit'],'seconds':commands[k]['seconds']} for k in ('lf-browser','lf-browser-idle')], 'stage':'PARTIAL'},indent=2))
    ledger_text=table(['Scope','EXPECTED','EXECUTED','PASS','FAIL','SKIPPED','NOT_RUN','BLOCKED'],[[r[k] for k in ('id','expected','executed','passed','failed','skipped','not_run','blocked')] for r in ledger])
    ledger_text+='''
EXECUTED means a terminal PASS or FAIL; skipped IDs were selected by the runner but their bodies did not complete. BLOCKED overlaps terminal counts and denotes unresolved gate inputs; it is not an additional test outcome. Browser latest execution PASS still has an unresolved earlier timeout. Do not sum parents with child assertions or command/build/trial checks. Go child assertions: SQLite 133 observed, 130 PASS / 3 SKIPPED; PostgreSQL 133 observed, 133 PASS. Child IDs are retained but not independently exhaustive. All 128 source-defined top-level IDs per mode received a terminal runner event; NOT_RUN=0 there. No ignored/xfail/todo results were observed. Parser negative checks reject missing/skip IDs.

Browser attempts on LF source: first **FAIL**, exit 1 / 111.077 s, upstream internal 20-s timeout at tests/run-browser.mjs:81, 1 CPU/1400 MiB during other audit work; retry **PASS**, exit 0 / 79.697 s, 2 CPU/2000 MiB, no concurrent compilation, network none. Both use Bun 1.4.2 and Chromium 156.0.8078.73. React files and timeout unchanged. Resource conditions differ, so the first failure cannot be assigned to an upstream defect or dismissed as resolved nondeterminism. The earlier CRLF browser attempt also hit the harness 1800-s timeout; it is separate invalid-input evidence. This is layout/crypto/locale smoke, not authenticated UI↔API end-to-end testing.

Buildx history logs request was **NOT_RUN**: auto-review did not allow execution when the preceding session exhausted usage. No shell/encoding workaround was used. It is an optional diagnostic, not an unresolved image-build result: saved lf-image-build stderr records completed export/unpack, command exit 0 (525.387 s), and lf-image-inspect exit 0 independently confirms image sha256:61040df30cfedd64c79cc478a811bffe952db7b7ca14319fcf1c33ae3f94b176, 125660444 bytes. Build provenance warning about missing Git metadata is retained; pinned source blobs and COMMIT_SHA build argument supply separate provenance.
'''
    causes='''
| Class | Result / exact reason | Disposition |
|---|---|---|
| Upstream tests / nondeterminism | A minute-boundary branch can skip RepeatedHealthChecksDeduplicateStartJobs; not observed in these runs. Schema exporter deliberately requires GOWAVE_EXPORT_SCHEMA=1 and writes migration source files. | No proven upstream gofmt or Go assertion defect in blob-identical runs. Clock and generator policy need explicit future fixtures. |
| Test environment | TestRootOnlyWritableRejectsServiceAccountFiles skips root in each suite; TestApplyUpdateRequestsRootHelper skips Docker in each suite. | Nonroot supplemental test PASS; original 2 skips remain. Native updater remains BLOCKED pending isolated non-container Linux execution; production/VPS not touched. |
| Test configuration | SQLite suite skips TestMigrateSQLiteToPostgres_Integration and 3 PG child migration tests because GOWAVE_TEST_POSTGRES is absent. TestExportSchema skips in both modes because export flag is absent. | PG mode covers the DSN-dependent cases. Export fixture regeneration NOT_RUN to preserve original fixtures. No skip removed from denominator. |
| Unresolved browser failure | First LF run reached Chromium but did not receive completion within upstream 20 s; idle 2-CPU retry passed. | Both outcomes retained. Cause not proven; strict no-flaky gate remains open. |
| Audit input error | Windows Git core.autocrlf=true converted 1735/1772 archive members; gofmt listed 173 paths despite exit 0. Bash failed on pipefail\\r; frontend check/typecheck/contract text comparison failed. | FAIL retained in first-attempt ledger. Separate LF archive and all 1772 blob hashes verified; corrected checks PASS. No original Go/React edits or gofmt -w. |
| Audit dependencies | First branding invocation lacked git; original browser harness timed out. | Git/Chromium tool image supplies dependencies; branding PASS; browser outcomes above. |
| Audit baseline script | First baseline exited 1 with IndexError on empty port bindings. Diagnostic second attempt exited 1 deliberately: backend was running but internal Docker network returned empty 3000/3001 bindings. No measurements existed. | Fixed only audit harness: probe sidecar inside internal network, no host ports. Six measured trials completed. Both failed attempts recorded, never backend failures. |
| Tool access | Buildx history logs denied execution during previous session usage limit. | NOT_RUN optional diagnostic; saved completed build and inspect evidence suffice. No bypass. |
| Mandatory current gate gaps | Original skips and unresolved first browser timeout. | STAGE_01 PARTIAL; strict PASS and automatic Stage 02 transition prohibited. |
| Future gates, not executed | Real systemd install/update/rollback, live external node/provider/SSH flows, full authenticated UI traces, full static/metrics differential matrix, Rust/architecture parity, original Remnawave fixture regeneration. | NOT_RUN/NOT_TESTED; no complete compatibility claim. Existing Go mocks/goldens and installer stubs are not those checks. |
'''
    section(DOC/'TEST_INVENTORY.md','Final consolidated ledger',ledger_text+'\n'+causes)
    med=[]
    for mode,ts in b['modes'].items():
        med.append(f'{mode}: startup {statistics.median(t["startup_seconds"] for t in ts):.3f} s, backend RSS {statistics.median(t["backend_rss_bytes"] for t in ts)/2**20:.2f} MiB, CPU {statistics.median(t["backend_cpu_percent"] for t in ts):.3f}%')
    pg=b['modes']['postgres']
    baseline='; '.join(med)+f'. PostgreSQL separately: median cgroup memory {statistics.median(t["database"]["cgroup_bytes"] for t in pg)/2**20:.2f} MiB, CPU {statistics.median(t["database"]["cpu_percent"] for t in pg):.3f}%. Image {b["image_bytes"]} bytes; image binary {b["image_binary_bytes"]} bytes.'
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    stage=f'''# STAGE 01 — Audit GoWave

- Status: **PARTIAL**. Inventory and measured baseline completed; strict no-skips/no-flaky gate is not satisfied.
- Started UTC: 2026-11-02. Final local report UTC: {now}.
- Upstream: `d709bad01dc0ceacb20012a3afdf528eddfd061f`.
- Starting RustWave HEAD: `bc5694f61fd407417f1d9a0d3bc57d2d0a8d9123`; branch `rustwave-dev`. Final delivery SHA is the commit containing this report, verified after push; do not confuse the starting SHA with the audit commit.
- Windows host; Docker Desktop 4.97.0 / Engine 29.9.2, Linux amd64 VM 4 CPU / 4,046,016,512 bytes. Test Go 1.27.3, Bun 1.4.2, PG 18.6, Chromium 156.0.8078.73. VPS unused.

## Выполненный инвентарь и источники

**304/304 (100%) объявленных элементов инвентаря**: 248 HTTP/WS method+path операций, 187 уникальных путей, и 56 сквозных/non-HTTP групп. Это охват обнаруженного исходного кода, не 100% поведения или API-совместимости. Отдельно: 2 GET metrics endpoints и 2 static wildcard регистрации; внутри 248 — 1 WebSocket и 2 HEAD. Индексированы 1122 Go declarations в 34 production directories, 221 frontend transport/hook callsites, 218 contract commands, 40 application tables на каждой БД плюс migration ledger, 31 metric families и 8 committed fixtures. Группы перекрываются с реализацией API и не являются независимыми алгоритмами.

Основные документы: [architecture](../ARCHITECTURE_BASELINE.md), [functional matrix](../FUNCTIONAL_PARITY_MATRIX.md), [test inventory](../TEST_INVENTORY.md), [Go baseline](../benchmarks/GO_BASELINE.md), [frontend callsites](../FRONTEND_API_SHAPE_MATRIX.md), [frontend parity](../FRONTEND_API_PARITY.md), [static](../STATIC_SERVING_PARITY.md), [metrics](../METRICS_PARITY.md). Детали: [source surfaces](../audit/SOURCE_SURFACES.md), [complete contract shapes](../audit/CONTRACT_SHAPES.md), [custom frontend shapes](../audit/FRONTEND_CUSTOM.md), [packages](../audit/GO_PACKAGES.md), [symbols](../audit/GO_SYMBOLS.md), [fixtures](../audit/FIXTURES.md).

Auth/scopes/tickets, users/nodes/RPC, profiles/inbounds/hosts/squads, subscriptions/templates/HWID, traffic/history, SQLite/PG migrations, jobs/outbox/cron, notifications, real implementations in stubs, plugins/tools/SSH WS, CLI/import/backup/restore/update, installer/Docker/workflows/static/metrics inventoried. Frontend 3.4.4, React 19.3.1, backend-contract 3.4.15 and Bun 1.4.2 checked against lockfile. Missing/null/empty, envelopes, middleware errors, headers/cookies and UI consumers are recorded; proposed Rust owners remain NOT_STARTED.

## Архив, форматирование и сохранность

[Archive integrity](../audit/ARCHIVE_INTEGRITY.md) preserves all 173 gofmt-listed paths, initial archive hashes and gofmt -d evidence. First gofmt exit 0 with nonempty output is **FAIL**. Git system core.autocrlf=true caused CRLF archive conversion, not a proven formatting defect in pinned upstream. Correct archive used command-local core.autocrlf=false; **1772/1772 Git blob hashes match**, including verification after tests/build. Corrected gofmt -l and gofmt -d empty, strict fmt gate and vet PASS. Original Go/React/install/workflows/license diff against lock is empty. No gofmt -w, reset, clean, force push, Rust implementation or production mutation.

Docker tests used disposable DB storage, synthetic credentials, own resource-limited containers/networks. Baseline uses an internal HTTP probe sidecar with no published ports. SQLite memory remains inside Go process; no fictitious separate DB RAM/CPU. Raw logs, probes, credentials and DB contents are ignored and not published. AGPL-3.0/attribution preserved.

## Команды и фактические результаты

[Exact command ledger](../audit/COMMANDS.md), [test IDs](../audit/go-test-manifest.json), [actual Go outcomes](../audit/go-test-results.json), [first failed archive attempt](../audit/first-attempt-results.json), [final ledger](../audit/final-test-ledger.json). Unit, child, command and benchmark counts use separate denominators.

{ledger_text}

Frontend Biome/typecheck/24 unit tests/production build PASS; installer controlled-stub tests, response-rule headers, exact contract/OpenAPI export and branding PASS. Contract probes validated 88 GET + 182 mutations for each DB (540 schema responses), not 540 unique endpoints or exhaustive behavior.

## Измеренный Go baseline

{baseline}

Three fresh starts per DB, 20-s warmup and 30-s idle windows; 100% CPU = one core. Startup includes Docker/probe overhead. Empty dataset, no nodes/users, no load test. [All trial values, methodology, binary hashes and runtime smoke](../benchmarks/GO_BASELINE.md). These local figures do not predict VPS capacity.

## Расхождения, ограничения и gate

{causes}

All requested source subsystems, consumers, dependencies, DB/CLI/static/metrics surfaces and future determinism requirements are documented. Report/artifact completeness is PASS; stage strict execution gate remains **PARTIAL**, both DB no-skips gates **BLOCKED**. Rust parity **NOT_TESTED**; stable **NOT READY**. No mandatory ID was removed to obtain a green result.

## GitHub / CI и дальнейшая работа

Delivery is committed and pushed only to origin/rustwave-dev after local artifact validation and git diff --check. Remote SHA and GitHub metadata are checked after push; the final response supplies the exact SHA. The inherited workflows have no rustwave-dev push trigger; absence of a CI run is NOT_RUN, not CI PASS. [Actions](https://github.com/test-alexsun/RustWave/actions).

Next allowed task: close remaining Stage 01 execution gaps in an isolated environment, investigate browser timeout, and decide a source-preserving schema-export test strategy. Read [handoff](../HANDOFF.md) and the matrices. **STAGE_02 not started; transition not ready under the strict gate and requires a separate user instruction.**
'''
    put(DOC/'stages/STAGE_01_AUDIT.md',stage)
    put(DOC/'PROGRESS.md','''# Ход разработки

| Этап | Статус | Результат |
|---|---|---|
| 00 Bootstrap | COMPLETE | Подтверждён commit bc5694f61fd407417f1d9a0d3bc57d2d0a8d9123. [Отчёт](stages/STAGE_00_BOOTSTRAP.md) |
| 01 Audit | PARTIAL | Инвентарь 304/304; 248 HTTP/WS; LF 1772/1772; baseline обеих БД измерен. Browser retry PASS, прежний timeout FAIL сохранён; no-skips gate BLOCKED. [Отчёт](stages/STAGE_01_AUDIT.md) |
| 02–15 | NOT_TESTED | Не начаты; автоматического перехода нет |

Go suites: SQLite 124 PASS / 4 SKIPPED; PG 125 PASS / 3 SKIPPED; FAIL=0 и NOT_RUN=0 в исправленной LF-копии. Вложенные результаты и первый ошибочный CRLF-run не скрыты: [test inventory](TEST_INVENTORY.md). 24 frontend unit tests PASS; browser 1 FAIL и 1 PASS при разных ресурсах. Docker image build PASS; отклонённый history logs NOT_RUN. [Baseline](benchmarks/GO_BASELINE.md).

100% относится только к объявленному инвентарю обнаруженного кода. Go↔Rust parity NOT_TESTED; Stable NOT READY. Финальный commit — commit, содержащий этот отчёт, в rustwave-dev; фактический remote SHA проверяется после push.
''')
    put(DOC/'HANDOFF.md','''# Передача — STAGE_01_AUDIT

Продолжать **этап 01, PARTIAL**; не запускать этап 02 автоматически. Ветка rustwave-dev. Upstream d709bad01dc0ceacb20012a3afdf528eddfd061f. Базовый подтверждённый commit bc5694f61fd407417f1d9a0d3bc57d2d0a8d9123; итоговые отчёты принадлежат commit, содержащему этот файл. Узнать точный SHA: git log -1 --format=%H и git ls-remote origin refs/heads/rustwave-dev. Никаких merge/force push не требуется.

Прочитать [stage report](stages/STAGE_01_AUDIT.md), [test inventory](TEST_INVENTORY.md), [architecture](ARCHITECTURE_BASELINE.md), [functional matrix](FUNCTIONAL_PARITY_MATRIX.md), [baseline](benchmarks/GO_BASELINE.md), [archive integrity](audit/ARCHIVE_INTEGRITY.md), [commands](audit/COMMANDS.md), [fixture hashes](audit/FIXTURES.md) и три parity matrices.

Завершено: 304 inventory items, 248 HTTP/WS operations, 221 frontend callsites, 1772/1772 LF blob matches. Corrected Go suites/vet/fmt, frontend checks/typecheck/unit/build, installer stubs, headers/export/probes/branding и Docker image PASS. 6 baseline trials измерены. Browser первый LF-run FAIL timeout, idle retry PASS; оба сохранены. Buildx history logs НЕ выполнялась из-за auto-review/usage limit; разрешённые ранее сохранённые build/inspect logs подтверждают результат сборки независимо.

Остаётся: строгий no-skips gate (SQLite 4 top + 3 child skips; PG 3 top skips), native updater test требует изолированного non-container Linux, schema export opt-in пишет исходные fixtures и не запускался; root-only test отдельно прошёл UID10001. Browser timeout не имеет доказанной причины. Не считать latest PASS доказательством отсутствия flaky. Все причины в final test ledger; ничего не удалять из manifest. Полные UI/static/metrics/Go↔Rust/architecture differential проверки ещё NOT_TESTED.

Данные сохранены локально в ignored docs/benchmarks/raw: исходный неверный CRLF archive/source, отдельный правильный upstream-lf.tar/source-lf, commands.json, extra/commands.json, baseline.json, версии image digests. Original source не менять. Git core.autocrlf=true создаёт неверный archive без command-local -c core.autocrlf=false. Две ошибки baseline harness (пустые Docker published port bindings в internal network) исправлены probe sidecar внутри сети; не открывать production ports. VPS не использовался.

Быстрая проверка/обновление документов (не повторяет долгие тесты): python tools/audit-stage01/results.py; python tools/audit-stage01/baseline_report.py; python tools/audit-stage01/finalize.py; python tools/audit-stage01/check.py; git diff --check. Source inventory уже построен; при его изменении inventory.py затем features.py перед results.py. Скрипты run.py / browser_retry.py / benchmark.py отказываются затирать имеющиеся свидетельства. Для новой execution-сессии использовать отдельный каталог доказательств; не запускать resume.py поверх успешных логов. Exact argv для выборочного воспроизведения находятся в COMMANDS.md; это список argv, не shell-escaped строка. Browser retry recipe — browser_retry.py, без изменений React/timeout.

Git после публикации должен быть clean и local SHA=origin/rustwave-dev. Upstream push DISABLED. В inherited workflows нет push trigger на rustwave-dev: отсутствие CI run — NOT_RUN. Не публиковать raw logs, DB rows, credentials, caches или binaries. Сохранить AGPL и attribution. Stage 02 — только по отдельной команде пользователя после решения оставшихся gate gaps.
''')
    section(DOC/'ARCHITECTURE_BASELINE.md','Final audit execution evidence',
            'Source inventory: 304 declared items, 248 HTTP/WS operations and 221 frontend callsites; 1772/1772 LF upstream blobs unchanged after execution. First CRLF formatting FAIL and source provenance are preserved in [archive integrity](audit/ARCHIVE_INTEGRITY.md). Measured Go/DB baseline is in [GO_BASELINE](benchmarks/GO_BASELINE.md). Both corrected Go suites and frontend checks ran; skips, first browser timeout and successful idle retry remain in [test ledger](TEST_INVENTORY.md). Docker build/inspect PASS independently of the denied optional Buildx history command (NOT_RUN). Strict stage gate PARTIAL; Rust compatibility NOT_TESTED. No Rust backend implemented.')
    section(DOC/'FUNCTIONAL_PARITY_MATRIX.md','Final audit status',
            'Source inventory is 304/304 declared items; all proposed Rust statuses remain NOT_STARTED. [Execution ledger](TEST_INVENTORY.md) and [baseline](benchmarks/GO_BASELINE.md) distinguish Go-only evidence from future parity. STAGE_01 PARTIAL because required execution skips and an unresolved browser timeout remain. No API compatibility percentage is claimed.')
    # Publish only known-safe versions/digests; no full Docker inspect environment.
    put(OUT/'environment.json',(RAW/'environment.json').read_text())
    extra='\nBaseline command: `python tools/audit-stage01/benchmark.py`, final exit 0 after two exit-1 harness attempts; see stage report for exact errors. Final raw baseline SHA-256: `'+hashlib.sha256((RAW/'baseline.json').read_bytes()).hexdigest()+'`. All six trial counters and UTC start are in [baseline measurements](baseline-measurements.json).\n\nBuildx history logs: NOT_RUN (previous auto-review/usage-limit rejection); no execution exit code exists. Saved build and image-inspect records above are independent executed evidence.\n'
    section(OUT/'COMMANDS.md','Final continuation evidence',extra)
    print('Final reports: PARTIAL, inventory complete, execution gaps retained')


if __name__ == '__main__':
    main()
