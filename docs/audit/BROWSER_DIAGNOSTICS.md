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
