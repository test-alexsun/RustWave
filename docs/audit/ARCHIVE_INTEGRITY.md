# Archive integrity and original formatting FAIL

Pinned upstream: d709bad01dc0ceacb20012a3afdf528eddfd061f. Original Go files were not edited; gofmt -w was never executed.

## Cause and exact evidence

- Git system setting: `file:C:/Program Files/Git/etc/gitconfig core.autocrlf=true`.
- Initial command: `git archive --format=tar -o docs/benchmarks/raw/upstream.tar d709bad01dc0ceacb20012a3afdf528eddfd061f` (with only command-local safe.directory).
- `git show <SHA>:backend-go/cmd/server/main.go`: 5 LF, 0 CRLF. First tar member: 5 LF, 5 CRLF.
- `gofmt -l .`: exit 0, **173 paths** below. Formatting gate = **FAIL**, because required stdout is empty.
- `gofmt -d /src/backend-go/cmd/server/main.go`: exit 1, only CRLF→LF changes in its five lines. No change in tokens or indentation.
- Full first tar checked with Git blob SHA-1 formula `sha1("blob "+len+NUL+bytes)`: 1772 regular files, 1735 mismatches. This is a transport/checkout conversion defect, not evidence that upstream committed malformed formatting.
- Corrected command: `git -c core.autocrlf=false archive --format=tar -o docs/benchmarks/raw/upstream-lf.tar d709bad01dc0ceacb20012a3afdf528eddfd061f`.
- Corrected tar: **1772/1772 blob matches, 0 mismatches**. Extracted to a separate source-lf directory. Old source/archive/logs preserved. No in-place line-ending conversion or formatter fix was applied.
- First SQLite and PG suites failed TestInstallerMigratesExistingUnitAndKeepsBoundary because embedded Bash contained `pipefail\r`; installer shell syntax also failed. Frontend Biome/CSS declaration checks and contract text export were affected by CRLF. Those results are preserved as an invalid-input attempt and are not counted as pinned-reference results.
- Corrected LF gofmt results and all retest exit codes are in COMMANDS.md. Tests must use the LF copy even though git diff of Windows working tree was empty: Git clean conversion made that check insufficient for byte identity.

## Archive SHA-256

- upstream.tar: `9baffb76faca87fdc60cc650dfe48b4a5fe0bec689101a19554fb7bcbdcc6960`; matching 37/1772.
- upstream-lf.tar: `f31c9d722a1f97965e978445e4bf2c33c387dfe9fa07b17473a575d04699a82f`; matching 1772/1772.

## All 173 paths reported by original gofmt -l

Paths relative to backend-go.

```text
cmd/server/main.go
config/config.go
config/config_test.go
config/panel_path_test.go
internal/auth/challenges.go
internal/auth/handler.go
internal/auth/jwt.go
internal/auth/oauth.go
internal/auth/oauth_removed_test.go
internal/auth/passkeys.go
internal/auth/password.go
internal/auth/register_test.go
internal/auth/security_test.go
internal/cli/import_pasarguard.go
internal/cli/import_pasarguard_test.go
internal/cli/migrate_pg_to_sqlite.go
internal/cli/migrate_sqlite_to_pg.go
internal/cli/migrate_sqlite_to_pg_test.go
internal/cli/migrate_to_docker.go
internal/cli/migrate_to_docker_test.go
internal/cli/rescue.go
internal/configprofiles/bulk_hosts.go
internal/configprofiles/handler.go
internal/configprofiles/host_patch.go
internal/configprofiles/service.go
internal/configprofiles/service_test.go
internal/configprofiles/xray_sort.go
internal/configrender/plugins.go
internal/configrender/snippets.go
internal/contracts/commands.go
internal/contracts/registry.go
internal/contracts/registry_test.go
internal/cron/scheduler.go
internal/cron/scheduler_test.go
internal/database/database.go
internal/database/default_data.go
internal/database/default_subpage_config_data.go
internal/database/migrate.go
internal/database/migrations.go
internal/database/migrations_test.go
internal/database/models.go
internal/database/response_rule_headers_test.go
internal/database/schema_export_test.go
internal/httpx/color.go
internal/httpx/color_test.go
internal/httpx/httpx.go
internal/httpx/httpx_test.go
internal/infrabilling/handler.go
internal/jobs/queue.go
internal/jobs/queue_test.go
internal/keygen/keygen.go
internal/metrics/definitions.go
internal/metrics/registry.go
internal/metrics/registry_test.go
internal/middleware/auth.go
internal/middleware/auth_test.go
internal/middleware/cors.go
internal/middleware/logger.go
internal/middleware/status.go
internal/nodes/bulk.go
internal/nodes/client.go
internal/nodes/client_test.go
internal/nodes/commands.go
internal/nodes/compatibility_test.go
internal/nodes/config_rejection.go
internal/nodes/config_rejection_test.go
internal/nodes/events.go
internal/nodes/handler.go
internal/nodes/handler_test.go
internal/nodes/ips.go
internal/nodes/service.go
internal/nodes/sni.go
internal/nodes/start_config.go
internal/nodes/start_test.go
internal/nodes/torrent.go
internal/nodes/traffic_tracking.go
internal/nodes/traffic_tracking_test.go
internal/nodes/usage.go
internal/nodes/usage_test.go
internal/nodessh/terminal.go
internal/nodessh/tickets.go
internal/nodessh/vault.go
internal/nodessh/vault_test.go
internal/notify/notify.go
internal/notify/notify_test.go
internal/notify/templates.go
internal/prometheus/exporter.go
internal/prometheus/prometheus_test.go
internal/prometheus/rss.go
internal/prometheus/server.go
internal/responserules/headers.go
internal/responserules/headers_test.go
internal/server/dashboard.go
internal/server/dashboard_test.go
internal/server/mutation_probe_test.go
internal/server/notify_test.go
internal/server/parity_test.go
internal/server/probe_test.go
internal/server/response_rule_headers_test.go
internal/server/review_test.go
internal/server/server.go
internal/serviceunit/service.go
internal/serviceunit/service_test.go
internal/squads/handler.go
internal/squads/handler_test.go
internal/stubs/commands.go
internal/stubs/hwid.go
internal/stubs/integrations.go
internal/stubs/plugins.go
internal/stubs/shared_lists.go
internal/stubs/stubs.go
internal/stubs/system_tools.go
internal/stubs/torrent_blocker.go
internal/subscription/data.go
internal/subscription/diff_test.go
internal/subscription/encrypt.go
internal/subscription/express.go
internal/subscription/handler.go
internal/subscription/history.go
internal/subscription/history_test.go
internal/subscription/hwid.go
internal/subscription/protected.go
internal/subscription/review_test.go
internal/subscription/serve.go
internal/subscription/srr.go
internal/subscription/subscription_test.go
internal/subtemplates/handler.go
internal/subtpl/crypto.go
internal/subtpl/crypto_test.go
internal/subtpl/defaults_test.go
internal/subtpl/diff_test.go
internal/subtpl/export.go
internal/subtpl/fromobject.go
internal/subtpl/gen_links.go
internal/subtpl/gen_mihomo.go
internal/subtpl/gen_singbox.go
internal/subtpl/gen_xray_json.go
internal/subtpl/js/js.go
internal/subtpl/js/js_test.go
internal/subtpl/mapper.go
internal/subtpl/model.go
internal/subtpl/ojson/ojson.go
internal/subtpl/ojson/ojson_test.go
internal/subtpl/ojson/path.go
internal/subtpl/render.go
internal/subtpl/resolve.go
internal/subtpl/template.go
internal/subtpl/yaml.go
internal/subtpl/yaml_dump.go
internal/subtpl/yaml_dump_test.go
internal/system/channel.go
internal/system/handler.go
internal/system/host_memory.go
internal/system/nodes_metrics.go
internal/system/oauth_removed_test.go
internal/system/restore.go
internal/system/restore_test.go
internal/system/route_counter.go
internal/system/selfupdate.go
internal/system/selfupdate_test.go
internal/system/stats_test.go
internal/system/tools.go
internal/system/updates.go
internal/testdb/testdb.go
internal/tokens/handler.go
internal/tokens/scopes_data.go
internal/users/events.go
internal/users/handler.go
internal/users/lifecycle.go
internal/users/lifecycle_test.go
internal/users/service.go
internal/users/users_test.go
main.go
```
