# Frontend custom transports and UI map

Source `d709bad01dc0ceacb20012a3afdf528eddfd061f`. Companion to the generated callsite matrix. Paths below are relative to `frontend/src/`. This is source analysis; browser/API differential status is NOT_TESTED.

## Transports outside command factories

| Callsite | Method/path and request | Expected response / parser / UI effect |
|---|---|---|
| shared/_modals/hosts/create-host-drawer/create-host.modal.tsx | POST /api/hosts/preview, `{host:{remark,address,port,path,sni,fingerprint,securityLayer},userAgent,protocol:"vless"}` | `res.data.response?.previewContent || ""`, preview text; empty/default form values filled locally; inspect exact inline host object |
| shared/_modals/nodes/node-logs-modal/node-logs.modal.tsx | GET /api/nodes/{uuid}/logs, query type | `{response:{logs:string[]}}`; TypeScript generic only; log modal |
| shared/_modals/nodes/update-node-modal/update-node.modal.tsx (two GET calls) | GET /api/nodes/{uuid}/updates, repo aaaSaZaN/gowave-node or XTLS/Xray-core | `{response:{currentVersion:string,latestRelease?:Release,latestPrerelease?:Release,allReleases:Release[],architecture:string,os:string,currentCoreVersion:string,error?:string}}`; Release = tag_name/name/prerelease/published_at/assets[{name,browser_download_url,size}] |
| same file (three POST calls) | POST /api/nodes/{uuid}/updates/apply; `{type:'node',repo,version}`, `{type:'core',downloadUrl}`, or `{type:'core',repo,version}` | returns `res.data.response`; async apply UX; not Zod validated |
| shared/ui/sidebar/panel-update-check.ts | GET /api/system/updates/check, optional channel stable/dev | **Unwrapped** IPanelUpdateCheck: canAutoUpdate, hasUpdate, isDocker booleans; changelog/currentVersion/latestVersion strings; channel/targetChannel enum; updateCommand optional string |
| shared/ui/sidebar/build-info-modal.tsx | POST /api/system/updates/apply, `{channel}` | body ignored, success schedules page reload after 30 s; errors handled by mutation |
| shared/api/hooks/nodes/nodes.query.hooks.ts | GET /api/nodes/traffic-summary | local Zod `{response:{nodes:[{uuid:string,lifetimeTrafficBytes:number}]}}`; exact number precision required |
| shared/api/hooks/infra-billing/infra-billing.query.hooks.ts | GET /api/infra-billing/history, `{start:pageParam,size}`; defaults 0/100 | GetInfraBillingRecordsCommand.ResponseSchema; `.response.records.length` accumulated against `.total`; next page undefined when complete |
| shared/api/hooks/node-ssh/evaluate-vault.ts | POST EvaluateVaultCommand.TSQ_url, `{blinded}` | explicit ResponseSchema parse of unknown response; return evaluation to browser vault |
| shared/ui/connection-status-overlay/use-connection-probe.ts | GET health if token exists, otherwise auth/status; 5 s timeout | no schema validation; any HTTP response indicates connection recovered, even error status; network failure retries 1–30 s |
| shared/_modals/nodes/node-ssh-terminal/session/ssh-connection.ts | new WebSocket(options.url,[`rw`,ticket,token]); URL returned by ticket endpoint | binary terminal bytes and text control JSON; client supports identities/sign/hostkey replies, open/resize; server read limit 1 MiB, agent deadline 30 s; ticket expiry 15 s; must test handshake/origin/reuse/expiry separately |
| entities/dashboard/updates-store/use-updates-store.ts | two axios GETs to GitHub (repo and latest release) | stargazers_count and release tag_name; external dependency, not GoWave API |
| features/dashboard/config-profiles/monaco-setup/monaco-setup.feature.tsx | three axios GETs of jsonSchemaUrl | editor JSON schema; external/local asset based on resolved URL, no Bearer factory |
| app/i18n/plugins.ts | fetch locale path + build-id query | JSON translation resources; handles failed response |
| shared/_modals/universal/help-drawer/help-drawer.shared.tsx | fetch resolveDocsUrl(screen,language) | Markdown/text documentation |
| shared/ui/load-templates/use-download-template.tsx | fetch template.url | template content parsed downstream; external URL, not backend command |

All direct occurrences have source line numbers in [generated matrix](../FRONTEND_API_SHAPE_MATRIX.md). Remaining shared transports are factories in `shared/api/tsq-helpers`; those are mechanisms, not additional business callsites. Type/interface `endpoint: string` declarations are excluded. WebAssembly and editor runtime URLs are in `frontend/scripts/editor-assets.cjs` and lazy Monaco setup; they are static assets, not API operations.

## UI route → consumers

Router: `app/router/router.tsx`; literal route map: `shared/constants/routes.ts`; basename from PANEL_BASE_PATH. Intermediate group routes redirect to defaults.

| UI path | Consumer families / required scenarios |
|---|---|
| /auth/login | auth status, login/register/passkey/OAuth; initial setup, invalid credentials, loading, session loss |
| /oauth2/callback/:provider and /auth/oauth2/callback/:provider | OAuth state/code callback; success and error |
| /dashboard/home | health, system stats, bandwidth, recap; initial/empty/error |
| /dashboard/open/:entity/:id and /dashboard/tools/quick-open | entity resolution and entity modal opening; missing entity |
| /dashboard/management/users | users filters/list/stream/CRUD/bulk; metadata, HWID, subscription info/connection keys, usage/request history/torrent modals |
| /dashboard/management/hosts | hosts CRUD/preview/clone/reorder/bulk; profile/inbound/squad selectors |
| /dashboard/management/nodes | nodes CRUD/bulk/reorder/reset/restart, config profile selection, logs/update modal, SSH, integrations |
| /dashboard/management/stats/nodes | bandwidth statistics by node/user/squad |
| /dashboard/management/metrics/nodes | node metrics and system node statistics |
| /dashboard/management/config-profiles and /:uuid | profiles/inbounds/computed config, snippets; Monaco/Xray WASM; validation and empty profile |
| /dashboard/management/internal-squads and /external-squads | squads CRUD/order/tags/membership/access nodes/templates |
| /dashboard/management/subscription-settings | subscription settings schema and mutation; field validation |
| /dashboard/management/response-rules | shared subscription settings plus local header schemas; rule editing and matcher |
| /dashboard/management/settings | branding/auth/API tokens/scopes/passkeys/backend tools; permission and 401 states |
| /dashboard/management/plugins and /:uuid | plugins CRUD/sync/executor/tags, shared lists |
| /dashboard/tools/hwid-inspector | device list/stats/top-users, delete/create actions |
| /dashboard/tools/srh-inspector | subscription request history/statistics |
| /dashboard/tools/torrent-blocker-reports | torrent reports/stats/truncate |
| /dashboard/tools/sessions-explorer | connections/geocheck POST jobs and GET polling, drop |
| /dashboard/tools/http-stats | HTTP route statistics |
| /dashboard/templates/:type and /:uuid | subscription template list/edit/create/reorder/tags; output download |
| /dashboard/subpage and /:uuid | subscription-page configs CRUD/clone/reorder/tags |
| /dashboard/crm/infra-billing | providers, billed nodes and paginated payment history |
| global main layout / sidebar | metadata, panel update channel/check/apply, notifications, connection watchdog, help, locale |

Hook rows include direct symbol consumer paths. A hook with no direct consumer is retained as declared surface, not silently dropped; static symbol references cannot prove browser reachability. Subscription public-page deployment is a separate application; this React panel manages its configuration and links.

## Shape fidelity checklist for Stage 02

For each FE-ID compare declared RequestBody/Query/ParamSchema with actual serialized request, and ResponseSchema with router output. Preserve omitted vs null vs empty, date/number precision, nested objects/array order, enum case, pagination totals/cursors and error envelope. `createGetQueryHook` always GETs even if an imported command says otherwise; actual transport wins. Check requestMethod and schema overrides individually. Login/refresh/logout behavior must follow existing frontend; do not invent refresh endpoints. ResponseRules local schema in `shared/api/schemas/subscription-settings.schema.ts` extends contract behavior and must stay intact. Static browser smoke is not a full backend-connected UI test.

Local schema detail: responseModifications is optional, and its headers is optional. Headers accepts a record of header-name→string-value or the legacy `{key,value}[]`; legacy input is transformed using case-insensitive last-entry-wins keys while preserving the last key's spelling. SubscriptionSettings responseRules is nullable; UpdateSubscriptionSettings request responseRules is optional; TestSrrMatcher response matchedRule is nullable. These override the embedded OpenAPI expectations and are validated by scripts/tests/response-rule-headers.cjs. Do not collapse optional into nullable or remove the legacy transformation.
