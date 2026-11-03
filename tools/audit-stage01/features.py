"""Human-reviewed capability groups plus every literal HTTP operation."""
from inventory import ROOT, DOC, OUT, read, write, table
import json
import re

groups = [
('BOOT','Startup, env validation, UTC, bind-before-workers, shutdown','server,config','config/config.go; internal/server/server.go','APP_HOST/PORT, APP_SECRET, signals','all migrations','Go/net/http,godotenv'),
('AUTH-PASSWORD','Password login, first-admin registration, HMAC+scrypt and legacy bcrypt, login audit events','auth','internal/auth/handler.go','login/register/status','admin,auth_challenges','jwt,bcrypt'),
('AUTH-OAUTH','GitHub, PocketID, Keycloak, generic OIDC, Telegram; nonce/state/PKCE','auth','internal/auth/oauth.go','authorize/callback','admin,auth_challenges,remnawave_settings','oauth2,oidc'),
('AUTH-PASSKEY','WebAuthn challenge issue/consume, credentials, counters','auth','internal/auth/passkeys.go','passkey routes','admin,passkeys,auth_challenges','go-webauthn'),
('AUTH-SCOPE','HS256 expiry, ADMIN/API lookup, token revocation, scope and AdminOnly policy','middleware,tokens,contracts','internal/middleware/auth.go; internal/tokens/handler.go; internal/contracts','Bearer and token CRUD','admin,api_tokens','jwt'),
('HTTP-CONTRACT','Envelopes, validation, errors, contract status, CORS, logger','httpx,middleware,contracts','internal/httpx; internal/middleware; internal/contracts','all routes, preflight','none directly','Chi,CORS'),
('USER-LIFECYCLE','User fields, credentials, traffic/status/expiry transitions, streaming and bulk transactions','users','internal/users','user CRUD and scheduled expiry','users,user_traffic,internal_squad_members,jobs','GORM,uuid'),
('NODE-RPC','mTLS node client, compatibility, request signing, start/config/stop/retire','nodes,keygen','internal/nodes/client.go; internal/nodes/service.go','node RPC and jobs','nodes,keygen,jobs','crypto/tls,HTTP'),
('NODE-HEALTH','Health loop, reconnect/start deduplication, hot statistics','nodes','internal/nodes','health ticks, startup sync','nodes,jobs','HTTP,timers'),
('NODE-USAGE','Traffic deltas, reset tracking, online status, per-user and per-node histories','nodes','internal/nodes','usage polling','nodes_usage_history,nodes_user_usage_history,user_traffic,nodes','GORM'),
('NODE-UPDATE','Node/Xray release lookup and apply RPC, logs','nodes','internal/nodes','node update/logs routes','nodes','GitHub,remote node'),
('PROFILE','Profile JSON, inbound extraction, reorder/tags, computed config','configprofiles,configrender','internal/configprofiles; internal/configrender','profiles/inbounds routes and sync','config_profiles,config_profile_inbounds,config_profile_inbounds_to_nodes,jobs','JSON,GORM'),
('HOST','Host override rendering, preview/clone, bulk mutation and sorting','configprofiles','internal/configprofiles','hosts routes','hosts,hosts_to_nodes,internal_squad_host_links','GORM'),
('SQUAD','Internal/external memberships, inbound/host/template overrides, bulk add/remove','squads','internal/squads','squad routes','internal_squads,internal_squad_members,internal_squad_inbounds,external_squads,external_squads_templates','GORM'),
('SUB-PUBLIC','Public subscription dispatch, user status, headers, client detection and info','subscription','internal/subscription','/api/sub/*','users,user_traffic,hosts,subscription_settings','HTTP,subtpl'),
('SUB-RULES','Response rule matching, header overrides, status/body behavior','subscription,responserules','internal/subscription; internal/responserules','subscription render / srr matcher','subscription_settings','regexp,JSON'),
('SUB-HWID','HWID limits, device create/delete/filter and user-agent handling','subscription,stubs','internal/subscription; internal/stubs/hwid.go','HWID routes and public requests','hwid_user_devices,users','GORM'),
('SUB-HISTORY','Buffered subscription history, inline test mode, flush on shutdown, disable flag','subscription','internal/subscription/history.go','public request event / history API','user_subscription_request_history','goroutines,GORM'),
('TPL-FORMATS','XRAY_BASE64, CLASH, MIHOMO, STASH, SINGBOX, XRAY_JSON output','subtpl','internal/subtpl/render.go; internal/subtpl/gen_*.go','render, client exports','stored templates/hosts/users via caller','YAML,base64'),
('TPL-COMPAT','JS coercion/number/date/object order/path semantics and YAML serialization','subtpl/js,subtpl/ojson,subtpl','internal/subtpl/js; internal/subtpl/ojson; internal/subtpl/yaml_dump.go','template evaluation','none','Go standard library,YAML'),
('TPL-CRYPTO','Client encryption/key derivation and protocol-specific links','subtpl,keygen','internal/subtpl/crypto.go; internal/subtpl/gen_links.go; internal/keygen','encrypted subscription / secret key','keygen','age,circl,x/crypto'),
('TPL-STORAGE','Template and subscription-page config CRUD/default seeding','subtemplates,database','internal/subtemplates; internal/database/default_data.go','template/subpage routes','subscription_templates,subscription_page_config','JSON,GORM'),
('PLUGIN','Plugin executor/sync/clone/reorder/tags and node integration associations','stubs,nodes','internal/stubs/plugins.go; internal/stubs/integrations.go','plugin/node-integration routes and jobs','node_plugin,integrations,jobs','node RPC'),
('PLUGIN-LISTS','Shared lists and snippets CRUD + propagation','stubs','internal/stubs/shared_lists.go; internal/stubs/stubs.go','shared-lists/snippets','shared_lists,config_profile_snippets,jobs','node RPC'),
('PLUGIN-TORRENT','Torrent blocker report collection, aggregation/truncation and notifications','stubs,nodes','internal/stubs/torrent_blocker.go; internal/nodes','torrent-collect','torrent_blocker_reports,jobs','node RPC'),
('CONNECTIONS','Async sessions by node/user, geocheck and drop, persisted job results','stubs,nodes,jobs','internal/stubs/commands.go; internal/nodes','connections endpoints / plugin-exec','jobs','node RPC'),
('METADATA','User/node metadata storage','stubs','internal/stubs/stubs.go','metadata GET/PUT','users,nodes','JSON,GORM'),
('SSH','Ristretto255 OPRF vault evaluation, encrypted browser vault, single-use tickets, SSH WS bridge','nodessh','internal/nodessh; ../frontend/src/entities/ssh-vault','node-ssh WS + ticket/vault','auth_challenges,keygen,nodes','x/crypto/ssh,websocket,circl'),
('BILLING','Providers, node billing and payment history, due notifications','infrabilling,cron','internal/infrabilling; internal/cron','infra-billing routes / crm/billing','infra_providers,infra_billing_nodes,infra_billing_history','GORM'),
('JOBS','Transactional outbox, target serialisation, leases, retries/backoff, PG SKIP LOCKED/advisory lock','jobs','internal/jobs/queue.go','enqueue/claim/process','jobs','GORM,timers'),
('JOB-KINDS','user-sync,node-start,node-stop,node-retire,torrent-collect,plugin-sync,plugin-exec,connections-drop,geocheck,notify delivery','server,notify','internal/server/server.go; internal/notify','registered worker kinds','jobs','node RPC,HTTP'),
('CRON-RESET','DAY/WEEK/MONTH/MONTH_ROLLING users reset and node reset','cron','internal/cron/scheduler.go','UTC calendar tasks','scheduled_executions,users,user_traffic,nodes,jobs','clock'),
('CRON-LIFECYCLE','Continuous expiry/traffic limits; caught-up persistent schedule; cleanup','cron','internal/cron/scheduler.go','15s tick, job/hour and usage/week cleanup','scheduled_executions,jobs,usage histories','clock'),
('NOTIFY','Webhook HMAC/secret, Telegram proxy/threads, retries and notification thresholds','notify,cron','internal/notify; internal/cron','service/user/node/torrent/CRM events','jobs,scheduled_executions','HTTP,Telegram'),
('METRICS','31 Prometheus families, separate BasicAuth listener, enabled/disabled','metrics,prometheus','internal/metrics; internal/prometheus','GET /metrics, GET /health','users,user_traffic,nodes,infra_providers','runtime,procfs'),
('SYSTEM-STATS','Host/process stats, HTTP counters, recap/bandwidth/node metrics','system','internal/system','system stats routes','users,nodes,usage histories','procfs,runtime'),
('TOOLS','One-time token to scoped cookie, queue retry/cancel, Swagger/Scalar and OpenAPI','system,tokens','internal/system/tools.go','/api/backend-tools/*','auth_challenges,admin,jobs','JWT,CDN docs UI'),
('DB-SQLITE','WAL, single connection, foreign keys, busy timeout, NORMAL synchronous','database','internal/database/database.go','database.Init','all tables','glebarez/modernc SQLite'),
('DB-POSTGRES','UTC, 20-connection default pool, imported foreign key types','database','internal/database/database.go; internal/database/migrations.go','database.Init','all tables','pgx,GORM postgres'),
('DB-MIGRATIONS','7 numbered migrations per engine, idempotent add-column, default seeding','database','internal/database/migrations; internal/database/migrate.go','AutoMigrate wrapper','gowave_migrations + all models','embedded SQL'),
('RESTORE','Tar.gz/sql.gz PostgreSQL COPY parse, staged SQLite validation, atomic replacement and sequence repair','system','internal/system/restore.go','POST /api/system/actions/restore','all tables','gzip,tar,GORM'),
('CLI-RESCUE','Interactive/noninteractive admin reset/list/create, enable password, print node secret','cli','internal/cli/rescue.go','rescue/cli aliases and flags','admin,remnawave_settings,keygen','terminal,stdin'),
('CLI-IMPORT','PasarGuard users, traffic and HWIDs from SQLite/PostgreSQL','cli','internal/cli/import_pasarguard.go','import pasarguard','users,user_traffic,hwid_user_devices','SQLite,PostgreSQL'),
('CLI-PG-SQLITE','Upstream PG to SQLite migration including type compatibility','cli','internal/cli/migrate_pg_to_sqlite.go','migrate pg-to-sqlite','all tables','both DB drivers'),
('CLI-SQLITE-PG','SQLite to PG transaction, schema/type and sequence checks','cli','internal/cli/migrate_sqlite_to_pg.go','migrate sqlite-to-pg','all tables','both DB drivers'),
('CLI-DOCKER','Preflight, copy validation, backup, generated compose/env/wrapper, service switch','cli','internal/cli/migrate_to_docker.go','migrate to-docker','all tables, files','Docker,systemd'),
('UPDATE','stable/dev release check, SHA256SUMS, root-owned binary/dir, update-request handoff','system,serviceunit','internal/system/selfupdate.go; internal/system/updates.go','update apply; API apply','files, /run/gowave','GitHub,tar,sha256,systemd'),
('SERVICE','Unprivileged gowave systemd service, root-owned code, sticky DB dir, path-triggered update','serviceunit','internal/serviceunit','service install','files /etc/systemd/system','bash,systemd'),
('INSTALL','Native SQLite or Docker PostgreSQL, bilingual prompts, Caddy/Nginx, channel/update/migration','install','../install.sh','installer flags and wizard','DB data, filesystem','curl,systemd,Docker,reverse proxy'),
('DOCKER','Multi-stage Bun/Go build, nonroot Alpine runtime; PG18 health ordering, loopback ports','docker','../Dockerfile; ../docker-compose.yml; ../docker-compose.build.yml','compose up/build','postgres volume; frontend files','Bun,Go,Alpine,PG18'),
('RELEASE','CI vet/race/dual DB/frontend/contract/docker; release amd64/arm64 artifacts/checksums','workflows','../.github/workflows','PR/workflow_call, main dev, v* releases','none','GitHub Actions,GHCR'),
('STATIC','Six roots, base-path rewrite, SPA/.html fallback, GET/HEAD, gzip-only WASM, manifest','server','internal/server/dashboard.go; internal/server/server.go','GET/HEAD /*','none','http.ServeContent,gzip'),
('FRONTEND','React auth/layout/router/query cache, Zod decoding, loading/empty/error handling','frontend','../frontend/src/app.tsx; ../frontend/src/app; ../frontend/src/shared/api','UI routes and transports','browser token/store','React,Mantine,TanStack,Axios,Zod'),
('EDITOR','Lazy Monaco/Xray WASM, JSON schema download, gzip assets; locales/help/templates','frontend','../frontend/scripts/editor-assets.cjs; ../frontend/src/features/dashboard/config-profiles','browser assets and validators','none','hash-pinned download,Monaco,WASM'),
('BACKUP-OPERATIONS','DB export/backup operational commands and migration backup; no dedicated backup HTTP route found','cli,install','../README.md; internal/cli/migrate_to_docker.go','operator pg_dump/file backup, restore API','all data','pg_dump,filesystem'),
('NODE-INSTALL','Separate privileged node migration installer; may stop Docker node','scripts','../scripts/migrate-node.sh','migrate-node.sh','separate node files','systemd,Docker,GitHub'),
]


def main():
    routes=json.loads(read(OUT/'routes.json'))
    symbol_rows=[]
    for p in (ROOT/'backend-go').rglob('*.go'):
        if p.name.endswith('_test.go'): continue
        s=read(p)
        for m in re.finditer(r'^func (?:\([^)]+\) )?(\w+)\(',s,re.M):
            symbol_rows.append((m[1], p.relative_to(ROOT).as_posix()+':'+str(s.count('\n',0,m.start())+1)))
    receiver={'authHandler':'auth','userHandler':'users','nodeHandler':'nodes','cpHandler':'configprofiles','sysHandler':'system','squadsHandler':'squads','subtemplatesHandler':'subtemplates','tokensHandler':'tokens','infrabillingHandler':'infrabilling','sshHandler':'nodessh','subHandler':'subscription','stubHandler':'stubs','s':'stubs','t':'system'}
    rows=[]
    for r in routes:
        rec,name=r['handler'].split('.',1)
        pkg=receiver[rec]
        files=[f for n,f in symbol_rows if n==name and '/'+pkg+'/' in f]
        related=[g[0] for g in groups if pkg in g[2].split(',')]
        rows.append([r['id'],r['method']+' '+r['path'],', '.join(files),', '.join(related),f'Package {pkg}: [DB/deps/tests](audit/GO_PACKAGES.md); group details below',pkg,'NOT_STARTED'])
    text='# Functional parity matrix\n\nSource `d709bad01dc0ceacb20012a3afdf528eddfd061f`. '
    text+=f'Inventory contains **{len(routes)+len(groups)} items = {len(routes)} HTTP/WS operations + {len(groups)} cross-cutting/non-HTTP capability groups**. Groups deliberately overlap endpoint implementations; this is a declared work-item denominator, not a count of independent algorithms or test assertions. '
    text+='Every Go production package and symbol is indexed in [packages](audit/GO_PACKAGES.md) and [symbols](audit/GO_SYMBOLS.md). All Rust modules below are proposed ownership labels only, no implementation exists. Compatibility proven: 0; global parity NOT_TESTED. Inventory completeness is source-discovery completeness, not 100% behavioral compatibility.\n\n'
    text+=table(['ID','HTTP/WS operation','Handler source','Capability IDs','DB / dependencies / existing tests','Proposed Rust module','Status'],rows)
    text+='\n## Capability groups and non-HTTP surfaces\n\nDB names are conceptual affected entities; exact names/types and associations are in [model map](audit/DATABASE_TABLES.md) and both SQL migration trees. Test evidence is package-level unless the test inventory names a dedicated scenario.\n\n'
    text+=table(['ID','Capability','Source (relative to backend-go)','API / CLI / event','DB / state','External dependencies','Existing tests / future Rust owner','Status'],[
        [g[0],g[1],g[3],g[4],g[5],g[6],f'[Test inventory](TEST_INVENTORY.md); {g[2]}','NOT_STARTED'] for g in groups])
    (DOC/'FUNCTIONAL_PARITY_MATRIX.md').write_text(text,encoding='utf-8')
    metrics=[]
    s=read(ROOT/'backend-go/internal/metrics/definitions.go')
    for m in re.finditer(r'(\w+)\s*= (gauge|counter)\("([^"]+)", "([^"]+)"\)',s):
        name=m[3]
        labels='node_uuid'
        if name.startswith('process_'): labels='instance_id, instance_name'
        elif name=='users_status': labels='status'
        elif name=='users_online_stats': labels='metricType'
        elif name=='users_total': labels='type'
        elif name=='node_basic_info': labels='node_uuid,node_name,node_country_emoji,provider_name,tags'
        elif name=='node_system_info': labels='node_uuid,arch,cpu_model,hostname,platform,release,version'
        elif '_inbound_' in name or '_outbound_' in name: labels='node_uuid,tag'
        metrics.append(['remnawave_'+name,m[2],m[4],labels+',app=remnawave'])
    write(OUT/'METRIC_FAMILIES.md','Prometheus families',f'{len(metrics)} families, exact HELP/TYPE and label keys from definitions.go + exporter.go. Units follow names/help; values require controlled event fixtures.', ['Name','TYPE','HELP','Labels'],metrics)
    counts=json.loads(read(OUT/'counts.json')); counts.update(capability_groups=len(groups),feature_items=len(groups)+len(routes),metric_families=len(metrics))
    (OUT/'counts.json').write_text(json.dumps(counts,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(counts))


if __name__=='__main__': main()
