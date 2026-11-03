# Go baseline — local Docker Desktop

Pinned GoWave `d709bad01dc0ceacb20012a3afdf528eddfd061f`. Corrected LF archive: 1772/1772 Git blobs verified; original CRLF attempt retained in [archive report](../audit/ARCHIVE_INTEGRITY.md).

## Environment and method

Windows host, Docker Desktop 4.97.0 / Engine 29.9.2, WSL Linux amd64, 4 logical CPUs and 4,046,016,512 bytes VM RAM. This is an empty-instance idle baseline, not a throughput/load/capacity test and not a prediction for the 1-vCPU/<1-GiB VPS. VPS not used. Background services remain enabled with zero users/nodes; no concurrent audit build/test workload during measurements.

Reproduce: build the **unmodified upstream Dockerfile** from blob-verified raw/source-lf with COMMIT_SHA pinned, tag rustwave-audit01:upstream-lf, then `python tools/audit-stage01/benchmark.py`. Script creates only its own internal Docker network, an idle Bun HTTP probe sidecar on the internal network (no published ports), 1-CPU/256-MiB nonroot read-only app containers, 1-CPU/512-MiB PostgreSQL container with disposable tmpfs, and removes them after completion. No production volumes or databases are mounted.

Three independent fresh application/database starts per mode. PostgreSQL database is recreated between trials after stopping the prior app. Startup = host monotonic duration from docker start invocation to first HTTP 200 health, including Docker startup/exec/probe overhead; it is not an instrumented pure server.Run duration. PG startup is measured separately to pg_isready. After 20-s warmup, a nominal 30-s idle window samples cgroup v2 usage_usec; CPU = delta / actual monotonic seconds × 100, where 100% is one core. Backend RSS = /proc/1/status VmRSS; cgroup memory.current includes process/cache/tmpfs. PG cgroup values include all DB workers; PG PID1 RSS alone is not total DB RSS. Sampling itself has small docker exec/process overhead. No confidence interval or loaded-dataset claim from n=3.

SQLite is embedded in the Go process: its allocator/cache work is inside backend RSS/CPU. A separate SQLite daemon memory number would be fictitious; recorded as no separate process, not zero incremental cost. PG backend and DB are measured separately and are never conflated into a single backend value. DB tmpfs and memory cache differ from disk-backed production storage.

UTC start: 2026-11-03T02:09:23.070374+00:00. Image ID `sha256:61040df30cfedd64c79cc478a811bffe952db7b7ca14319fcf1c33ae3f94b176`.

## Measured idle results

| DB | Trial | Startup s | Backend RSS MiB | Backend cgroup MiB | Backend CPU % | DB cgroup MiB | DB CPU % | Window s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sqlite | 1 | 0.897 | 32.07 | 15.61 | 0.813 | in-process | in-process | 30.65 |
| sqlite | 2 | 0.661 | 31.66 | 13.69 | 0.876 | in-process | in-process | 30.27 |
| sqlite | 3 | 2.413 | 31.34 | 13.52 | 0.963 | in-process | in-process | 30.66 |
| postgres | 1 | 1.185 | 32.10 | 14.20 | 1.056 | 194.46 | 1.586 | 30.69 |
| postgres | 2 | 1.841 | 30.24 | 12.25 | 0.988 | 213.20 | 0.774 | 30.58 |
| postgres | 3 | 2.992 | 29.99 | 12.17 | 1.471 | 213.54 | 1.113 | 30.49 |

Medians: sqlite: startup 0.897 s, backend RSS 31.66 MiB, backend CPU 0.876%; postgres: startup 1.841 s, backend RSS 30.24 MiB, backend CPU 1.056%.

PostgreSQL startup (separate, one observation): 3.505 s. Image size from docker image inspect Size: **125,660,444 bytes / 119.84 MiB**, local cumulative image size (not registry compressed transfer or shared-disk reclaim size).

## Runtime smoke observations (Go only)

| DB | Request | Status | Content-Type |
| --- | --- | --- | --- |
| sqlite | GET / | 200 | text/html; charset=utf-8 |
| sqlite | GET /dashboard/home | 200 | text/html; charset=utf-8 |
| sqlite | GET /api/unknown-audit-path | 200 | text/html; charset=utf-8 |
| sqlite | GET /assets/missing-audit.js | 404 | text/plain; charset=utf-8 |
| sqlite | GET /missing-audit.html | 200 | text/html; charset=utf-8 |
| sqlite | GET /api/users | 401 | text/plain; charset=utf-8 |
| sqlite | head | 200 | text/html; charset=utf-8 |
| sqlite | metrics_unauthorized | 401 | application/json; charset=utf-8 |
| sqlite | metrics_authorized | 200 | text/plain; version=0.0.4; charset=utf-8 |
| sqlite | metrics_health | 200 | application/json; charset=utf-8 |
| sqlite | metrics_wrong_method | CONNECTION_ERROR |  |
| postgres | GET / | 200 | text/html; charset=utf-8 |
| postgres | GET /dashboard/home | 200 | text/html; charset=utf-8 |
| postgres | GET /api/unknown-audit-path | 200 | text/html; charset=utf-8 |
| postgres | GET /assets/missing-audit.js | 404 | text/plain; charset=utf-8 |
| postgres | GET /missing-audit.html | 200 | text/html; charset=utf-8 |
| postgres | GET /api/users | 401 | text/plain; charset=utf-8 |
| postgres | head | 200 | text/html; charset=utf-8 |
| postgres | metrics_unauthorized | 401 | application/json; charset=utf-8 |
| postgres | metrics_authorized | 200 | text/plain; version=0.0.4; charset=utf-8 |
| postgres | metrics_health | 200 | application/json; charset=utf-8 |
| postgres | metrics_wrong_method | CONNECTION_ERROR |  |

Metrics disabled smoke: {"sqlite": {"api_health_exit": 0, "metrics_health_exit": 1, "pass": true}, "postgres": {"api_health_exit": 0, "metrics_health_exit": 1, "pass": true}}. Connection failure is the expected wrong-method metrics behavior; it is not a successful JSON status. These small smoke checks do not replace the full static/metrics differential matrices.

Complete measured counters: [baseline-measurements.json](../audit/baseline-measurements.json). Only synthetic empty-instance resource counters are published; HTTP bodies and authentication material are omitted.


## Binary artifacts

| Artifact | Bytes | MiB | SHA-256 |
| --- | --- | --- | --- |
| lf-gowave | 28733600 | 27.40 | a409b9a4c95362b4893a34f65109d7d8af47c053326b5f766b37f68da8879e0f |
| gowave-image | 28733600 | 27.40 | 78bc150baf647d3ee2cb57a00b27dac11b6309ffb3a717f04b9d0fa1fc2ae415 |

lf-gowave is the standalone CGO_ENABLED=0 Go 1.27.3-bookworm build with -trimpath -ldflags="-s -w". gowave-image is copied from the final unmodified upstream Dockerfile image (adds version/channel/commit link flags, Alpine build stage). They are distinct build artifacts; do not assume byte identity. Commands/exit codes are in [COMMANDS](../audit/COMMANDS.md). Compiler/base-image versions and digest evidence are preserved with the execution ledger.
