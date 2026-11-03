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


## Readiness and controlled-clock investigation

| Identity | Expected trials | Executed | PASS | FAIL | SKIPPED | NOT_RUN |
| --- | --- | --- | --- | --- | --- | --- |
| Original unchanged | 3 | 3 | 3 | 0 | 0 | 0 |
| External changed-semantics | 12 | 12 | 12 | 0 | 0 | 0 |
| Initial daemon-unavailable attempt | 15 | 0 | 0 | 0 | 0 | 15 |

The first readiness01 attempt failed before starting any container: Docker Desktop Linux Engine named pipe absent. Seven Docker invocations failed to launch the planned 3 original + 12 external trials; classify all 15 trials NOT_RUN/environment BLOCKED, not failed assertions. Installed Docker Desktop was started; successful docker info preceded readiness02. No production/VPS use. Historical results, baseline and Go tests were not rerun.

Original smoke runs execute unmodified `bun run test:browser` and pinned tests/run-browser.mjs. Exercised environment: Linux amd64 Docker tool image, Bun1.4.2, Chromium156.0.8078.73, UTC/C.UTF-8, 2CPU/2000MiB, network none. Upstream documents Bun and local Chromium, not a minimum CPU/RAM SLA; these limits are the documented audit environment, not an invented upstream support guarantee. Three successes cannot erase historical flakiness or establish all-environment stability.

External matrix: normal2CPU/2000MiB, CPU-only1CPU/2000MiB, RAM-only2CPU/1400MiB, contention1CPU/1400MiB plus one CPU-loop process. Three fresh profiles each, same pinned source/dependencies/fixtures. Per-profile bundle builds once; reported trial duration excludes build. The original runner builds every invocation, so command durations are not directly comparable. Source remains read-only and 1772 blobs are reverified. No old evidence is overwritten.

### Root cause and evidence boundaries

1. **Upstream smoke synchronization defect: modal readiness.** browser-smoke.tsx:180–184 flushes a click, sleeps100ms, then requires `.jer-editor-container`. InboundCheckboxCard opens a Mantine modal. Locked Mantine Transition/use-transition schedules state changes through requestAnimationFrame (including a second frame) and timers; Transition returns null in exited state. A timer expiring is not proof these frame callbacks/React commits completed. Previous control run returned `dataset.result=failed` / “Inbound JSON viewer is missing” before the first assertion. The exact failing condition is DOM absence at the query. Which individual frame/commit was delayed in that historical run was not recorded; the state-machine race is established, not its precise scheduler trace. No evidence of a production JSON-viewer functional defect.

2. **Upstream smoke synchronization defect: clock readiness.** ClockFixture calls useTime(20). The hook registers setInterval in useEffect, then calls setNow(Date.now()); React must commit that update before the span changes. The smoke sleeps60ms and compares span text to firstTime. In two previous CPU-contention runs that comparison was false. Cgroup throttled periods increased59/59 and50/50 over their sample windows. The precise failed condition is no visible clock advance at assertion time; whether interval delivery, effect registration or commit was late cannot be distinguished from old assertion-only traces. Real-time scheduling is not a correctness barrier, and CPU quotas amplify this race. This supports an upstream **test harness** defect, not an established useTime production defect.

3. **External tool defects.** Prior V1 used a premature2-second CDP call timeout and produced five tool failures; retained separately. Later harness uses a single20-second deadline. New diagnostic runner attaches Runtime/Network/Page before navigation, logs each assert and resource counters. It changes navigation/observation timing and cannot be treated as an exact original-run replay. Browser missing CDP completion has several possible causes; the original20-second timeout remains **unresolved**, not attributed to the modal or clock without evidence.

4. **Environment.** CPU contention/throttling changes rendering/timer scheduling; previous corrected15 trials had no OOM or Network.loadingFailed. The unavailable Docker daemon was a separate startup blocker, corrected by starting Desktop. No browser or application test executed during that failed launch attempt.

### Separate external harness and semantic changes

browser_deterministic.mjs uses an in-memory Vite transform only on browser-smoke.tsx. Original files and production build behavior are unchanged. All original assertions remain intact and each successful run must record exactly59 PASS assertions. Modal wait is replaced with MutationObserver + requestAnimationFrame predicate readiness for the viewer and string-value element. The outer20-second smoke deadline remains; readiness failure remains a failure, not a skip.

Clock test temporarily fixes Date.now at100000, captures the20ms interval in an isolated browser context, waits for registration, and drives three20ms ticks through the real registered callback inside flushSync. It requires exactly one matching interval; ambiguous timer identity fails. It waits for committed DOM time advance, executes the unchanged assertion, then restores global clock/timer APIs. The registration/advance code fails on missing or ambiguous interval registration. Debug console probes are stripped by the pinned production build; no AUDIT_CLOCK console events were observed. Assertion progress is retained independently in window.__auditProgress and CDP snapshots. This observability limit is explicit; no clock console evidence is invented. This tests state propagation under controlled test time; **it does not test real timer delivery under contention**, and its PASS is not an original-smoke PASS. Other original waits/animations remain real-time; whole-suite mathematical determinism is not claimed.

Scope of resolution: two known readiness hazards are removed in this separate harness, subject to the observed matrix results. Scheduling, rendering and other legacy fixed waits can still vary. Bounded repeat success is evidence of observed reproducibility, not proof that all possible flakes are eliminated. No production CSPRNG, Go source, React source, fixtures, GATE_POLICY or20-second timeout was changed.

### Gate decision

**STAGE_01 PARTIAL; browser gate BLOCKED; historical FLAKY=FAIL.** New external results cannot close the original mandatory gate. Closing it without an exception requires an authorized upstream test-harness correction and original-gate revalidation; that changes the pinned test reference and is outside this audit-only change. The exact historical timeout cause remains unresolved. Stop at Stage01; no Stage02 work.

[CDP events, progress and counters](browser-readiness.json).




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

Candidate `RUSTWAVE-BROWSER-PATCH-V1`; patch SHA256 `0cae2b9c7a6800a6b1c9be9645d438a8beecbce62003f978b4ccbf333c4abf88`. Counts {"PASS": 20, "FAIL": 0, "SKIPPED": 0, "NOT_RUN": 0, "BLOCKED": 0, "FLAKY": 0}. All59 assertions and real native timer evidence preserved; original1772 blobs unchanged. Temporal wait semantics changed explicitly. STAGE_01 PARTIAL; browser gate BLOCKED pending explicit new-baseline acceptance. Historical FAIL/FLAKY remain, original20s timeout root cause unresolved. [Proposal, equivalence limits and preparation errors](BROWSER_PATCH_V1.md). No Stage02 work.
