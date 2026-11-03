# Ход разработки

**Current continuation:** Candidate RUSTWAVE-BROWSER-PATCH-V1 passed20/20 (5 per required profile), preserving59 assertions and real-timer evidence. Original history remains unchanged. STAGE_01 PARTIAL; browser gate BLOCKED pending explicit new-baseline acceptance. Latest details: “Versioned test-only patch V1”. Earlier sections below are preserved historical checkpoints; their former blockers are superseded only by explicitly recorded supplementary evidence. Go/native gaps are covered by the supplementary runs; current browser-baseline adoption remains pending.

| Этап | Статус | Результат |
|---|---|---|
| 00 Bootstrap | COMPLETE | Подтверждён commit bc5694f61fd407417f1d9a0d3bc57d2d0a8d9123. [Отчёт](stages/STAGE_00_BOOTSTRAP.md) |
| 01 Audit | PARTIAL | Инвентарь 304/304; 248 HTTP/WS; LF 1772/1772; baseline обеих БД измерен. Browser retry PASS, прежний timeout FAIL сохранён; no-skips gate BLOCKED. [Отчёт](stages/STAGE_01_AUDIT.md) |
| 02–15 | NOT_TESTED | Не начаты; автоматического перехода нет |

Go suites: SQLite 124 PASS / 4 SKIPPED; PG 125 PASS / 3 SKIPPED; FAIL=0 и NOT_RUN=0 в исправленной LF-копии. Вложенные результаты и первый ошибочный CRLF-run не скрыты: [test inventory](TEST_INVENTORY.md). 24 frontend unit tests PASS; browser 1 FAIL и 1 PASS при разных ресурсах. Docker image build PASS; отклонённый history logs NOT_RUN. [Baseline](benchmarks/GO_BASELINE.md).

100% относится только к объявленному инвентарю обнаруженного кода. Go↔Rust parity NOT_TESTED; Stable NOT READY. Финальный commit — commit, содержащий этот отчёт, в rustwave-dev; фактический remote SHA проверяется после push.



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

[Full per-ID coverage](audit/SUPPLEMENTARY_COVERAGE.md): 128/128 top-level IDs per mode have PASS evidence after supplementation, with all observed child gaps covered. This is execution coverage, not Go↔Rust compatibility. Full-suite skips are historical facts; effective supplementary coverage is separate.

Browser diagnostic counts: {"browser-gaps01": {"PASS": 3, "FAIL": 6}, "browser-gaps02": {"PASS": 7, "FAIL": 2}, "browser-gaps03": {"PASS": 6}}. V1 includes premature 2-s tool failures; V2 uses original20-s deadline. Control mixed outcomes prove readiness-sensitive **FLAKY**; historical timeout cause remains **BLOCKED**. [Diagnostic report](audit/BROWSER_DIAGNOSTICS.md).

STAGE_01 remains **PARTIAL**, Stage02 **NOT READY**. Go execution gaps are covered; strict browser no-flaky gate remains unresolved. Six baseline trials and source inventory were not rerun.


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
