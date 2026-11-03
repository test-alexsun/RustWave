# Static-serving inventory / future parity

Source `d709bad01dc0ceacb20012a3afdf528eddfd061f`; `backend-go/internal/server/{server,dashboard}.go`, `frontend/{vite.config.ts,scripts/editor-assets.cjs}`. Go test evidence: [TEST_INVENTORY](TEST_INVENTORY.md); runtime smoke: [GO_BASELINE](benchmarks/GO_BASELINE.md). Every Go↔Rust row remains **NOT_TESTED** on SQLite/PostgreSQL. Stage 02 must turn these IDs into fixtures; Stage 11 must execute the complete gate.

| ID | Actual source behavior / required fixture | Existing Go evidence |
|---|---|---|
| STATIC-01 | First existing path at NewApp: ./frontend/dist, ./dist, ../frontend/dist, ./static, /opt/gowave/frontend/dist, /opt/gowave/dist; no embedded frontend. Stat checks existence, not directory type. No candidate → no wildcard. | server.go; full root ordering/no-root matrix not covered |
| STATIC-02 | PANEL_BASE_PATH normalized; dashboard/static only. Bare mount 308 with query; outside prefix 404. Replace one base marker in index. | TestDashboardMount, TestDashboardPrefixPreservesAPI, config tests |
| STATIC-03 | GET/HEAD wildcard; extensionless → index; missing file with extension other than .html → 404. Missing .html also falls back to index. | TestDashboardMount; .html edge needs fixture |
| STATIC-04 | fs.ValidPath rejects dot/traversal segments. Need router URL decoding, encoded slash/dots, null bytes, symlink/private-file cases; lexical check alone does not prove symlink isolation. | traversal subset in TestDashboardMount; full private matrix NOT_RUN |
| STATIC-05 | Existing API routes take priority. Unknown extensionless /api path may hit SPA when base=/; no explicit API rejection in dashboardHandler. Verify router before defining Rust behavior. | Existing test covers known health/users with non-root base; baseline smoke |
| STATIC-06 | /assets/foo fallback strips assets/ and checks root, including WASM/schema/runtime. | TestDashboardMount, TestDashboardPrecompressedAssets |
| STATIC-07 | .gz preferred if acceptsGzip; Vary Accept-Encoding whenever packed exists. gzip q=0 rejected; wildcard encoding ignored and malformed q may count as accepted. | gzip/q=.5/q=0/identity tested; other cases need fixtures |
| STATIC-08 | Only .gz and gzip refused → streaming decode + Last-Modified; corrupt gzip → 500. HEAD omits body. Packed accepted → ServeContent compressed bytes + Content-Encoding gzip. | TestDashboardPrecompressedAssets; decoded HEAD/range/conditional matrix needed |
| STATIC-09 | Plain file uses http.ServeContent: standard Content-Length, modification/conditional/range behavior. No explicit ETag. Decompressed-only branch differs. | range/If-Modified-Since/ETag dedicated fixtures NOT_RUN |
| STATIC-10 | NewApp sets .wasm application/wasm, .json application/json, .js application/javascript. Direct helper tests can observe platform text/javascript because they bypass NewApp MIME registration. | helper tests plus router-level fixture required |
| STATIC-11 | index/manifest Cache-Control no-cache,no-store,must-revalidate; manifest start_url/scope/id rewritten to base; application/manifest+json; HEAD no body. | TestDashboardMount |
| STATIC-12 | editor:download fetches hash-pinned WASM/runtime/schema; compress keeps main.wasm only as gz; browser lazy loads runtime. Go/Rust must use same dist build. | Dockerfile, editor-assets.cjs; browser evidence separate |

Future `tests/compatibility/static/` NOT_CREATED: Stage 01 must not implement Rust. Compare status, raw bytes or decoded body as appropriate, Content-Type/Encoding/Length, Vary, Cache-Control, Last-Modified, ETag/Range and error bodies. Fixed mtime/build and root/non-root mount required. No blanket HTML fallback normalization.

## Executed Go runtime smoke

On both SQLite and PostgreSQL in the built LF image: GET / and /dashboard/home → 200 HTML; unknown extensionless /api/unknown-audit-path → **200 HTML SPA**, not API JSON 404; missing .js → 404; missing .html → 200 HTML; protected /api/users → 401; HEAD dashboard → 200 with empty body. These are observed upstream behaviors to preserve or explicitly discuss later, not fixes applied here. See [measured baseline](benchmarks/GO_BASELINE.md). Full range/cache/traversal/private-file and Go↔Rust matrices remain NOT_TESTED.
