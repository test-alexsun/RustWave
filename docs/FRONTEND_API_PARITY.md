# Frontend consumer parity status

Stage 01 source audit. Frontend 3.4.4 / React 19.3.1 / backend-contract 3.4.15 / Bun 1.4.2 verified in manifest/lockfile. [Callsites](FRONTEND_API_SHAPE_MATRIX.md), [shapes](audit/CONTRACT_SHAPES.md), [custom/UI map](audit/FRONTEND_CUSTOM.md).

| Scenario family | Go evidence scope | Rust / SQLite | Rust / PostgreSQL |
|---|---|---|---|
| Initial load, status, login/register/passkey/OAuth, session loss/logout | Existing probes/unit tests; see execution inventory | NOT_TESTED | NOT_TESTED |
| Users filters/list/CRUD/bulk, empty/error/validation | Probe/mutation subsets, no full browser traces | NOT_TESTED | NOT_TESTED |
| Nodes/profiles/inbounds/hosts/squads | Go package tests + probes | NOT_TESTED | NOT_TESTED |
| Settings/tokens/scopes/passkeys/response rules | Auth/probe tests and frontend local schemas | NOT_TESTED | NOT_TESTED |
| Subscriptions/templates/public UX/HWID/history | Golden render/HTTP fixtures; separate subscription-page app not run | NOT_TESTED | NOT_TESTED |
| Plugins/connections/torrent/integrations/SSH/billing | Mocked tests; real remote services NOT_RUN | NOT_TESTED | NOT_TESTED |
| Static/WASM/locale, loading/empty/error/layout | Static helper tests; browser smoke separately recorded | NOT_TESTED | NOT_TESTED |

Every FE-ID is a proposed future integration ID. Go schema references are not captured fixtures; Rust fixtures absent. Probe files remain ignored because they can contain synthetic credentials. Stage 02 must cover missing/null/empty, precision, timezone, enum, order/nesting, totals/cursors, errors/status/headers/cookies and side effects. Typecheck and browser smoke are separate checks; neither proves full backend parity. Never weaken frontend/Zod for Rust.

## Executed frontend smoke status

Corrected LF Biome, typecheck, 24 Bun tests and production build PASS. Chromium smoke first failed upstream 20-s timeout; idle retry passed using 2 CPUs and 2000 MiB, without React edits. Earlier failure is retained and its cause is unresolved. This does not execute authenticated UI/API flows or prove the 221 callsites compatible with Rust. [Complete evidence](TEST_INVENTORY.md).
