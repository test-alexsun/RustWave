# Передача — STAGE_01_AUDIT

**Final gate review, 2026-11-03:** Browser V1 принят владельцем и прошёл формальную проверку. CI NOT_RUN; browser gate BLOCKED; STAGE_01 PARTIAL до реального CI и окончательной проверки. Исторические секции ниже сохранены и не описывают текущий статус.

Продолжать **этап 01, PARTIAL**; не запускать этап 02 автоматически. Ветка rustwave-dev. Upstream d709bad01dc0ceacb20012a3afdf528eddfd061f. Базовый подтверждённый commit bc5694f61fd407417f1d9a0d3bc57d2d0a8d9123; итоговые отчёты принадлежат commit, содержащему этот файл. Узнать точный SHA: git log -1 --format=%H и git ls-remote origin refs/heads/rustwave-dev. Никаких merge/force push не требуется.

Прочитать [stage report](stages/STAGE_01_AUDIT.md), [test inventory](TEST_INVENTORY.md), [architecture](ARCHITECTURE_BASELINE.md), [functional matrix](FUNCTIONAL_PARITY_MATRIX.md), [baseline](benchmarks/GO_BASELINE.md), [archive integrity](audit/ARCHIVE_INTEGRITY.md), [commands](audit/COMMANDS.md), [fixture hashes](audit/FIXTURES.md) и три parity matrices.

Завершено: 304 inventory items, 248 HTTP/WS operations, 221 frontend callsites, 1772/1772 LF blob matches. Corrected Go suites/vet/fmt, frontend checks/typecheck/unit/build, installer stubs, headers/export/probes/branding и Docker image PASS. 6 baseline trials измерены. Browser первый LF-run FAIL timeout, idle retry PASS; оба сохранены. Buildx history logs НЕ выполнялась из-за auto-review/usage limit; разрешённые ранее сохранённые build/inspect logs подтверждают результат сборки независимо.

Остаётся: строгий no-skips gate (SQLite 4 top + 3 child skips; PG 3 top skips), native updater test требует изолированного non-container Linux, schema export opt-in пишет исходные fixtures и не запускался; root-only test отдельно прошёл UID10001. Browser timeout не имеет доказанной причины. Не считать latest PASS доказательством отсутствия flaky. Все причины в final test ledger; ничего не удалять из manifest. Полные UI/static/metrics/Go↔Rust/architecture differential проверки ещё NOT_TESTED.

Данные сохранены локально в ignored docs/benchmarks/raw: исходный неверный CRLF archive/source, отдельный правильный upstream-lf.tar/source-lf, commands.json, extra/commands.json, baseline.json, версии image digests. Original source не менять. Git core.autocrlf=true создаёт неверный archive без command-local -c core.autocrlf=false. Две ошибки baseline harness (пустые Docker published port bindings в internal network) исправлены probe sidecar внутри сети; не открывать production ports. VPS не использовался.

Быстрая проверка/обновление документов (не повторяет долгие тесты): python tools/audit-stage01/results.py; python tools/audit-stage01/baseline_report.py; python tools/audit-stage01/finalize.py; python tools/audit-stage01/check.py; git diff --check. Source inventory уже построен; при его изменении inventory.py затем features.py перед results.py. Скрипты run.py / browser_retry.py / benchmark.py отказываются затирать имеющиеся свидетельства. Для новой execution-сессии использовать отдельный каталог доказательств; не запускать resume.py поверх успешных логов. Exact argv для выборочного воспроизведения находятся в COMMANDS.md; это список argv, не shell-escaped строка. Browser retry recipe — browser_retry.py, без изменений React/timeout.

Git после публикации должен быть clean и local SHA=origin/rustwave-dev. Upstream push DISABLED. В inherited workflows нет push trigger на rustwave-dev: отсутствие CI run — NOT_RUN. Не публиковать raw logs, DB rows, credentials, caches или binaries. Сохранить AGPL и attribution. Stage 02 — только по отдельной команде пользователя после решения оставшихся gate gaps.

Browser readiness/network/navigation investigation: [diagnostics](audit/BROWSER_DIAGNOSTICS.md). Historical browser console/network telemetry is unavailable; original timeout remains unresolved.



## Execution gaps continuation

Starting confirmed commit 4b9dfb4fc0c62582e38821b54e97b95aed0ceaa8; native workflow commit 8a976f2. Continue Stage01 browser gate only; Stage02 not started. Do not rerun results.py/finalize.py without gaps_report.py afterwards: base generators retain historical checkpoint sections.

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

[Full per-ID coverage](audit/SUPPLEMENTARY_COVERAGE.md): 128/128 top-level IDs per mode have PASS evidence after supplementation, with all observed child gaps covered. This is execution coverage, not Go↔Rust compatibility. Full-suite skips are historical facts; effective supplementary coverage is separate.

Browser diagnostic counts: {"browser-gaps01": {"PASS": 3, "FAIL": 6}, "browser-gaps02": {"PASS": 7, "FAIL": 2}, "browser-gaps03": {"PASS": 6}}. V1 includes premature 2-s tool failures; V2 uses original20-s deadline. Control mixed outcomes prove readiness-sensitive **FLAKY**; historical timeout cause remains **BLOCKED**. [Diagnostic report](audit/BROWSER_DIAGNOSTICS.md).

STAGE_01 remains **PARTIAL**, Stage02 **NOT READY**. Go execution gaps are covered; strict browser no-flaky gate remains unresolved. Six baseline trials and source inventory were not rerun.

Reproduce diagnostics only into a new evidence directory: python tools/audit-stage01/browser_experiment.py <new-name>. Supplement runner refuses existing evidence. Native workflow and JSON artifact evidence retained under ignored raw/gaps01/native. Do not rerun baseline or inventory.

Schema exporter output differs from the initial migration baseline; its test validates generation, not fixture equality. [Hashes and source-only diff](audit/SCHEMA_EXPORT_EVIDENCE.md). Pinned fixtures remain unchanged.


## Readiness and controlled-clock investigation

| Identity | Expected trials | Executed | PASS | FAIL | SKIPPED | NOT_RUN |
| --- | --- | --- | --- | --- | --- | --- |
| Original unchanged | 3 | 3 | 3 | 0 | 0 | 0 |
| External changed-semantics | 12 | 12 | 12 | 0 | 0 | 0 |
| Initial daemon-unavailable attempt | 15 | 0 | 0 | 0 | 0 | 15 |

The first readiness01 attempt failed before starting any container: Docker Desktop Linux Engine named pipe absent. Seven Docker invocations failed to launch the planned 3 original + 12 external trials; classify all 15 trials NOT_RUN/environment BLOCKED, not failed assertions. Installed Docker Desktop was started; successful docker info preceded readiness02. No production/VPS use. Historical results, baseline and Go tests were not rerun.

Original smoke runs execute unmodified `bun run test:browser` and pinned tests/run-browser.mjs. Exercised environment: Linux amd64 Docker tool image, Bun1.4.2, Chromium156.0.8078.73, UTC/C.UTF-8, 2CPU/2000MiB, network none. Upstream documents Bun and local Chromium, not a minimum CPU/RAM SLA; these limits are the documented audit environment, not an invented upstream support guarantee. Three successes cannot erase historical flakiness or establish all-environment stability.

External matrix: normal2CPU/2000MiB, CPU-only1CPU/2000MiB, RAM-only2CPU/1400MiB, contention1CPU/1400MiB plus one CPU-loop process. Three fresh profiles each, same pinned source/dependencies/fixtures. Per-profile bundle builds once; reported trial duration excludes build. The original runner builds every invocation, so command durations are not directly comparable. Source remains read-only and 1772 blobs are reverified. No old evidence is overwritten.

Modal100ms and clock60ms waits are upstream smoke readiness races. A separate DOM/controlled-clock harness preserves assertions but changes wait semantics; it is not replacement evidence for the original smoke. Historical20s timeout root cause remains unresolved. STAGE_01 PARTIAL, browser gate BLOCKED, Stage02 NOT READY. Full analysis and limits: [browser diagnostics](audit/BROWSER_DIAGNOSTICS.md). Reproduce only into a new evidence directory with tools/audit-stage01/readiness_run.py; do not rerun baseline/Go/native/inventory. Starting delivery commit d694945c8bfde9d44b720c0ee0c807ea1db91ead.




## Versioned test-only patch V1

| Run ID | Status | CLI exit | Smoke seconds | Assertion outcomes |
| --- | --- | --- | --- | --- |
| patched-normal-1 | PASS | 0 | 5.358 | 59 |
| patched-normal-2 | PASS | 0 | 4.843 | 59 |
| patched-normal-3 | PASS | 0 | 4.648 | 59 |
| patched-normal-4 | PASS | 0 | 4.489 | 59 |
| patched-normal-5 | PASS | 0 | 4.779 | 59 |
| patched-cpu-only-1 | PASS | 0 | 6.785 | 59 |
| patched-cpu-only-2 | PASS | 0 | 6.296 | 59 |
| patched-cpu-only-3 | PASS | 0 | 7.118 | 59 |
| patched-cpu-only-4 | PASS | 0 | 6.626 | 59 |
| patched-cpu-only-5 | PASS | 0 | 8.647 | 59 |
| patched-ram-only-1 | PASS | 0 | 4.513 | 59 |
| patched-ram-only-2 | PASS | 0 | 4.346 | 59 |
| patched-ram-only-3 | PASS | 0 | 4.293 | 59 |
| patched-ram-only-4 | PASS | 0 | 4.568 | 59 |
| patched-ram-only-5 | PASS | 0 | 4.596 | 59 |
| patched-contention-1 | PASS | 0 | 9.451 | 59 |
| patched-contention-2 | PASS | 0 | 7.454 | 59 |
| patched-contention-3 | PASS | 0 | 9.128 | 59 |
| patched-contention-4 | PASS | 0 | 8.453 | 59 |
| patched-contention-5 | PASS | 0 | 8.756 | 59 |

Candidate `RUSTWAVE-BROWSER-PATCH-V1`; patch SHA256 `0cae2b9c7a6800a6b1c9be9645d438a8beecbce62003f978b4ccbf333c4abf88`. Counts {"PASS": 20, "FAIL": 0, "SKIPPED": 0, "NOT_RUN": 0, "BLOCKED": 0, "FLAKY": 0}. All59 assertions and real native timer evidence preserved; original1772 blobs unchanged. Temporal wait semantics changed explicitly. STAGE_01 PARTIAL; browser gate BLOCKED pending explicit new-baseline acceptance. Historical FAIL/FLAKY remain, original20s timeout root cause unresolved. [Proposal, equivalence limits and preparation errors](audit/BROWSER_PATCH_V1.md). No Stage02 work.

## Final gate review and baseline adoption

[Решение о принятии Browser V1](audit/BROWSER_V1_ADOPTION.md). Новый обязательный baseline зарегистрирован отдельно от original HISTORICAL_FLAKY. Все 59 assertions и 20 успешных запусков перепроверены; 21 отрицательный gate-сценарий PASS. Текущий blocker: обязательный CI ещё не исполнен. Go↔Rust parity NOT_TESTED; STAGE_02 не начат.
