# STAGE 01 — Audit GoWave

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
