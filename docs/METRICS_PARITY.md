# Metrics inventory / future parity

Source `d709bad01dc0ceacb20012a3afdf528eddfd061f`. Exact **31 families** (4 counters, 27 gauges), HELP, TYPE, labels: [METRIC_FAMILIES](audit/METRIC_FAMILIES.md). Prefix remnawave, default app="remnawave" intentionally retained. Units follow names/help. Do not turn gauges named total into counters.

| ID | Go behavior | Evidence / future fixture |
|---|---|---|
| MET-01 | Separate listener AppHost:METRICS_PORT, default 127.0.0.1:3001; Docker 0.0.0.0 inside namespace. | config.go, server.Start; both DB listener fixtures |
| MET-02 | METRICS_ENABLED defaults true; only case-insensitive trimmed false disables. Empty configured port also prevents listener. Exporter still starts; bind failure logs without stopping API. | config/server source; disabled runtime fixture |
| MET-03 | GET /metrics, BasicAuth, nonempty configured credentials, constant-time compare. 401 JSON message/statusCode; WWW-Authenticate realm also set on success. | prometheus/server.go and tests |
| MET-04 | text/plain; version=0.0.4; charset=utf-8. Preserve registration order, HELP/TYPE, labels/escaping and float/NaN/Inf representation. | registry_test.go, prom-vectors.json |
| MET-05 | Public GET /health on metrics listener: DB ping deadline 5s, info/error/details envelope, 200/503. | prometheus tests; DB failure fixture |
| MET-06 | Other paths/methods including HEAD /metrics close connection via Hijack / ErrAbortHandler; not JSON 404/405. | prometheus tests; runtime wrong-method smoke |
| MET-07 | Export 15s; user cache 1min; series sync 6h. ACTIVE/DISABLED/LIMITED/EXPIRED and onlineNow/lastDay/lastWeek/neverOnline. | exporter.go; controlled clock/cache fixtures |
| MET-08 | Basic/system labels include node identity/provider/tags/arch. Missing hot-system data removes system gauges; status/online remain. Sync early returns for zero DB rows. | exporter tests; add/delete/disconnect transitions |
| MET-09 | Traffic counters increment node_uuid+tag; negative/NaN increments ignored. Network-total gauges mean OS-since-boot. | registry/definitions + node event fixtures |
| MET-10 | Runtime procfs RSS, Go heap/goroutines; external/arrayBuffers/eventLoop zero. instance_id default 0, instance_name api. | rss.go/exporter.go; system stats tests |
| MET-11 | API stats, bandwidth, nodes, recap, http, nodes/metrics and health are distinct JSON surfaces. | handlers/probes and frontend schemas |

SQLite/PG differential status: **NOT_TESTED**, no Rust fixtures. [Tests](TEST_INVENTORY.md) report Go-only results; [baseline](benchmarks/GO_BASELINE.md) records empty-instance measurements. Future `tests/compatibility/metrics/` NOT_CREATED. Dynamic values need per-field tolerances; families/HELP/TYPE/labels/auth/listener require exact match. No normalizations approved.

## Executed Go runtime smoke

Both DB modes: unauthenticated GET /metrics → 401; correct BasicAuth → 200; GET /health → 200; POST /metrics closes connection. METRICS_ENABLED=false leaves API health working and metrics listener unavailable. Empty-instance text retained in ignored raw evidence; this is not a full populated 31-family/system-stat differential test. [Baseline](benchmarks/GO_BASELINE.md); no Rust parity executed.
