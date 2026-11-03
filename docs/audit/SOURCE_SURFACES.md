# Source surface completeness ledger

Pinned upstream d709bad01dc0ceacb20012a3afdf528eddfd061f. These are source-discovered units, not parity test passes.

## Configuration environment keys

| Key | Source |
|---|---|
| APP_HOST | backend-go/config/config.go:84 |
| APP_PORT | backend-go/config/config.go:89 |
| APP_SECRET | backend-go/config/config.go:99 |
| BANDWIDTH_USAGE_NOTIFICATIONS_ENABLED | backend-go/config/config.go:226 |
| CONTAINER | backend-go/internal/system/updates.go:79 |
| DATABASE_URL | backend-go/config/config.go:102 |
| DATABASE_URL | backend-go/internal/cli/migrate_sqlite_to_pg.go:64 |
| DB_DRIVER | backend-go/config/config.go:101 |
| DB_MAX_CONNECTIONS | backend-go/config/config.go:246 |
| DOCKER | backend-go/internal/system/updates.go:79 |
| EXPIRATION_NOTIFICATIONS_ENABLED | backend-go/config/config.go:228 |
| EXPORT_TO_STREAM_ENABLED | backend-go/config/config.go:234 |
| FRONT_END_DOMAIN | backend-go/config/config.go:120 |
| GOWAVE_COMPOSE_DIR | backend-go/internal/system/updates.go:126 |
| GOWAVE_TEST_POSTGRES | backend-go/internal/testdb/testdb.go:27 |
| INSTANCE_ID | backend-go/internal/prometheus/exporter.go:284 |
| INSTANCE_TYPE | backend-go/internal/prometheus/exporter.go:288 |
| IN_DOCKER | backend-go/internal/cli/migrate_sqlite_to_pg.go:225 |
| IN_DOCKER | backend-go/internal/system/updates.go:79 |
| IS_HTTP_LOGGING_ENABLED | backend-go/config/config.go:155 |
| IS_TELEGRAM_NOTIFICATIONS_ENABLED | backend-go/config/config.go:199 |
| JWT_AUTH_LIFETIME | backend-go/config/config.go:136 |
| METRICS_ENABLED | backend-go/config/config.go:146 |
| METRICS_PASS | backend-go/config/config.go:157 |
| METRICS_PORT | backend-go/config/config.go:94 |
| METRICS_USER | backend-go/config/config.go:156 |
| NOTIFICATIONS_CONFIG_PATH | backend-go/internal/notify/notify.go:91 |
| NOT_CONNECTED_USERS_NOTIFICATIONS_ENABLED | backend-go/config/config.go:227 |
| PANEL_BASE_PATH | backend-go/config/config.go:152 |
| PANEL_DOMAIN | backend-go/config/config.go:125 |
| POSTGRES_DB | backend-go/internal/cli/migrate_sqlite_to_pg.go:79 |
| POSTGRES_DSN | backend-go/internal/cli/migrate_sqlite_to_pg.go:67 |
| POSTGRES_PASSWORD | backend-go/internal/cli/migrate_sqlite_to_pg.go:71 |
| POSTGRES_PORT | backend-go/internal/cli/migrate_sqlite_to_pg.go:83 |
| POSTGRES_USER | backend-go/internal/cli/migrate_sqlite_to_pg.go:75 |
| RUNTIME_DIRECTORY | backend-go/internal/system/updates.go:188 |
| SERVICE_CLEAN_USAGE_HISTORY | backend-go/config/config.go:231 |
| SERVICE_DISABLE_SRH_RECORDS | backend-go/config/config.go:233 |
| SERVICE_DISABLE_USER_USAGE_RECORDS | backend-go/config/config.go:232 |
| SHORT_UUID_LENGTH | backend-go/config/config.go:238 |
| SUB_PUBLIC_DOMAIN | backend-go/config/config.go:130 |
| TELEGRAM_BOT_API_ROOT | backend-go/config/config.go:201 |
| TELEGRAM_BOT_PROXY | backend-go/config/config.go:205 |
| TELEGRAM_BOT_TOKEN | backend-go/config/config.go:200 |
| USER_USAGE_IGNORE_BELOW_BYTES | backend-go/config/config.go:254 |
| WEBHOOK_ENABLED | backend-go/config/config.go:184 |
| WEBHOOK_SECRET_HEADER | backend-go/config/config.go:185 |
| WEBHOOK_URL | backend-go/config/config.go:187 |

## SQL table declaration inventory

| Engine | Tables in numbered SQL (plus gowave_migrations runner table) |
|---|---|
| sqlite | admin, api_tokens, auth_challenges, config_profile_inbounds, config_profile_inbounds_to_nodes, config_profile_snippets, config_profiles, entity_meta, external_squads, external_squads_templates, hosts, hosts_to_nodes, hwid_user_devices, infra_billing_history, infra_billing_nodes, infra_providers, integrations, internal_squad_host_links, internal_squad_inbounds, internal_squad_members, internal_squads, jobs, keygen, node_meta, node_plugin, nodes, nodes_usage_history, nodes_user_usage_history, passkeys, remnawave_settings, scheduled_executions, shared_lists, subscription_page_config, subscription_settings, subscription_templates, torrent_blocker_reports, user_meta, user_subscription_request_history, user_traffic, users |
| postgres | admin, api_tokens, auth_challenges, config_profile_inbounds, config_profile_inbounds_to_nodes, config_profile_snippets, config_profiles, entity_meta, external_squads, external_squads_templates, hosts, hosts_to_nodes, hwid_user_devices, infra_billing_history, infra_billing_nodes, infra_providers, integrations, internal_squad_host_links, internal_squad_inbounds, internal_squad_members, internal_squads, jobs, keygen, node_meta, node_plugin, nodes, nodes_usage_history, nodes_user_usage_history, passkeys, remnawave_settings, scheduled_executions, shared_lists, subscription_page_config, subscription_settings, subscription_templates, torrent_blocker_reports, user_meta, user_subscription_request_history, user_traffic, users |

SQLite-only table names: []; PG-only: []. Identical names do not prove identical types/constraints; inspect both SQL files and migration tests.

## Router registration closure

Literal Chi registrations found only in internal/server/server.go, internal/stubs/stubs.go and internal/system/tools.go. No production Route/Mount/Method/Handle registration was found by rg. 248 explicit method/path operations + 2 static wildcard registrations. Separate metrics switch handles GET /metrics and GET /health; CORS preflight is middleware. Chi route-walk test independently checks embedded command coverage but does not prove all response shapes.

## Source/tooling coverage

34 production Go directories including both entrypoints, config and testdb; 1122 function/method declarations. 40 schema models plus gowave_migrations. React source callsites include command factories, direct axios/instance calls, fetch and WebSocket. Frontend interface endpoint fields excluded. Installer, Dockerfiles/Compose, scripts, workflows, licenses and asset generation included in architecture/matrix. No Rust source created.
