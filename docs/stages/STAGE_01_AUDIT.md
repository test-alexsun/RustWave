# STAGE 01 — Audit GoWave

**Current continuation:** Original smoke 3/3 PASS in the latest bounded control run; separate readiness/controlled-clock test 12/12 PASS. Historical browser FLAKY remains FAIL for gate; exact original timeout cause unresolved. STAGE_01 PARTIAL. Latest details: “Readiness and controlled-clock investigation”.

- Status: **PARTIAL**. Inventory and measured baseline completed; strict no-skips/no-flaky gate is not satisfied.
- Started UTC: 2026-11-02. Final local report UTC: 2026-11-03T02:23:41.317763+00:00.
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

| Scope | EXPECTED | EXECUTED | PASS | FAIL | SKIPPED | NOT_RUN | BLOCKED |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GO-sqlite | 128 | 124 | 124 | 0 | 4 | 0 | 4 |
| GO-postgres | 128 | 125 | 125 | 0 | 3 | 0 | 3 |
| BUN-unit | 24 | 24 | 24 | 0 | 0 | 0 | 0 |
| GO-nonroot-supplement | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| BROWSER-LF-attempts | 2 | 2 | 1 | 1 | 0 | 0 | 1 |
| BUILDX-history-logs-optional | 1 | 0 | 0 | 0 | 0 | 1 | 0 |
| COMMAND-checks | 14 | 14 | 14 | 0 | 0 | 0 | 0 |
| BASELINE-trials | 6 | 6 | 6 | 0 | 0 | 0 | 0 |

EXECUTED means a terminal PASS or FAIL; skipped IDs were selected by the runner but their bodies did not complete. BLOCKED overlaps terminal counts and denotes unresolved gate inputs; it is not an additional test outcome. Browser latest execution PASS still has an unresolved earlier timeout. Do not sum parents with child assertions or command/build/trial checks. Go child assertions: SQLite 133 observed, 130 PASS / 3 SKIPPED; PostgreSQL 133 observed, 133 PASS. Child IDs are retained but not independently exhaustive. All 128 source-defined top-level IDs per mode received a terminal runner event; NOT_RUN=0 there. No ignored/xfail/todo results were observed. Parser negative checks reject missing/skip IDs.

Browser attempts on LF source: first **FAIL**, exit 1 / 111.077 s, upstream internal 20-s timeout at tests/run-browser.mjs:81, 1 CPU/1400 MiB during other audit work; retry **PASS**, exit 0 / 79.697 s, 2 CPU/2000 MiB, no concurrent compilation, network none. Both use Bun 1.4.2 and Chromium 156.0.8078.73. React files and timeout unchanged. Resource conditions differ, so the first failure cannot be assigned to an upstream defect or dismissed as resolved nondeterminism. The earlier CRLF browser attempt also hit the harness 1800-s timeout; it is separate invalid-input evidence. This is layout/crypto/locale smoke, not authenticated UI↔API end-to-end testing.

Buildx history logs request was **NOT_RUN**: auto-review did not allow execution when the preceding session exhausted usage. No shell/encoding workaround was used. It is an optional diagnostic, not an unresolved image-build result: saved lf-image-build stderr records completed export/unpack, command exit 0 (525.387 s), and lf-image-inspect exit 0 independently confirms image sha256:61040df30cfedd64c79cc478a811bffe952db7b7ca14319fcf1c33ae3f94b176, 125660444 bytes. Build provenance warning about missing Git metadata is retained; pinned source blobs and COMMIT_SHA build argument supply separate provenance.


Frontend Biome/typecheck/24 unit tests/production build PASS; installer controlled-stub tests, response-rule headers, exact contract/OpenAPI export and branding PASS. Contract probes validated 88 GET + 182 mutations for each DB (540 schema responses), not 540 unique endpoints or exhaustive behavior.

## Измеренный Go baseline

sqlite: startup 0.897 s, backend RSS 31.66 MiB, CPU 0.876%; postgres: startup 1.841 s, backend RSS 30.24 MiB, CPU 1.056%. PostgreSQL separately: median cgroup memory 213.20 MiB, CPU 1.113%. Image 125660444 bytes; image binary 28733600 bytes.

Three fresh starts per DB, 20-s warmup and 30-s idle windows; 100% CPU = one core. Startup includes Docker/probe overhead. Empty dataset, no nodes/users, no load test. [All trial values, methodology, binary hashes and runtime smoke](../benchmarks/GO_BASELINE.md). These local figures do not predict VPS capacity.

## Расхождения, ограничения и gate


| Class | Result / exact reason | Disposition |
|---|---|---|
| Upstream tests / nondeterminism | A minute-boundary branch can skip RepeatedHealthChecksDeduplicateStartJobs; not observed in these runs. Schema exporter deliberately requires GOWAVE_EXPORT_SCHEMA=1 and writes migration source files. | No proven upstream gofmt or Go assertion defect in blob-identical runs. Clock and generator policy need explicit future fixtures. |
| Test environment | TestRootOnlyWritableRejectsServiceAccountFiles skips root in each suite; TestApplyUpdateRequestsRootHelper skips Docker in each suite. | Nonroot supplemental test PASS; original 2 skips remain. Native updater remains BLOCKED pending isolated non-container Linux execution; production/VPS not touched. |
| Test configuration | SQLite suite skips TestMigrateSQLiteToPostgres_Integration and 3 PG child migration tests because GOWAVE_TEST_POSTGRES is absent. TestExportSchema skips in both modes because export flag is absent. | PG mode covers the DSN-dependent cases. Export fixture regeneration NOT_RUN to preserve original fixtures. No skip removed from denominator. |
| Unresolved browser failure | First LF run reached Chromium but did not receive completion within upstream 20 s; idle 2-CPU retry passed. | Both outcomes retained. Cause not proven; strict no-flaky gate remains open. |
| Audit input error | Windows Git core.autocrlf=true converted 1735/1772 archive members; gofmt listed 173 paths despite exit 0. Bash failed on pipefail\r; frontend check/typecheck/contract text comparison failed. | FAIL retained in first-attempt ledger. Separate LF archive and all 1772 blob hashes verified; corrected checks PASS. No original Go/React edits or gofmt -w. |
| Audit dependencies | First branding invocation lacked git; original browser harness timed out. | Git/Chromium tool image supplies dependencies; branding PASS; browser outcomes above. |
| Audit baseline script | First baseline exited 1 with IndexError on empty port bindings. Diagnostic second attempt exited 1 deliberately: backend was running but internal Docker network returned empty 3000/3001 bindings. No measurements existed. | Fixed only audit harness: probe sidecar inside internal network, no host ports. Six measured trials completed. Both failed attempts recorded, never backend failures. |
| Tool access | Buildx history logs denied execution during previous session usage limit. | NOT_RUN optional diagnostic; saved completed build and inspect evidence suffice. No bypass. |
| Mandatory current gate gaps | Original skips and unresolved first browser timeout. | STAGE_01 PARTIAL; strict PASS and automatic Stage 02 transition prohibited. |
| Future gates, not executed | Real systemd install/update/rollback, live external node/provider/SSH flows, full authenticated UI traces, full static/metrics differential matrix, Rust/architecture parity, original Remnawave fixture regeneration. | NOT_RUN/NOT_TESTED; no complete compatibility claim. Existing Go mocks/goldens and installer stubs are not those checks. |


All requested source subsystems, consumers, dependencies, DB/CLI/static/metrics surfaces and future determinism requirements are documented. Report/artifact completeness is PASS; stage strict execution gate remains **PARTIAL**, both DB no-skips gates **BLOCKED**. Rust parity **NOT_TESTED**; stable **NOT READY**. No mandatory ID was removed to obtain a green result.

## GitHub / CI и дальнейшая работа

Delivery is committed and pushed only to origin/rustwave-dev after local artifact validation and git diff --check. Remote SHA and GitHub metadata are checked after push; the final response supplies the exact SHA. The inherited workflows have no rustwave-dev push trigger; absence of a CI run is NOT_RUN, not CI PASS. [Actions](https://github.com/test-alexsun/RustWave/actions).

Next allowed task: close remaining Stage 01 execution gaps in an isolated environment, investigate browser timeout, and decide a source-preserving schema-export test strategy. Read [handoff](../HANDOFF.md) and the matrices. **STAGE_02 not started; transition not ready under the strict gate and requires a separate user instruction.**

Browser readiness/network/navigation investigation: [diagnostics](../audit/BROWSER_DIAGNOSTICS.md). Historical browser console/network telemetry is unavailable; original timeout remains unresolved.



## Execution gaps continuation

Native updater and root-writability tests PASS on non-container GitHub-hosted Ubuntu 24.04 VM, UID1001, Go1.27.3. Both tests use t.TempDir; no production services or VPS. Job preflight asserts nonroot and no /.dockerenv. [Actions run](https://github.com/test-alexsun/RustWave/actions/runs/41566960948).

Schema export PASS in separate raw/gaps01/schema-source, never original LF snapshot. It internally generates SQLite and PostgreSQL SQL; generated files are disposable evidence, not replacements for committed fixtures. Migration integration and migration children PASS with separate PostgreSQL18 tmpfs. Root test also retains its earlier nonroot Docker PASS. Original top-level full-suite results remain SQLite124PASS/4SKIPPED, PG125PASS/3SKIPPED, NOT_RUN0; SQLite child130PASS/3SKIPPED and PG child133PASS.

New execution accounting (separate from historical runs):

| Scope | EXPECTED | EXECUTED | PASS | FAIL | SKIPPED | NOT_RUN | BLOCKED | FLAKY |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Go supplementary top-level | 12 | 12 | 12 | 0 | 0 | 0 | 0 | 0 |
| Browser V1 (includes tool errors) | 9 | 9 | 3 | 6 | 0 | 0 | 1 | 1 |
| Browser V2 corrected deadline | 9 | 9 | 7 | 2 | 0 | 0 | 1 | 1 |
| Browser CPU/RAM isolated | 6 | 6 | 6 | 0 | 0 | 0 | 0 | 0 |

BLOCKED and FLAKY overlap terminal outcomes; never add them as extra test cases. V1 includes five premature CDP timeouts and one readiness failure. V2+isolated valid diagnostics total15 executions:13PASS/2FAIL, both failures in CPU-contention. No OOM or Network.loadingFailed in those15. CPU contention used95–100% of one core; observed final cgroup memory825–872MiB includes Chromium/harness/cache and is not backend RSS.

| Label | Supplement | Top-level IDs | All observed IDs | Result |
| --- | --- | --- | --- | --- |
| sqlite | schema | 1 | 1 | PASS |
| sqlite | migration | 3 | 7 | PASS |
| sqlite | native | 2 | 2 | PASS |
| postgres | schema | 1 | 1 | PASS |
| postgres | migration | 3 | 7 | PASS |
| postgres | native | 2 | 2 | PASS |

[Full per-ID coverage](../audit/SUPPLEMENTARY_COVERAGE.md): 128/128 top-level IDs per mode have PASS evidence after supplementation, with all observed child gaps covered. This is execution coverage, not Go↔Rust compatibility. Full-suite skips are historical facts; effective supplementary coverage is separate.

Browser diagnostic counts: {"browser-gaps01": {"PASS": 3, "FAIL": 6}, "browser-gaps02": {"PASS": 7, "FAIL": 2}, "browser-gaps03": {"PASS": 6}}. V1 includes premature 2-s tool failures; V2 uses original20-s deadline. Control mixed outcomes prove readiness-sensitive **FLAKY**; historical timeout cause remains **BLOCKED**. [Diagnostic report](../audit/BROWSER_DIAGNOSTICS.md).

STAGE_01 remains **PARTIAL**, Stage02 **NOT READY**. Go execution gaps are covered; strict browser no-flaky gate remains unresolved. Six baseline trials and source inventory were not rerun.

Schema exporter output differs from the initial migration baseline; its test validates generation, not fixture equality. [Hashes and source-only diff](../audit/SCHEMA_EXPORT_EVIDENCE.md). Pinned fixtures remain unchanged.


## Readiness and controlled-clock investigation

| Identity | Expected trials | Executed | PASS | FAIL | SKIPPED | NOT_RUN |
| --- | --- | --- | --- | --- | --- | --- |
| Original unchanged | 3 | 3 | 3 | 0 | 0 | 0 |
| External changed-semantics | 12 | 12 | 12 | 0 | 0 | 0 |
| Initial daemon-unavailable attempt | 15 | 0 | 0 | 0 | 0 | 15 |

The first readiness01 attempt failed before starting any container: Docker Desktop Linux Engine named pipe absent. Seven Docker invocations failed to launch the planned 3 original + 12 external trials; classify all 15 trials NOT_RUN/environment BLOCKED, not failed assertions. Installed Docker Desktop was started; successful docker info preceded readiness02. No production/VPS use. Historical results, baseline and Go tests were not rerun.

Original smoke runs execute unmodified `bun run test:browser` and pinned tests/run-browser.mjs. Exercised environment: Linux amd64 Docker tool image, Bun1.4.2, Chromium156.0.8078.73, UTC/C.UTF-8, 2CPU/2000MiB, network none. Upstream documents Bun and local Chromium, not a minimum CPU/RAM SLA; these limits are the documented audit environment, not an invented upstream support guarantee. Three successes cannot erase historical flakiness or establish all-environment stability.

External matrix: normal2CPU/2000MiB, CPU-only1CPU/2000MiB, RAM-only2CPU/1400MiB, contention1CPU/1400MiB plus one CPU-loop process. Three fresh profiles each, same pinned source/dependencies/fixtures. Per-profile bundle builds once; reported trial duration excludes build. The original runner builds every invocation, so command durations are not directly comparable. Source remains read-only and 1772 blobs are reverified. No old evidence is overwritten.

Modal100ms and clock60ms waits are upstream smoke readiness races. A separate DOM/controlled-clock harness preserves assertions but changes wait semantics; it is not replacement evidence for the original smoke. Historical20s timeout root cause remains unresolved. STAGE_01 PARTIAL, browser gate BLOCKED, Stage02 NOT READY. Full analysis and limits: [browser diagnostics](../audit/BROWSER_DIAGNOSTICS.md). Reproduce only into a new evidence directory with tools/audit-stage01/readiness_run.py; do not rerun baseline/Go/native/inventory. Starting delivery commit d694945c8bfde9d44b720c0ee0c807ea1db91ead.
