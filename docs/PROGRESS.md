# Ход разработки

**Current continuation:** Go execution gaps covered by supplementary evidence (128/128 top-level IDs per DB); original skips retained. Browser FLAKY/BLOCKED remains; STAGE_01 PARTIAL. The original delivery sections below are historical; current results are in “Execution gaps continuation”.

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
