# Test inventory and execution accounting

**Current continuation:** Original smoke 3/3 PASS in the latest bounded control run; separate readiness/controlled-clock test 12/12 PASS. Historical browser FLAKY remains FAIL for gate; exact original timeout cause unresolved. STAGE_01 PARTIAL. Latest details: “Readiness and controlled-clock investigation”.

Pinned source `d709bad01dc0ceacb20012a3afdf528eddfd061f`. Expected top-level Go test IDs: **128 per DB mode**, independently extracted before execution in [manifest](audit/go-test-manifest.json). Test package includes data-free unit tests too: DB mode indicates environment, not proof each test accesses that DB. `go test -json -count=1 -p=2 -race ./...` for SQLite; PostgreSQL without race as upstream CI, with GOWAVE_TEST_POSTGRES. Locale C.UTF-8, TZ UTC, Go 1.27.3 Linux amd64, resource-limited local Docker. Source and fixtures unmodified.

| Mode | Top-level PASS | FAIL | SKIPPED | NOT_RUN | Observed subtests | Subtest results | Fail-closed gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| sqlite | 124 | 0 | 4 | 0 | 133 | {"PASS": 130, "SKIPPED": 3} | BLOCKED |
| postgres | 125 | 0 | 3 | 0 | 133 | {"PASS": 133} | BLOCKED |

## Preserved first CRLF archive attempt (not pinned-reference evidence)

See [archive integrity](audit/ARCHIVE_INTEGRITY.md). These failures remain in the ledger; corrected LF results above supersede their input provenance, not erase them.

| Mode | PASS | FAIL | SKIPPED | NOT_RUN |
| --- | --- | --- | --- | --- |
| sqlite | 123 | 1 | 4 | 0 |
| postgres | 124 | 1 | 3 | 0 |

Top-level and child counts must not be added as independent scenarios. Runtime child IDs are retained in [execution ledger](audit/go-test-results.json); a parent PASS never hides a child SKIPPED. Dynamically generated subtest IDs are observed, not an independently complete future parity manifest. Package failures and malformed output also block PASS. The parser negative tests reject an explicit skip and a missing mandatory ID. No ignored/xfail/todo capability exists in the Go runner; missing terminal results are NOT_RUN.

| Expected ID | Source | SQLite | PostgreSQL |
| --- | --- | --- | --- |
| gowave/config/TestAppHostDefaultsToLoopback | backend-go/config/config_test.go:8 | PASS | PASS |
| gowave/config/TestIsLoopbackHost | backend-go/config/config_test.go:15 | PASS | PASS |
| gowave/config/TestDBMaxConnections | backend-go/config/config_test.go:31 | PASS | PASS |
| gowave/config/TestMetricsEnabled | backend-go/config/config_test.go:45 | PASS | PASS |
| gowave/config/TestPanelBasePath | backend-go/config/panel_path_test.go:5 | PASS | PASS |
| gowave/config/TestLoadPanelBasePath | backend-go/config/panel_path_test.go:19 | PASS | PASS |
| gowave/config/TestTelegramPlaceholderChatsAreUnset | backend-go/config/panel_path_test.go:31 | PASS | PASS |
| gowave/internal/auth/TestRemovedYandexCannotBeEnabledBySavedSettings | backend-go/internal/auth/oauth_removed_test.go:13 | PASS | PASS |
| gowave/internal/auth/TestRegisterConcurrentCreatesOneAdmin | backend-go/internal/auth/register_test.go:28 | PASS | PASS |
| gowave/internal/auth/TestRegisterRechecksAfterReadingBody | backend-go/internal/auth/register_test.go:74 | PASS | PASS |
| gowave/internal/auth/TestRegisterRejectsOversizedBody | backend-go/internal/auth/register_test.go:87 | PASS | PASS |
| gowave/internal/auth/TestPublicPasskeyBypassRejected | backend-go/internal/auth/security_test.go:43 | PASS | PASS |
| gowave/internal/auth/TestPasswordAuthenticationPolicy | backend-go/internal/auth/security_test.go:55 | PASS | PASS |
| gowave/internal/auth/TestFailedLoginEventOmitsPassword | backend-go/internal/auth/security_test.go:81 | PASS | PASS |
| gowave/internal/auth/TestChallengeExpiryAndConsumption | backend-go/internal/auth/security_test.go:118 | PASS | PASS |
| gowave/internal/auth/TestPasskeyRegistrationAndSignedLogin | backend-go/internal/auth/security_test.go:139 | PASS | PASS |
| gowave/internal/cli/TestParsePasarGuardDatabaseURL | backend-go/internal/cli/import_pasarguard_test.go:15 | PASS | PASS |
| gowave/internal/cli/TestPasarGuardEnvValue | backend-go/internal/cli/import_pasarguard_test.go:49 | PASS | PASS |
| gowave/internal/cli/TestDetectPasarGuardSourcePrefersEnvOverLeftoverSQLite | backend-go/internal/cli/import_pasarguard_test.go:68 | PASS | PASS |
| gowave/internal/cli/TestDetectPasarGuardSourceFallsBackToSQLiteFile | backend-go/internal/cli/import_pasarguard_test.go:89 | PASS | PASS |
| gowave/internal/cli/TestSQLiteReadOnlyURIOpensUnusualPaths | backend-go/internal/cli/import_pasarguard_test.go:115 | PASS | PASS |
| gowave/internal/cli/TestIsMigrationCommand | backend-go/internal/cli/migrate_sqlite_to_pg_test.go:20 | PASS | PASS |
| gowave/internal/cli/TestDetectMigrationPaths | backend-go/internal/cli/migrate_sqlite_to_pg_test.go:46 | PASS | PASS |
| gowave/internal/cli/TestDetectPostgresTargetDSNRequiresPassword | backend-go/internal/cli/migrate_sqlite_to_pg_test.go:76 | PASS | PASS |
| gowave/internal/cli/TestRedactDSN | backend-go/internal/cli/migrate_sqlite_to_pg_test.go:98 | PASS | PASS |
| gowave/internal/cli/TestMigrateSQLiteToPostgres_Integration | backend-go/internal/cli/migrate_sqlite_to_pg_test.go:114 | SKIPPED | PASS |
| gowave/internal/cli/TestCheckSQLiteForeignKeysNamesOrphans | backend-go/internal/cli/migrate_sqlite_to_pg_test.go:313 | PASS | PASS |
| gowave/internal/cli/TestDockerComposeTemplateMatchesRepository | backend-go/internal/cli/migrate_to_docker_test.go:12 | PASS | PASS |
| gowave/internal/cli/TestParseToDockerArgs | backend-go/internal/cli/migrate_to_docker_test.go:22 | PASS | PASS |
| gowave/internal/cli/TestResolveSourceSQLite | backend-go/internal/cli/migrate_to_docker_test.go:41 | PASS | PASS |
| gowave/internal/cli/TestBuildDockerEnvKeepsSecretsAndRendersLiterally | backend-go/internal/cli/migrate_to_docker_test.go:59 | PASS | PASS |
| gowave/internal/configprofiles/TestPatchHostCorrectsStoredModeAndRollsBackInvalidRelations | backend-go/internal/configprofiles/service_test.go:11 | PASS | PASS |
| gowave/internal/contracts/TestLookupReturnsAllMostSpecificMatches | backend-go/internal/contracts/registry_test.go:5 | PASS | PASS |
| gowave/internal/cron/TestScheduledJobRetentionPreservesActiveAndRecentJobs | backend-go/internal/cron/scheduler_test.go:19 | PASS | PASS |
| gowave/internal/cron/TestCalendarResetsAreBaselinedCaughtUpAndIdempotent | backend-go/internal/cron/scheduler_test.go:69 | PASS | PASS |
| gowave/internal/cron/TestRollingResetReplaysEveryMissedDay | backend-go/internal/cron/scheduler_test.go:100 | PASS | PASS |
| gowave/internal/cron/TestReviewUsersExpiresLimitsAndNotifies | backend-go/internal/cron/scheduler_test.go:117 | PASS | PASS |
| gowave/internal/database/TestMigrationsFreshAndExisting | backend-go/internal/database/migrations_test.go:9 | PASS | PASS |
| gowave/internal/database/TestFreshSchema | backend-go/internal/database/migrations_test.go:74 | PASS | PASS |
| gowave/internal/database/TestBrandingMigrationPreservesCustomTitles | backend-go/internal/database/migrations_test.go:89 | PASS | PASS |
| gowave/internal/database/TestResponseRuleHeadersUpgrade | backend-go/internal/database/response_rule_headers_test.go:12 | PASS | PASS |
| gowave/internal/database/TestExportSchema | backend-go/internal/database/schema_export_test.go:28 | SKIPPED | SKIPPED |
| gowave/internal/httpx/TestColorsMatchUpstream | backend-go/internal/httpx/color_test.go:6 | PASS | PASS |
| gowave/internal/httpx/TestClientIP | backend-go/internal/httpx/httpx_test.go:8 | PASS | PASS |
| gowave/internal/jobs/TestQueueRollbackRetryAndLease | backend-go/internal/jobs/queue_test.go:12 | PASS | PASS |
| gowave/internal/jobs/TestPerNodeSerialization | backend-go/internal/jobs/queue_test.go:64 | PASS | PASS |
| gowave/internal/jobs/TestPermanentErrorFailsWithoutRetry | backend-go/internal/jobs/queue_test.go:92 | PASS | PASS |
| gowave/internal/metrics/TestTextMatchesPromClient | backend-go/internal/metrics/registry_test.go:12 | PASS | PASS |
| gowave/internal/middleware/TestAuthorizationAndOtt | backend-go/internal/middleware/auth_test.go:16 | PASS | PASS |
| gowave/internal/nodes/TestCheckHealthExplainsForeignCertificate | backend-go/internal/nodes/client_test.go:24 | PASS | PASS |
| gowave/internal/nodes/TestOriginalNodeHashedSetCompatibility | backend-go/internal/nodes/compatibility_test.go:9 | PASS | PASS |
| gowave/internal/nodes/TestMetricsSnapshotsAreIsolated | backend-go/internal/nodes/compatibility_test.go:19 | PASS | PASS |
| gowave/internal/nodes/TestSummarizeXrayError | backend-go/internal/nodes/config_rejection_test.go:21 | PASS | PASS |
| gowave/internal/nodes/TestStartNodeKeepsServingNodeWhenNewConfigIsRejected | backend-go/internal/nodes/config_rejection_test.go:62 | PASS | PASS |
| gowave/internal/nodes/TestConfigErrorSurvivesHealthChecksUntilStartSucceeds | backend-go/internal/nodes/config_rejection_test.go:108 | PASS | PASS |
| gowave/internal/nodes/TestDisablingNodeClearsConfigError | backend-go/internal/nodes/config_rejection_test.go:134 | PASS | PASS |
| gowave/internal/nodes/TestGetNodesBatchesInboundsLikeSingleNode | backend-go/internal/nodes/handler_test.go:17 | PASS | PASS |
| gowave/internal/nodes/TestStartNodeClearsConnectingOnPreparationFailure | backend-go/internal/nodes/start_test.go:20 | PASS | PASS |
| gowave/internal/nodes/TestRepeatedHealthChecksDeduplicateStartJobs | backend-go/internal/nodes/start_test.go:79 | PASS | PASS |
| gowave/internal/nodes/TestTrafficPeriodStart | backend-go/internal/nodes/traffic_tracking_test.go:17 | PASS | PASS |
| gowave/internal/nodes/TestApplyTrackingStart | backend-go/internal/nodes/traffic_tracking_test.go:47 | PASS | PASS |
| gowave/internal/nodes/TestUpdateNodeTrafficTrackingStart | backend-go/internal/nodes/traffic_tracking_test.go:82 | PASS | PASS |
| gowave/internal/nodes/TestGetTrafficSummary | backend-go/internal/nodes/traffic_tracking_test.go:161 | PASS | PASS |
| gowave/internal/nodes/TestMultiplyConsumptionMatchesUpstream | backend-go/internal/nodes/usage_test.go:22 | PASS | PASS |
| gowave/internal/nodes/TestRecordUserUsageBillsHistoryAndFirstConnection | backend-go/internal/nodes/usage_test.go:32 | PASS | PASS |
| gowave/internal/nodes/TestStoreTorrentReportsPersistsAndNotifies | backend-go/internal/nodes/usage_test.go:87 | PASS | PASS |
| gowave/internal/nodessh/TestBrowserVaultCompatibility | backend-go/internal/nodessh/vault_test.go:12 | PASS | PASS |
| gowave/internal/notify/TestPrettyBytesMatchesUpstream | backend-go/internal/notify/notify_test.go:27 | PASS | PASS |
| gowave/internal/notify/TestWebhookDeliverySignsPayloadAndHonoursEventConfig | backend-go/internal/notify/notify_test.go:46 | PASS | PASS |
| gowave/internal/notify/TestTelegramTemplatesEscapeValues | backend-go/internal/notify/notify_test.go:103 | PASS | PASS |
| gowave/internal/notify/TestUnknownEventInConfigIsRejected | backend-go/internal/notify/notify_test.go:128 | PASS | PASS |
| gowave/internal/notify/TestTorrentReportLinksIntoDashboard | backend-go/internal/notify/notify_test.go:137 | PASS | PASS |
| gowave/internal/notify/TestTelegramRejectionsAreNotRetried | backend-go/internal/notify/notify_test.go:160 | PASS | PASS |
| gowave/internal/prometheus/TestMissingInterfaceRemovesOnlyNetworkMetrics | backend-go/internal/prometheus/prometheus_test.go:21 | PASS | PASS |
| gowave/internal/prometheus/TestExporterAndServer | backend-go/internal/prometheus/prometheus_test.go:53 | PASS | PASS |
| gowave/internal/responserules/TestHeadersCanonicalAndLegacy | backend-go/internal/responserules/headers_test.go:9 | PASS | PASS |
| gowave/internal/responserules/TestHeadersRejectInvalidShapes | backend-go/internal/responserules/headers_test.go:33 | PASS | PASS |
| gowave/internal/responserules/TestNormalizePreservesRuleData | backend-go/internal/responserules/headers_test.go:42 | PASS | PASS |
| gowave/internal/responserules/TestNormalizeUnchangedAndInvalidDocuments | backend-go/internal/responserules/headers_test.go:72 | PASS | PASS |
| gowave/internal/server/TestDashboardMount | backend-go/internal/server/dashboard_test.go:37 | PASS | PASS |
| gowave/internal/server/TestDashboardPrecompressedAssets | backend-go/internal/server/dashboard_test.go:107 | PASS | PASS |
| gowave/internal/server/TestDashboardPrefixPreservesAPI | backend-go/internal/server/dashboard_test.go:177 | PASS | PASS |
| gowave/internal/server/TestContractMutationProbe | backend-go/internal/server/mutation_probe_test.go:76 | PASS | PASS |
| gowave/internal/server/TestActionsEnqueueNotifications | backend-go/internal/server/notify_test.go:17 | PASS | PASS |
| gowave/internal/server/TestContractRouteCoverage | backend-go/internal/server/parity_test.go:63 | PASS | PASS |
| gowave/internal/server/TestContractResponseProbe | backend-go/internal/server/probe_test.go:171 | PASS | PASS |
| gowave/internal/server/TestResponseRuleHeadersSettingsAndDebugger | backend-go/internal/server/response_rule_headers_test.go:11 | PASS | PASS |
| gowave/internal/server/TestResponseRuleHeadersInvalidUpdateIsAtomic | backend-go/internal/server/response_rule_headers_test.go:49 | PASS | PASS |
| gowave/internal/server/TestMissingComputedProfileReturnsNotFound | backend-go/internal/server/review_test.go:9 | PASS | PASS |
| gowave/internal/serviceunit/TestInstallerMigratesExistingUnitAndKeepsBoundary | backend-go/internal/serviceunit/service_test.go:11 | PASS | PASS |
| gowave/internal/squads/TestExternalSquadRemovalPreservesOtherMemberships | backend-go/internal/squads/handler_test.go:16 | PASS | PASS |
| gowave/internal/subscription/TestHTTPMatchesUpstream | backend-go/internal/subscription/diff_test.go:233 | PASS | PASS |
| gowave/internal/subscription/TestHistoryWriterBatchesTrimsAndDrains | backend-go/internal/subscription/history_test.go:11 | PASS | PASS |
| gowave/internal/subscription/TestRawProtectedAnnounceOnlyForDeviceLimit | backend-go/internal/subscription/review_test.go:15 | PASS | PASS |
| gowave/internal/subscription/TestSocketDropThroughContractStatus | backend-go/internal/subscription/review_test.go:45 | PASS | PASS |
| gowave/internal/subscription/TestResponseRuleHeaderFormats | backend-go/internal/subscription/subscription_test.go:83 | PASS | PASS |
| gowave/internal/subscription/TestResponseRulesFollowUpstream | backend-go/internal/subscription/subscription_test.go:110 | PASS | PASS |
| gowave/internal/subscription/TestBaseSubscriptionHeadersAndBody | backend-go/internal/subscription/subscription_test.go:145 | PASS | PASS |
| gowave/internal/subscription/TestHiddenHostsReachXrayJSONInjector | backend-go/internal/subscription/subscription_test.go:195 | PASS | PASS |
| gowave/internal/subscription/TestHwidLimitIsAtomic | backend-go/internal/subscription/subscription_test.go:213 | PASS | PASS |
| gowave/internal/subscription/TestEncryptedResponse | backend-go/internal/subscription/subscription_test.go:262 | PASS | PASS |
| gowave/internal/subscription/TestBrowserAndInfo | backend-go/internal/subscription/subscription_test.go:286 | PASS | PASS |
| gowave/internal/subtpl/TestKeyDerivationMatchesUpstream | backend-go/internal/subtpl/crypto_test.go:11 | PASS | PASS |
| gowave/internal/subtpl/TestSeededTemplatesMatchUpstream | backend-go/internal/subtpl/defaults_test.go:15 | PASS | PASS |
| gowave/internal/subtpl/TestRenderMatchesUpstream | backend-go/internal/subtpl/diff_test.go:147 | PASS | PASS |
| gowave/internal/subtpl/js/TestMatchesNode | backend-go/internal/subtpl/js/js_test.go:13 | PASS | PASS |
| gowave/internal/subtpl/ojson/TestMatchesLodashAndJSONStringify | backend-go/internal/subtpl/ojson/ojson_test.go:11 | PASS | PASS |
| gowave/internal/subtpl/ojson/TestSpreadKeepsExistingPosition | backend-go/internal/subtpl/ojson/ojson_test.go:60 | PASS | PASS |
| gowave/internal/subtpl/TestDumpYAMLMatchesJsYaml | backend-go/internal/subtpl/yaml_dump_test.go:13 | PASS | PASS |
| gowave/internal/system/TestSettingsDiscardRemovedOAuthProvider | backend-go/internal/system/oauth_removed_test.go:13 | PASS | PASS |
| gowave/internal/system/TestRestoreRepairsSequencesWithMixedPrimaryKeys | backend-go/internal/system/restore_test.go:12 | PASS | PASS |
| gowave/internal/system/TestExtractTarGzKeepsEntriesInside | backend-go/internal/system/selfupdate_test.go:48 | PASS | PASS |
| gowave/internal/system/TestReleaseChecksums | backend-go/internal/system/selfupdate_test.go:79 | PASS | PASS |
| gowave/internal/system/TestRootOnlyWritableRejectsServiceAccountFiles | backend-go/internal/system/selfupdate_test.go:106 | SKIPPED | SKIPPED |
| gowave/internal/system/TestApplyUpdateRequestsRootHelper | backend-go/internal/system/selfupdate_test.go:122 | SKIPPED | SKIPPED |
| gowave/internal/system/TestReadRequestedChannelRejectsUntrustedRequests | backend-go/internal/system/selfupdate_test.go:167 | PASS | PASS |
| gowave/internal/system/TestInstallerCommandPassesChannelToScript | backend-go/internal/system/selfupdate_test.go:200 | PASS | PASS |
| gowave/internal/system/TestGetStatsCountsUsersByStatus | backend-go/internal/system/stats_test.go:18 | PASS | PASS |
| gowave/internal/system/TestReadProcMeminfo | backend-go/internal/system/stats_test.go:93 | PASS | PASS |
| gowave/internal/system/TestDockerUpdateCommandUsesComposeDir | backend-go/internal/system/stats_test.go:108 | PASS | PASS |
| gowave/internal/system/TestGetStatsConcurrentRequestsShareResult | backend-go/internal/system/stats_test.go:124 | PASS | PASS |
| gowave/internal/users/TestLifecycleRevokeAndTransactionalOutbox | backend-go/internal/users/lifecycle_test.go:16 | PASS | PASS |
| gowave/internal/users/TestUpdateLoadsOnceAndKeepsPreviousCredential | backend-go/internal/users/lifecycle_test.go:80 | PASS | PASS |
| gowave/internal/users/TestGetStreamTelegramIdFilter | backend-go/internal/users/users_test.go:30 | PASS | PASS |
| gowave/internal/users/TestActiveInternalSquads | backend-go/internal/users/users_test.go:70 | PASS | PASS |
| gowave/internal/users/TestBulkExtendExpirationDate | backend-go/internal/users/users_test.go:108 | PASS | PASS |
| gowave/internal/users/TestHandlersIntegration | backend-go/internal/users/users_test.go:141 | PASS | PASS |
| gowave/internal/users/TestBulkHandlersApply | backend-go/internal/users/users_test.go:187 | PASS | PASS |

## Every observed skip/failure

### sqlite

| ID | Status | Reason |
| --- | --- | --- |
| gowave/internal/cli/TestMigrateSQLiteToPostgres_Integration | SKIPPED | migrate_sqlite_to_pg_test.go:117: Skipping integration test: GOWAVE_TEST_POSTGRES is not set |
| gowave/internal/database/TestMigrationsFreshAndExisting/postgres | SKIPPED | migrations_test.go:16: GOWAVE_TEST_POSTGRES not set |
| gowave/internal/database/TestBrandingMigrationPreservesCustomTitles/postgres | SKIPPED | migrations_test.go:96: GOWAVE_TEST_POSTGRES not set |
| gowave/internal/database/TestResponseRuleHeadersUpgrade/postgres | SKIPPED | response_rule_headers_test.go:19: GOWAVE_TEST_POSTGRES not set |
| gowave/internal/database/TestExportSchema | SKIPPED | schema_export_test.go:30: explicit schema export only |
| gowave/internal/system/TestRootOnlyWritableRejectsServiceAccountFiles | SKIPPED | selfupdate_test.go:108: files created by root are trusted |
| gowave/internal/system/TestApplyUpdateRequestsRootHelper | SKIPPED | selfupdate_test.go:127: running inside a container |

Package failures: []; malformed JSON lines: [].
### postgres

| ID | Status | Reason |
| --- | --- | --- |
| gowave/internal/database/TestExportSchema | SKIPPED | schema_export_test.go:30: explicit schema export only |
| gowave/internal/system/TestRootOnlyWritableRejectsServiceAccountFiles | SKIPPED | selfupdate_test.go:108: files created by root are trusted |
| gowave/internal/system/TestApplyUpdateRequestsRootHelper | SKIPPED | selfupdate_test.go:127: running inside a container |

Package failures: []; malformed JSON lines: [].

## Fixtures and test scope

Eight committed fixture files are listed with sizes/hashes in [FIXTURES.md](audit/FIXTURES.md): subscription HTTP gzip, subscription render golden gzip/matrix, crypto, YAML, ordered JSON, JS semantics, Prometheus vectors. Inline fixtures live in *_test.go, including testdb migration/seeding, fake HTTP/TLS node servers, HTTP probes, restore COPY dumps, installer helpers. They are not missing merely because there is no standalone fixture file. Existing nodes tests use mocks, not a deployed GoWave node. Source root tests require POSIX tools; Windows-host Go compilation is not the reference execution environment.

All Go test sources and packages are indexed in [GO_PACKAGES.md](audit/GO_PACKAGES.md). Default testdb SQLite has one in-memory connection and migrations/seeds; GOWAVE_TEST_POSTGRES switches testdb.Open to unique PG schemas. Some tests directly instantiate SQLite despite PG mode, so dual environment execution is not automatically dual DB coverage for every assertion. Database migration tests explicitly iterate engines and skip PG without DSN. CLI SQLite→PG integration needs DSN. No live external node is required by the default suite; separate real RPC/SSH/OAuth/provider integrations remain future NOT_TESTED.

Conditional skips in source: TestExportSchema requires GOWAVE_EXPORT_SCHEMA=1; its regeneration is deliberately not enabled because source fixtures must not change. RootOnlyWritable rejects service-owned files but skips root. ApplyUpdateRequestsRootHelper skips container environment. RepeatedHealthChecksDeduplicateStartJobs skips if real time crosses a minute: this is a determinism defect for future strict gates, not an acceptable blanket exemption. Exact observed skips above take precedence over this static list.

Contract route coverage enumerates Chi routes against 218 command definitions. Probe/mutation tests capture seeded handler responses with GOWAVE_PROBE_OUT; scripts/validate-contract.cjs validates these against locked Zod schemas. This is Go self/contract testing, not Go↔Rust differential compatibility. It does not execute every UI state or every negative input.

Frontend unit source files: entities/ssh-vault/encoding.test.ts; shared/lib/dependencies.test.ts, hardening.test.ts, virtual-layout.test.ts. Browser smoke: tests/run-browser.mjs + browser-smoke.tsx; uses Chromium and browser layout/crypto/locale assertions, not a complete authenticated backend flow. Scripts/tests/installer.sh exercises installer behavior with controlled stubs; real systemd/Docker migration is not run on host. scripts/tests/response-rule-headers.cjs validates header extension schemas. Branding/export/validator checks are separate command IDs below.

## Execution commands

Commands/exit codes/durations are recorded in [COMMANDS.md](audit/COMMANDS.md). Raw logs, exported probes, compiler cache and binaries stay in ignored docs/benchmarks/raw; only non-secret status/IDs/checksums are committed. Reproduce with Python tools/audit-stage01/inventory.py, run.py (Docker permissions), features.py, results.py; start from the git archive specified in the stage report. The benchmark is a separate script and must run without simultaneous compilation.

Fixture regeneration against original Remnawave/Node 24.21.0 is NOT_RUN; native installer execution, live provider/node/SSH sessions, full UI network traces and future Rust/architecture matrix are NOT_RUN/NOT_TESTED, explicitly outside Go unit evidence. Native updater test skips remain a Stage 01 execution gap, not a PASS.

## Frontend unit manifest / actual IDs

{'PASS': 24}; expected 24 source-defined names. Results from corrected lf-frontend-test; no assumed passes from build.

| ID | Source | Test name | Result |
| --- | --- | --- | --- |
| BUN-001 | frontend/src/entities/ssh-vault/encoding.test.ts | vault blobs retain padded standard Base64 and authenticated decryption | PASS |
| BUN-002 | frontend/src/entities/ssh-vault/encoding.test.ts | X25519 generator interoperates with native WebCrypto key import | PASS |
| BUN-003 | frontend/src/shared/lib/dependencies.test.ts | class names preserve conditional, nested, numeric and object values | PASS |
| BUN-004 | frontend/src/shared/lib/dependencies.test.ts | base64 matches RFC vectors, binary data and large UTF-8 templates | PASS |
| BUN-005 | frontend/src/shared/lib/dependencies.test.ts | base64 rejects malformed vault data and mixed alphabets | PASS |
| BUN-006 | frontend/src/shared/lib/dependencies.test.ts | query keys retain parameter values and invalidation prefixes | PASS |
| BUN-007 | frontend/src/shared/lib/dependencies.test.ts | table paths support literal dotted keys, arrays and missing properties | PASS |
| BUN-008 | frontend/src/shared/lib/dependencies.test.ts | table sorting is stable, case insensitive and keeps missing values last | PASS |
| BUN-009 | frontend/src/shared/lib/dependencies.test.ts | version checks follow SemVer prerelease precedence and ignore build metadata | PASS |
| BUN-010 | frontend/src/shared/lib/dependencies.test.ts | byte formatting retains IEC, SI, bit rate and zero behavior | PASS |
| BUN-011 | frontend/src/shared/lib/dependencies.test.ts | favicon resolver normalizes web hosts and rejects invalid addresses | PASS |
| BUN-012 | frontend/src/shared/lib/dependencies.test.ts | colors remain deterministic valid CSS hex values | PASS |
| BUN-013 | frontend/src/shared/lib/dependencies.test.ts | sparkline geometry handles empty, single, constant and invalid values | PASS |
| BUN-014 | frontend/src/shared/lib/dependencies.test.ts | assertion helper narrows truthy values and throws meaningful errors | PASS |
| BUN-015 | frontend/src/shared/lib/hardening.test.ts | optional React props omit undefined and retain meaningful falsy values | PASS |
| BUN-016 | frontend/src/shared/lib/hardening.test.ts | reordering preserves input and ignores missing array positions | PASS |
| BUN-017 | frontend/src/shared/lib/hardening.test.ts | editor row identity follows moves, immutable edits, insertions and deletions | PASS |
| BUN-018 | frontend/src/shared/lib/hardening.test.ts | required values preserve falsy data and reject missing values | PASS |
| BUN-019 | frontend/src/shared/lib/hardening.test.ts | JSON fields accept objects, arrays and text and reject unexpected scalar values | PASS |
| BUN-020 | frontend/src/shared/lib/hardening.test.ts | form errors validate unknown payloads and preserve nested field paths | PASS |
| BUN-021 | frontend/src/shared/lib/virtual-layout.test.ts | virtual rows cover the viewport with bounded overscan | PASS |
| BUN-022 | frontend/src/shared/lib/virtual-layout.test.ts | virtual row sizes follow keys through filtering and reordering | PASS |
| BUN-023 | frontend/src/shared/lib/virtual-layout.test.ts | virtual layout handles empty lists, hidden viewports, boundaries and shrinking data | PASS |
| BUN-024 | frontend/src/shared/lib/virtual-layout.test.ts | node version metadata supports contract versions and optional GoWave flags | PASS |

## Supplemental nonroot test

{'PASS': 1}. Run as UID/GID 10001 in isolated Docker; covers source root-dependent skip without removing that skip from full-run statistics. Native updater still needs a non-container Linux environment.

## Final consolidated ledger

| Scope | EXPECTED | EXECUTED | PASS | FAIL | SKIPPED | NOT_RUN | BLOCKED |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GO-sqlite | 128 | 124 | 124 | 0 | 4 | 0 | 4 |
| GO-postgres | 128 | 125 | 125 | 0 | 3 | 0 | 3 |
| BUN-unit | 24 | 24 | 24 | 0 | 0 | 0 | 0 |
| GO-nonroot-supplement | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| BROWSER-LF-attempts | 2 | 2 | 1 | 1 | 0 | 0 | 1 |
| BUILDX-history-logs-optional | 1 | 0 | 0 | 0 | 0 | 1 | 0 |
| COMMAND-checks | 14 | 14 | 14 | 0 | 0 | 0 | 0 |
| BASELINE-trials | 6 | 6 | 6 | 0 | 0 | 0 | 0 |

EXECUTED means a terminal PASS or FAIL; skipped IDs were selected by the runner but their bodies did not complete. BLOCKED overlaps terminal counts and denotes unresolved gate inputs; it is not an additional test outcome. Browser latest execution PASS still has an unresolved earlier timeout. Do not sum parents with child assertions or command/build/trial checks. Go child assertions: SQLite 133 observed, 130 PASS / 3 SKIPPED; PostgreSQL 133 observed, 133 PASS. Child IDs are retained but not independently exhaustive. All 128 source-defined top-level IDs per mode received a terminal runner event; NOT_RUN=0 there. No ignored/xfail/todo results were observed. Parser negative checks reject missing/skip IDs.

Browser attempts on LF source: first **FAIL**, exit 1 / 111.077 s, upstream internal 20-s timeout at tests/run-browser.mjs:81, 1 CPU/1400 MiB during other audit work; retry **PASS**, exit 0 / 79.697 s, 2 CPU/2000 MiB, no concurrent compilation, network none. Both use Bun 1.4.2 and Chromium 156.0.8078.73. React files and timeout unchanged. Resource conditions differ, so the first failure cannot be assigned to an upstream defect or dismissed as resolved nondeterminism. The earlier CRLF browser attempt also hit the harness 1800-s timeout; it is separate invalid-input evidence. This is layout/crypto/locale smoke, not authenticated UI↔API end-to-end testing.

Buildx history logs request was **NOT_RUN**: auto-review did not allow execution when the preceding session exhausted usage. No shell/encoding workaround was used. It is an optional diagnostic, not an unresolved image-build result: saved lf-image-build stderr records completed export/unpack, command exit 0 (525.387 s), and lf-image-inspect exit 0 independently confirms image sha256:61040df30cfedd64c79cc478a811bffe952db7b7ca14319fcf1c33ae3f94b176, 125660444 bytes. Build provenance warning about missing Git metadata is retained; pinned source blobs and COMMIT_SHA build argument supply separate provenance.


| Class | Result / exact reason | Disposition |
|---|---|---|
| Upstream tests / nondeterminism | A minute-boundary branch can skip RepeatedHealthChecksDeduplicateStartJobs; not observed in these runs. Schema exporter deliberately requires GOWAVE_EXPORT_SCHEMA=1 and writes migration source files. | No proven upstream gofmt or Go assertion defect in blob-identical runs. Clock and generator policy need explicit future fixtures. |
| Test environment | TestRootOnlyWritableRejectsServiceAccountFiles skips root in each suite; TestApplyUpdateRequestsRootHelper skips Docker in each suite. | Nonroot supplemental test PASS; original 2 skips remain. Native updater remains BLOCKED pending isolated non-container Linux execution; production/VPS not touched. |
| Test configuration | SQLite suite skips TestMigrateSQLiteToPostgres_Integration and 3 PG child migration tests because GOWAVE_TEST_POSTGRES is absent. TestExportSchema skips in both modes because export flag is absent. | PG mode covers the DSN-dependent cases. Export fixture regeneration NOT_RUN to preserve original fixtures. No skip removed from denominator. |
| Unresolved browser failure | First LF run reached Chromium but did not receive completion within upstream 20 s; idle 2-CPU retry passed. | Both outcomes retained. Cause not proven; strict no-flaky gate remains open. |
| Audit input error | Windows Git core.autocrlf=true converted 1735/1772 archive members; gofmt listed 173 paths despite exit 0. Bash failed on pipefail\r; frontend check/typecheck/contract text comparison failed. | FAIL retained in first-attempt ledger. Separate LF archive and all 1772 blob hashes verified; corrected checks PASS. No original Go/React edits or gofmt -w. |
| Audit dependencies | First branding invocation lacked git; original browser harness timed out. | Git/Chromium tool image supplies dependencies; branding PASS; browser outcomes above. |
| Audit baseline script | First baseline exited 1 with IndexError on empty port bindings. Diagnostic second attempt exited 1 deliberately: backend was running but internal Docker network returned empty 3000/3001 bindings. No measurements existed. | Fixed only audit harness: probe sidecar inside internal network, no host ports. Six measured trials completed. Both failed attempts recorded, never backend failures. |
| Tool access | Buildx history logs denied execution during previous session usage limit. | NOT_RUN optional diagnostic; saved completed build and inspect evidence suffice. No bypass. |
| Mandatory current gate gaps | Original skips and unresolved first browser timeout. | STAGE_01 PARTIAL; strict PASS and automatic Stage 02 transition prohibited. |
| Future gates, not executed | Real systemd install/update/rollback, live external node/provider/SSH flows, full authenticated UI traces, full static/metrics differential matrix, Rust/architecture parity, original Remnawave fixture regeneration. | NOT_RUN/NOT_TESTED; no complete compatibility claim. Existing Go mocks/goldens and installer stubs are not those checks. |

Browser readiness/network/navigation investigation: [diagnostics](audit/BROWSER_DIAGNOSTICS.md). Historical browser console/network telemetry is unavailable; original timeout remains unresolved.



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

Schema exporter output differs from the initial migration baseline; its test validates generation, not fixture equality. [Hashes and source-only diff](audit/SCHEMA_EXPORT_EVIDENCE.md). Pinned fixtures remain unchanged.


## Readiness and controlled-clock investigation

| Identity | Expected trials | Executed | PASS | FAIL | SKIPPED | NOT_RUN |
| --- | --- | --- | --- | --- | --- | --- |
| Original unchanged | 3 | 3 | 3 | 0 | 0 | 0 |
| External changed-semantics | 12 | 12 | 12 | 0 | 0 | 0 |
| Initial daemon-unavailable attempt | 15 | 0 | 0 | 0 | 0 | 15 |

The first readiness01 attempt failed before starting any container: Docker Desktop Linux Engine named pipe absent. Seven Docker invocations failed to launch the planned 3 original + 12 external trials; classify all 15 trials NOT_RUN/environment BLOCKED, not failed assertions. Installed Docker Desktop was started; successful docker info preceded readiness02. No production/VPS use. Historical results, baseline and Go tests were not rerun.

Original smoke runs execute unmodified `bun run test:browser` and pinned tests/run-browser.mjs. Exercised environment: Linux amd64 Docker tool image, Bun1.4.2, Chromium156.0.8078.73, UTC/C.UTF-8, 2CPU/2000MiB, network none. Upstream documents Bun and local Chromium, not a minimum CPU/RAM SLA; these limits are the documented audit environment, not an invented upstream support guarantee. Three successes cannot erase historical flakiness or establish all-environment stability.

External matrix: normal2CPU/2000MiB, CPU-only1CPU/2000MiB, RAM-only2CPU/1400MiB, contention1CPU/1400MiB plus one CPU-loop process. Three fresh profiles each, same pinned source/dependencies/fixtures. Per-profile bundle builds once; reported trial duration excludes build. The original runner builds every invocation, so command durations are not directly comparable. Source remains read-only and 1772 blobs are reverified. No old evidence is overwritten.

Modal100ms and clock60ms waits are upstream smoke readiness races. A separate DOM/controlled-clock harness preserves assertions but changes wait semantics; it is not replacement evidence for the original smoke. Historical20s timeout root cause remains unresolved. STAGE_01 PARTIAL, browser gate BLOCKED, Stage02 NOT READY. Full analysis and limits: [browser diagnostics](audit/BROWSER_DIAGNOSTICS.md). Reproduce only into a new evidence directory with tools/audit-stage01/readiness_run.py; do not rerun baseline/Go/native/inventory. Starting delivery commit d694945c8bfde9d44b720c0ee0c807ea1db91ead.
