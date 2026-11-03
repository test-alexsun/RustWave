# Test-only browser baseline V1 proposal

Candidate identity **RUSTWAVE-BROWSER-PATCH-V1**; original **GOWAVE-BROWSER-ORIGINAL-d709bad01dc0ceacb20012a3afdf528eddfd061f**. Patch SHA256 `0cae2b9c7a6800a6b1c9be9645d438a8beecbce62003f978b4ccbf333c4abf88`. Published patch uses zero-context diff to avoid whitespace-only context lines flagged by git diff --check. The20 runs used the full-context representation; both apply to byte-identical TSX, verified in browser-patch-v1-packaging.json. Both hashes and raw tested patch are retained. This is a packaging-only change, not a browser retest or code change. This is an authorized test-only candidate, not an unchanged upstream smoke. Upstream SHA `d709bad01dc0ceacb20012a3afdf528eddfd061f`. Only the temporary copy of frontend/tests/browser-smoke.tsx is changed. All1772 original blobs match; other1771 temporary-copy files and all fixtures match. Original tests/run-browser.mjs remains byte-identical; validation uses a separate versioned external CDP supervisor, whose hash is recorded in browser-patch-v1-results.json.

Twenty independent containers/browser processes with clean profiles, five per profile: normal2CPU/2000MiB; CPU-only1CPU/2000MiB; RAM-only2CPU/1400MiB; contention1CPU/1400MiB plus one controlled CPU loop during browser lifetime. Pinned image/Bun/Chromium/UTC/locale/fixtures identical. One immutable compiled bundle is reused; first invocation includes build time, smoke duration excludes it. Network none. Startup10s and outer smoke20s deadlines unchanged; deadline begins before navigation in this supervisor. Internal readiness bound19s does not extend outer20s. Every invocation has saved stdout/stderr, actual process exit, CDP events/exceptions/errors, snapshots, resource counters (throttling and memory.events) and timeout details.

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


Counts: {"PASS": 20, "FAIL": 0, "SKIPPED": 0, "NOT_RUN": 0, "BLOCKED": 0, "FLAKY": 0}. Full59 assertion identities and outcomes are retained per run. AST verification confirms all59 original assert argument expressions/expected values and their order match after explicit CRLF-to-LF whitespace normalization. Windows Git applied CRLF only to the changed test file; four multiline argument expressions differ solely at line breaks. Literal values are unchanged. Runtime manifests match the same59 message identities. Registered/delivered native timer events and DOM advancement are separately captured; Date.now and native scheduling are not replaced.

### Changes and equivalence argument

The modal fixed100ms wait becomes bounded readiness for an opened, visible dialog with a committed JSON-viewer/string element; the original value/read-only/mutation assertions remain. The clock fixed60ms wait becomes bounded confirmation of registration of the actual20ms native interval, callback delivery, state update and visible DOM time advancement; the original greater-than assertion remains. Test-only interval observation delegates to native setInterval and restores the wrapper in finally. No production hook or API behavior is patched. This candidate therefore retains a real-timer test rather than substituting a synthetic clock.

Timing acceptance **does change**: a slow but correctly committed update may pass within the bounded readiness window instead of being sampled after100/60ms. This removes unsupported fixed-sleep synchronization assumptions, not an explicitly documented application latency SLA. That change needs explicit baseline acceptance; identical assertions alone do not prove identical temporal semantics. Other legacy waits remain;20 passes cannot prove universal absence of flakes.

### Historical outcomes and preparation failures

Original immutable smoke most recently passed3/3 but retains its historical20s timeout FAIL. Earlier external instrumentation demonstrated viewer readiness and clock-contention FLAKY; those results remain distinct and unchanged. The historical20s timeout has no proven root cause; this patch does not claim to explain it.

Auto-review first timed out before execution; one permitted identical retry proceeded. Preparation results/ contains20 Docker exit125 mount failures (new read-only copy lacked node_modules mountpoint): no browser test executed. results02/ contains20 external-runner ReferenceError failures before page navigation (html scope defect): browser processes started but59 assertions were NOT_RUN. These tool FAIL logs and their failed runner snapshot are retained. Mountpoint and runner scope were corrected; results03/ is the requested20-case assertion validation. The initial AST checker also failed to load the TypeScript compiler API (the pinned TypeScript7 package has no legacy JS API); the installed Prettier TypeScript parser was used instead. Its first strict source-text comparison detected four CRLF-only multiline whitespace differences; explicit CRLF normalization resolved those with unchanged literal values. These checker failures are retained as audit-tool findings, not application assertion failures. No failed browser assertion was retried to obtain a green result. Further environment/programming errors now abort the series rather than repeatedly failing remaining cases.

### Gate recommendation — no automatic promotion

**STAGE_01 PARTIAL; browser gate BLOCKED pending explicit acceptance of a new mandatory test baseline.** Historical original FLAKY remains FAIL under unchanged GATE_POLICY. The adoption proposal is to register this precise patch+runner+assertion manifest as the new mandatory test identity, with the preserved original history and the explicit temporal-semantics change above. This is a baseline revision, not an exemption or relabelling historical FAIL as PASS. If any candidate trial failed or is missing, those gaps additionally block adoption. Final Stage01 closure requires explicit baseline approval plus review of all current mandatory evidence; no automatic Stage02 transition.

Reproduce from the immutable LF archive with prepare_browser_patch.py (refuses an existing copy), then validate_browser_patch.py (refuses existing evidence), AST check_browser_patch.cjs, and report_browser_patch.py. Use fresh evidence paths for any future run. Patch and identity live in tools/audit-stage01/. No Go tests, native tests, inventory or baseline measurements were repeated.

## Full assertion manifest

| ID | Unchanged expected assertion |
| --- | --- |
| BROWSER-A01 | JSON viewer renders inbound values |
| BROWSER-A02 | Inbound JSON remains read-only after interaction |
| BROWSER-A03 | Inbound JSON viewer hides mutation controls |
| BROWSER-A04 | virtual list bounds rendered rows |
| BROWSER-A05 | virtual list renders first row |
| BROWSER-A06 | virtual list drops rows outside viewport |
| BROWSER-A07 | virtual list observes variable row heights |
| BROWSER-A08 | virtual list handles shrinking data |
| BROWSER-A09 | window virtualization tracks scroll and margin |
| BROWSER-A10 | window virtualization bounds rows |
| BROWSER-A11 | remarks initialize from props |
| BROWSER-A12 | adding a remark reports immediately |
| BROWSER-A13 | removing a remark preserves surviving input identity |
| BROWSER-A14 | removed remark input detaches |
| BROWSER-A15 | remarks reset on new data |
| BROWSER-A16 | remarks do not echo parent data back |
| BROWSER-A17 | typing a remark reports immediately |
| BROWSER-A18 | omitted remarks have a stable empty default |
| BROWSER-A19 | tag input initializes from props |
| BROWSER-A20 | tag input follows changed values |
| BROWSER-A21 | session clock advances without render-time reads |
| BROWSER-A22 | valid SVG |
| BROWSER-A23 | SVG with comments |
| BROWSER-A24 | reject malformed SVG |
| BROWSER-A25 | reject non-SVG root |
| BROWSER-A26 | SVG without xmlns retains SVG namespace |
| BROWSER-A27 | SVG strips active content |
| BROWSER-A28 | non-SVG roots are rejected |
| BROWSER-A29 | auth initializes without token |
| BROWSER-A30 | auth reacts to token changes |
| BROWSER-A31 | logout updates context and removes token |
| BROWSER-A32 | repeated logout remains safe |
| BROWSER-A33 | UI operations observe rejected promises |
| BROWSER-A34 | UI operations surface asynchronous errors |
| BROWSER-A35 | country flag Unicode |
| BROWSER-A36 | country flag accessibility |
| BROWSER-A37 | progress starts |
| BROWSER-A38 | progress completes |
| BROWSER-A39 | masonry measures card height |
| BROWSER-A40 | masonry columns |
| BROWSER-A41 | masonry avoids overlaps |
| BROWSER-A42 | masonry measures added children |
| BROWSER-A43 | animated list updates |
| BROWSER-A44 | exit animation cleans up |
| BROWSER-A45 | chart creates SVG |
| BROWSER-A46 | chart updates |
| BROWSER-A47 | chart reuses instance |
| BROWSER-A48 | chart cleans up |
| BROWSER-A49 | sparkline renders line and area |
| BROWSER-A50 | error boundary catches |
| BROWSER-A51 | error boundary retries children |
| BROWSER-A52 | locale JSON |
| BROWSER-A53 | locale URL and cache busting |
| BROWSER-A54 | missing locale fails without retry |
| BROWSER-A55 | server failures allow retry |
| BROWSER-A56 | network failures allow retry |
| BROWSER-A57 | malformed translations fail without retry |
| BROWSER-A58 | scalar locale resource fails without retry |
| BROWSER-A59 | language cache and regional normalization |
