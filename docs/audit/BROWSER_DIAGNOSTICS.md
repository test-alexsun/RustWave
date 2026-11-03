# Browser timeout investigation

Pinned source: d709bad01dc0ceacb20012a3afdf528eddfd061f. Historical logs examined without rerunning successful tests or editing React/Go sources.

| Check | Historical evidence | Finding |
|---|---|---|
| Browser executable/dependencies | browser-versions; tools image | Bun 1.4.2, Chromium 156.0.8078.73; executable present |
| Build readiness | run-browser.mjs awaits Vite build before spawning Chromium; error reached line 81 | Build finished sufficiently to launch browser; no build error recorded |
| Chromium startup | 10-second DevTools endpoint discovery precedes line 81 | Startup readiness passed; this was not Chromium startup timeout |
| Page target readiness | /json/list returned page target before line 81 | Browser page existed; application readiness is not proven by target existence |
| Navigation | file:// page argument, no Playwright navigation API or navigation-specific deadline | Reported error was not a navigation timeout; complete document load was not separately recorded |
| Test completion | Runtime.evaluate awaits document.body.dataset.result, deadline 20 seconds | No completion response arrived before deadline; cannot tell whether page JS stalled, failed before its catch handler, or CDP evaluation/connection stalled |
| CDP | No explicit “Chromium debugging connection failed” in stderr | No recorded onerror, but successful socket open/evaluate dispatch was not independently logged |
| Network errors | Harness does not enable CDP Network or browser console events | No historical network trace; absence of logged errors does not prove no errors |
| Browser stderr | Harness accumulates startup stderr in memory and does not emit it on the later completion timeout | Original Chromium stderr and console are unavailable in saved logs; temporary profile/output removed by upstream finally block |
| Test fetch behavior | browser-smoke.tsx:514–570 replaces fetch with synthetic success/404/503/offline/invalid JSON responses | Those intentional error cases are assertions, not proof of a real network failure |
| Retry | lf-browser-idle stdout “Browser smoke tests passed”, exit 0 | All smoke completion assertions passed with 2 CPUs/2000 MiB, network none, no concurrent compilation; first run used 1 CPU/1400 MiB during other work |

First LF attempt: FAIL, exit 1, total 111.077 s including Vite build; internal completion timeout 20 s. Retry: PASS, exit 0, total 79.697 s. These total durations are not the timeout thresholds. Both raw command records and SHA-256 log hashes are retained in [COMMANDS.md](COMMANDS.md). The initial CRLF harness attempt timed out separately at 1800 s and is not valid pinned-source evidence.

Root cause remains **BLOCKED / unresolved**. Changed resource conditions make contention plausible but do not prove it. A future diagnostic run should retain CDP Runtime exceptions/console, Network failures, document.readyState, dataset.result and per-assertion progress when the original deadline expires, in an external audit harness against an unmodified frontend. This diagnostic telemetry was **NOT_RUN** for the original attempt and cannot be reconstructed. No timeout relaxation, fixture removal or React change was applied. Stage remains PARTIAL.



## Execution gaps continuation

| Version | Profile | Trial | Result | Exit | Duration s | Assertions | Last result/error | Network failures |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| browser-gaps01 | control | 1 | PASS | 0 | 7.9 | 59 | Browser smoke tests passed | 0 |
| browser-gaps01 | control | 2 | FAIL | 1 | 3.266 | 0 | Error: Inbound JSON viewer is missing | 0 |
| browser-gaps01 | control | 3 | PASS | 0 | 6.696 | 59 | Browser smoke tests passed | 0 |
| browser-gaps01 | constrained | 1 | PASS | 0 | 7.695 | 59 | Browser smoke tests passed | 0 |
| browser-gaps01 | constrained | 2 | FAIL | 1 | 6.562 | 0 | Error: CDP call timeout: Runtime.evaluate | 0 |
| browser-gaps01 | constrained | 3 | FAIL | 1 | 6.367 | 0 | Error: CDP call timeout: Runtime.evaluate | 0 |
| browser-gaps01 | contention | 1 | FAIL | 1 | 7.43 | 0 | Error: CDP call timeout: Runtime.evaluate | 0 |
| browser-gaps01 | contention | 2 | FAIL | 1 | 7.027 | 0 | Error: CDP call timeout: Runtime.evaluate | 0 |
| browser-gaps01 | contention | 3 | FAIL | 1 | 7.48 | 0 | Error: CDP call timeout: Runtime.evaluate | 0 |
| browser-gaps02 | control | 1 | PASS | 0 | 6.645 | 59 | Browser smoke tests passed | 0 |
| browser-gaps02 | control | 2 | PASS | 0 | 8.409 | 59 | Browser smoke tests passed | 0 |
| browser-gaps02 | control | 3 | PASS | 0 | 9.719 | 59 | Browser smoke tests passed | 0 |
| browser-gaps02 | constrained | 1 | PASS | 0 | 9.458 | 59 | Browser smoke tests passed | 0 |
| browser-gaps02 | constrained | 2 | PASS | 0 | 12.227 | 59 | Browser smoke tests passed | 0 |
| browser-gaps02 | constrained | 3 | PASS | 0 | 10.395 | 59 | Browser smoke tests passed | 0 |
| browser-gaps02 | contention | 1 | FAIL | 1 | 13.5 | 21 | Error: session clock advances without render-time reads | 0 |
| browser-gaps02 | contention | 2 | FAIL | 1 | 9.631 | 21 | Error: session clock advances without render-time reads | 0 |
| browser-gaps02 | contention | 3 | PASS | 0 | 13.018 | 59 | Browser smoke tests passed | 0 |
| browser-gaps03 | cpu-only | 1 | PASS | 0 | 10.273 | 59 | Browser smoke tests passed | 0 |
| browser-gaps03 | cpu-only | 2 | PASS | 0 | 10.318 | 59 | Browser smoke tests passed | 0 |
| browser-gaps03 | cpu-only | 3 | PASS | 0 | 14.01 | 59 | Browser smoke tests passed | 0 |
| browser-gaps03 | ram-only | 1 | PASS | 0 | 6.017 | 59 | Browser smoke tests passed | 0 |
| browser-gaps03 | ram-only | 2 | PASS | 0 | 5.989 | 59 | Browser smoke tests passed | 0 |
| browser-gaps03 | ram-only | 3 | PASS | 0 | 9.175 | 59 | Browser smoke tests passed | 0 |


External harness: browser_diagnostic.mjs builds pinned Vite input and adds progress logging only to the in-memory assert transform. Source remains read-only; no assertion, wait(100), expected result or upstream timeout was changed. CDP Runtime/Network/Page events are enabled before file navigation from about:blank. This attach order and instrumentation differ from the historical runner; findings cannot retroactively prove its precise cause. Each profile uses three fresh Chromium profiles, UTC/C.UTF-8, network none, identical built bundle within that profile. Control 2 CPU/2000 MiB; constrained 1 CPU/1400 MiB; contention same constrained limits plus a Bun CPU loop. Every series builds once; build time is separate. An idle sample captures cgroup CPU usage/throttling, current/peak RAM and memory.events, not just Bun RSS. cgroup resources include the harness and CPU stressor. Console and exceptions are recorded even where the smoke deliberately exercises ErrorBoundary; expected test errors alone are not an unexpected failure.

V1 tooling limitation: independent CDP-call timer was 2 s and prematurely failed some busy Runtime.evaluate requests; these are **audit harness failures**, not proof of the original 20-s timeout. V1 raw results and original harness snapshot are retained. V2 uses the unchanged **single 20-s smoke deadline** for pending evaluations, captures URL/readyState/result/progress and resources, and saves Chromium stderr even on failure. Startup deadline remains 10 s. No increase beyond the original smoke deadline.

V1 control produced PASS/FAIL/PASS under identical resource limits; the failure returned dataset.result=failed and `Error: Inbound JSON viewer is missing` before the first assert. Source browser-smoke.tsx:180–184 clicks the modal, waits a fixed 100 ms, then requires .jer-editor-container. This is direct evidence of a readiness-sensitive flaky smoke condition. It is not proof that the historical timeout had the same cause. Resource-limited CDP timeouts and per-profile outcomes must be assessed with the table and counters; no statistically quantified CPU/RAM causality claim from n=3. V3 additionally isolates CPU-only (1 CPU/2000 MiB) and RAM-only (2 CPU/1400 MiB), three runs each, against V2 control. The contention comparison keeps the constrained limits constant. This is a small diagnostic sample, not a statistical causal estimate.

Historical first LF browser FAIL and retry PASS remain unchanged. **FLAKY / BLOCKED** remains for the strict browser gate. The precise cause of the original timeout is still unresolved because original console/network telemetry was unavailable. These supplementary diagnostic successes never override historical outcomes or promote the stage to PASS.

V2 control and constrained profiles each passed 3/3. V2 contention returned dataset.result=failed twice on session clock advances without render-time reads, and passed once. Source browser-smoke.tsx:350–356 relies on a real-time 60-ms wait. This is a reproduced readiness/timer failure under controlled CPU contention; it is distinct from the historical 20-s timeout.

Counters and per-assertion progress: [browser-experiments.json](browser-experiments.json).
