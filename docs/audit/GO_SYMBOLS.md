# Go production symbol index

Source: `d709bad01dc0ceacb20012a3afdf528eddfd061f`.

Discovery aid, not a business-feature count. Includes every production Go function/method declaration.

| Package | Function | Receiver | Source |
| --- | --- | --- | --- |
| cmd/server | main |  | backend-go/cmd/server/main.go:5 |
| config | Load |  | backend-go/config/config.go:81 |
| config | envBool |  | backend-go/config/config.go:163 |
| config | envList | c *Config | backend-go/config/config.go:169 |
| config | loadOptional | c *Config | backend-go/config/config.go:182 |
| config | IsLoopbackHost | c *Config | backend-go/config/config.go:265 |
| config | NormalizePanelBasePath |  | backend-go/config/config.go:276 |
| config | Validate | c *Config | backend-go/config/config.go:295 |
| internal/auth | ConsumeChallenge |  | backend-go/internal/auth/challenges.go:12 |
| internal/auth | NewHandler |  | backend-go/internal/auth/handler.go:24 |
| internal/auth | GetStatus | h *Handler | backend-go/internal/auth/handler.go:76 |
| internal/auth | Register | h *Handler | backend-go/internal/auth/handler.go:161 |
| internal/auth | loginAttempt |  | backend-go/internal/auth/handler.go:247 |
| internal/auth | Login | h *Handler | backend-go/internal/auth/handler.go:261 |
| internal/auth | GenerateToken |  | backend-go/internal/auth/jwt.go:11 |
| internal/auth | NewOAuthHandler |  | backend-go/internal/auth/oauth.go:29 |
| internal/auth | oauthRandom |  | backend-go/internal/auth/oauth.go:52 |
| internal/auth | configuration | h *OAuthHandler | backend-go/internal/auth/oauth.go:59 |
| internal/auth | Authorize | h *OAuthHandler | backend-go/internal/auth/oauth.go:115 |
| internal/auth | Callback | h *OAuthHandler | backend-go/internal/auth/oauth.go:143 |
| internal/auth | fetchIdentity | h *OAuthHandler | backend-go/internal/auth/oauth.go:296 |
| internal/auth | NewPasskeyHandler |  | backend-go/internal/auth/passkeys.go:25 |
| internal/auth | WebAuthnID | u passkeyUser | backend-go/internal/auth/passkeys.go:34 |
| internal/auth | WebAuthnName | u passkeyUser | backend-go/internal/auth/passkeys.go:35 |
| internal/auth | WebAuthnDisplayName | u passkeyUser | backend-go/internal/auth/passkeys.go:36 |
| internal/auth | WebAuthnCredentials | u passkeyUser | backend-go/internal/auth/passkeys.go:37 |
| internal/auth | configured | h *PasskeyHandler | backend-go/internal/auth/passkeys.go:39 |
| internal/auth | loadUser | h *PasskeyHandler | backend-go/internal/auth/passkeys.go:58 |
| internal/auth | storeSession | h *PasskeyHandler | backend-go/internal/auth/passkeys.go:97 |
| internal/auth | passkeyJSON |  | backend-go/internal/auth/passkeys.go:105 |
| internal/auth | RegistrationOptions | h *PasskeyHandler | backend-go/internal/auth/passkeys.go:110 |
| internal/auth | AuthenticationOptions | h *PasskeyHandler | backend-go/internal/auth/passkeys.go:134 |
| internal/auth | passkeyResponse |  | backend-go/internal/auth/passkeys.go:153 |
| internal/auth | session | h *PasskeyHandler | backend-go/internal/auth/passkeys.go:166 |
| internal/auth | VerifyRegistration | h *PasskeyHandler | backend-go/internal/auth/passkeys.go:182 |
| internal/auth | VerifyAuthentication | h *PasskeyHandler | backend-go/internal/auth/passkeys.go:234 |
| internal/auth | HashPassword |  | backend-go/internal/auth/password.go:16 |
| internal/auth | VerifyPassword |  | backend-go/internal/auth/password.go:35 |
| internal/cli | DetectPasarGuardSource |  | backend-go/internal/cli/import_pasarguard.go:82 |
| internal/cli | detectPasarGuardSourceIn |  | backend-go/internal/cli/import_pasarguard.go:95 |
| internal/cli | pasarGuardEnvValue |  | backend-go/internal/cli/import_pasarguard.go:137 |
| internal/cli | parsePasarGuardDatabaseURL |  | backend-go/internal/cli/import_pasarguard.go:161 |
| internal/cli | sqliteReadOnlyURI |  | backend-go/internal/cli/import_pasarguard.go:212 |
| internal/cli | ImportFromPasarGuard |  | backend-go/internal/cli/import_pasarguard.go:219 |
| internal/cli | ImportPasarGuardInteractive |  | backend-go/internal/cli/import_pasarguard.go:405 |
| internal/cli | DetectUpstreamPostgresDSN |  | backend-go/internal/cli/migrate_pg_to_sqlite.go:50 |
| internal/cli | isUpstreamEnvPath |  | backend-go/internal/cli/migrate_pg_to_sqlite.go:126 |
| internal/cli | MigratePostgresToSQLite |  | backend-go/internal/cli/migrate_pg_to_sqlite.go:137 |
| internal/cli | listPostgresTables |  | backend-go/internal/cli/migrate_pg_to_sqlite.go:269 |
| internal/cli | migratePostgresTable |  | backend-go/internal/cli/migrate_pg_to_sqlite.go:285 |
| internal/cli | ensureSQLiteTableColumns |  | backend-go/internal/cli/migrate_pg_to_sqlite.go:376 |
| internal/cli | sqliteTypeForPostgres |  | backend-go/internal/cli/migrate_pg_to_sqlite.go:411 |
| internal/cli | quoteIdentifier |  | backend-go/internal/cli/migrate_pg_to_sqlite.go:434 |
| internal/cli | closeGormDB |  | backend-go/internal/cli/migrate_pg_to_sqlite.go:438 |
| internal/cli | MigratePGToSQLiteInteractive |  | backend-go/internal/cli/migrate_pg_to_sqlite.go:449 |
| internal/cli | DetectGoWaveSQLitePath |  | backend-go/internal/cli/migrate_sqlite_to_pg.go:35 |
| internal/cli | DetectPostgresTargetDSN |  | backend-go/internal/cli/migrate_sqlite_to_pg.go:60 |
| internal/cli | redactDSN |  | backend-go/internal/cli/migrate_sqlite_to_pg.go:101 |
| internal/cli | MigrateSQLiteToPostgres |  | backend-go/internal/cli/migrate_sqlite_to_pg.go:113 |
| internal/cli | checkSQLiteForeignKeys |  | backend-go/internal/cli/migrate_sqlite_to_pg.go:232 |
| internal/cli | postgresTargetData |  | backend-go/internal/cli/migrate_sqlite_to_pg.go:262 |
| internal/cli | listSQLiteTables |  | backend-go/internal/cli/migrate_sqlite_to_pg.go:276 |
| internal/cli | listPostgresCurrentTables |  | backend-go/internal/cli/migrate_sqlite_to_pg.go:285 |
| internal/cli | postgresForeignKeyOrder |  | backend-go/internal/cli/migrate_sqlite_to_pg.go:297 |
| internal/cli | migrateTableSQLiteToPG |  | backend-go/internal/cli/migrate_sqlite_to_pg.go:355 |
| internal/cli | resetPostgresSequences |  | backend-go/internal/cli/migrate_sqlite_to_pg.go:511 |
| internal/cli | parseToDockerArgs |  | backend-go/internal/cli/migrate_to_docker.go:66 |
| internal/cli | RunMigrateToDocker |  | backend-go/internal/cli/migrate_to_docker.go:98 |
| internal/cli | prepareToDocker |  | backend-go/internal/cli/migrate_to_docker.go:119 |
| internal/cli | checkSQLiteFileForeignKeys |  | backend-go/internal/cli/migrate_to_docker.go:214 |
| internal/cli | resolveSourceSQLite |  | backend-go/internal/cli/migrate_to_docker.go:223 |
| internal/cli | buildDockerEnv |  | backend-go/internal/cli/migrate_to_docker.go:245 |
| internal/cli | renderDockerEnv |  | backend-go/internal/cli/migrate_to_docker.go:265 |
| internal/cli | printToDockerPlan |  | backend-go/internal/cli/migrate_to_docker.go:288 |
| internal/cli | executeToDocker |  | backend-go/internal/cli/migrate_to_docker.go:313 |
| internal/cli | installCLIWrapper |  | backend-go/internal/cli/migrate_to_docker.go:425 |
| internal/cli | runDockerCompose |  | backend-go/internal/cli/migrate_to_docker.go:439 |
| internal/cli | runVerbose |  | backend-go/internal/cli/migrate_to_docker.go:455 |
| internal/cli | checkPanelHealth |  | backend-go/internal/cli/migrate_to_docker.go:462 |
| internal/cli | portFree |  | backend-go/internal/cli/migrate_to_docker.go:484 |
| internal/cli | waitPortFree |  | backend-go/internal/cli/migrate_to_docker.go:493 |
| internal/cli | freeLoopbackPort |  | backend-go/internal/cli/migrate_to_docker.go:504 |
| internal/cli | randomHex |  | backend-go/internal/cli/migrate_to_docker.go:514 |
| internal/cli | IsMigrationCommand |  | backend-go/internal/cli/rescue.go:19 |
| internal/cli | IsPostgresToSQLiteMigrationCommand |  | backend-go/internal/cli/rescue.go:37 |
| internal/cli | migrationDestination |  | backend-go/internal/cli/rescue.go:41 |
| internal/cli | runToDocker |  | backend-go/internal/cli/rescue.go:48 |
| internal/cli | runSQLiteToPG |  | backend-go/internal/cli/rescue.go:56 |
| internal/cli | RunRescue |  | backend-go/internal/cli/rescue.go:95 |
| internal/cli | PrintNodeSecretKey |  | backend-go/internal/cli/rescue.go:192 |
| internal/cli | printUsage |  | backend-go/internal/cli/rescue.go:202 |
| internal/cli | interactiveMenu |  | backend-go/internal/cli/rescue.go:231 |
| internal/cli | ResetSuperadmin |  | backend-go/internal/cli/rescue.go:285 |
| internal/cli | ListAdmins |  | backend-go/internal/cli/rescue.go:295 |
| internal/cli | EnablePasswordAuth |  | backend-go/internal/cli/rescue.go:311 |
| internal/cli | resetAdminPasswordInteractive |  | backend-go/internal/cli/rescue.go:322 |
| internal/cli | createAdminInteractive |  | backend-go/internal/cli/rescue.go:364 |
| internal/configprofiles | BulkDeleteHosts | h *Handler | backend-go/internal/configprofiles/bulk_hosts.go:10 |
| internal/configprofiles | BulkDisableHosts | h *Handler | backend-go/internal/configprofiles/bulk_hosts.go:23 |
| internal/configprofiles | BulkEnableHosts | h *Handler | backend-go/internal/configprofiles/bulk_hosts.go:34 |
| internal/configprofiles | BulkUpdateHosts | h *Handler | backend-go/internal/configprofiles/bulk_hosts.go:45 |
| internal/configprofiles | NewHandler |  | backend-go/internal/configprofiles/handler.go:22 |
| internal/configprofiles | formatInbound |  | backend-go/internal/configprofiles/handler.go:56 |
| internal/configprofiles | formatInbounds | h *Handler | backend-go/internal/configprofiles/handler.go:79 |
| internal/configprofiles | formatProfile | h *Handler | backend-go/internal/configprofiles/handler.go:102 |
| internal/configprofiles | GetConfigProfilesTags | h *Handler | backend-go/internal/configprofiles/handler.go:148 |
| internal/configprofiles | SetConfigProfilesTags | h *Handler | backend-go/internal/configprofiles/handler.go:168 |
| internal/configprofiles | GetProfiles | h *Handler | backend-go/internal/configprofiles/handler.go:198 |
| internal/configprofiles | CreateConfigProfile | h *Handler | backend-go/internal/configprofiles/handler.go:220 |
| internal/configprofiles | GetConfigProfile | h *Handler | backend-go/internal/configprofiles/handler.go:258 |
| internal/configprofiles | UpdateConfigProfile | h *Handler | backend-go/internal/configprofiles/handler.go:274 |
| internal/configprofiles | DeleteConfigProfile | h *Handler | backend-go/internal/configprofiles/handler.go:316 |
| internal/configprofiles | ReorderConfigProfiles | h *Handler | backend-go/internal/configprofiles/handler.go:322 |
| internal/configprofiles | GetProfileInbounds | h *Handler | backend-go/internal/configprofiles/handler.go:351 |
| internal/configprofiles | GetAllInbounds | h *Handler | backend-go/internal/configprofiles/handler.go:370 |
| internal/configprofiles | GetComputedConfig | h *Handler | backend-go/internal/configprofiles/handler.go:388 |
| internal/configprofiles | GetHostsTags | h *Handler | backend-go/internal/configprofiles/handler.go:411 |
| internal/configprofiles | nullableString |  | backend-go/internal/configprofiles/handler.go:420 |
| internal/configprofiles | nullableStringPtr |  | backend-go/internal/configprofiles/handler.go:427 |
| internal/configprofiles | nullableAlpn |  | backend-go/internal/configprofiles/handler.go:434 |
| internal/configprofiles | nullableMihomoIpVersion |  | backend-go/internal/configprofiles/handler.go:443 |
| internal/configprofiles | formatHostResponse |  | backend-go/internal/configprofiles/handler.go:452 |
| internal/configprofiles | GetHosts | h *Handler | backend-go/internal/configprofiles/handler.go:567 |
| internal/configprofiles | CreateHost | h *Handler | backend-go/internal/configprofiles/handler.go:590 |
| internal/configprofiles | GetHost | h *Handler | backend-go/internal/configprofiles/handler.go:616 |
| internal/configprofiles | UpdateHost | h *Handler | backend-go/internal/configprofiles/handler.go:633 |
| internal/configprofiles | DeleteHost | h *Handler | backend-go/internal/configprofiles/handler.go:667 |
| internal/configprofiles | CloneHost | h *Handler | backend-go/internal/configprofiles/handler.go:676 |
| internal/configprofiles | ReorderHosts | h *Handler | backend-go/internal/configprofiles/handler.go:706 |
| internal/configprofiles | BulkHostsAction | h *Handler | backend-go/internal/configprofiles/handler.go:729 |
| internal/configprofiles | Preview | h *Handler | backend-go/internal/configprofiles/handler.go:788 |
| internal/configprofiles | patchHost |  | backend-go/internal/configprofiles/host_patch.go:15 |
| internal/configprofiles | NewService |  | backend-go/internal/configprofiles/service.go:25 |
| internal/configprofiles | SetSyncer | s *Service | backend-go/internal/configprofiles/service.go:33 |
| internal/configprofiles | DB | s *Service | backend-go/internal/configprofiles/service.go:37 |
| internal/configprofiles | CreateHostFromInput | s *Service | backend-go/internal/configprofiles/service.go:97 |
| internal/configprofiles | replaceHostRelations |  | backend-go/internal/configprofiles/service.go:261 |
| internal/configprofiles | CreateHost | s *Service | backend-go/internal/configprofiles/service.go:307 |
| internal/configprofiles | GetAllHosts | s *Service | backend-go/internal/configprofiles/service.go:323 |
| internal/configprofiles | GetHostByUUID | s *Service | backend-go/internal/configprofiles/service.go:329 |
| internal/configprofiles | InternalSquadInboundLinks | s *Service | backend-go/internal/configprofiles/service.go:338 |
| internal/configprofiles | PatchHost | s *Service | backend-go/internal/configprofiles/service.go:347 |
| internal/configprofiles | CloneHost | s *Service | backend-go/internal/configprofiles/service.go:357 |
| internal/configprofiles | UpdateHost | s *Service | backend-go/internal/configprofiles/service.go:383 |
| internal/configprofiles | DeleteHost | s *Service | backend-go/internal/configprofiles/service.go:392 |
| internal/configprofiles | GetAllProfiles | s *Service | backend-go/internal/configprofiles/service.go:404 |
| internal/configprofiles | GetProfileByUUID | s *Service | backend-go/internal/configprofiles/service.go:410 |
| internal/configprofiles | CreateProfile | s *Service | backend-go/internal/configprofiles/service.go:419 |
| internal/configprofiles | UpdateProfile | s *Service | backend-go/internal/configprofiles/service.go:458 |
| internal/configprofiles | DeleteProfile | s *Service | backend-go/internal/configprofiles/service.go:505 |
| internal/configprofiles | syncInbounds |  | backend-go/internal/configprofiles/service.go:514 |
| internal/configprofiles | GetInboundsByProfileUUID | s *Service | backend-go/internal/configprofiles/service.go:632 |
| internal/configprofiles | GetAllInbounds | s *Service | backend-go/internal/configprofiles/service.go:638 |
| internal/configprofiles | SetProfileTags | s *Service | backend-go/internal/configprofiles/service.go:644 |
| internal/configprofiles | GenerateHostPreview | s *Service | backend-go/internal/configprofiles/service.go:662 |
| internal/configprofiles | parseOrderedValue |  | backend-go/internal/configprofiles/xray_sort.go:67 |
| internal/configprofiles | reorderKeys |  | backend-go/internal/configprofiles/xray_sort.go:115 |
| internal/configprofiles | sortInboundObject |  | backend-go/internal/configprofiles/xray_sort.go:135 |
| internal/configprofiles | SortXrayConfig |  | backend-go/internal/configprofiles/xray_sort.go:146 |
| internal/configprofiles | SortInboundConfig |  | backend-go/internal/configprofiles/xray_sort.go:185 |
| internal/configprofiles | encodeOrderedValue |  | backend-go/internal/configprofiles/xray_sort.go:212 |
| internal/configrender | Plugin |  | backend-go/internal/configrender/plugins.go:10 |
| internal/configrender | Expand |  | backend-go/internal/configrender/snippets.go:12 |
| internal/contracts | loadCommands |  | backend-go/internal/contracts/commands.go:40 |
| internal/contracts | FindCommand |  | backend-go/internal/contracts/commands.go:64 |
| internal/contracts | loadEndpoints |  | backend-go/internal/contracts/registry.go:24 |
| internal/contracts | Lookup |  | backend-go/internal/contracts/registry.go:44 |
| internal/contracts | AdminOnly |  | backend-go/internal/contracts/registry.go:78 |
| internal/contracts | Allows |  | backend-go/internal/contracts/registry.go:87 |
| internal/contracts | ValidScope |  | backend-go/internal/contracts/registry.go:98 |
| internal/cron | SetNodeFormatter | s *Scheduler | backend-go/internal/cron/scheduler.go:39 |
| internal/cron | New |  | backend-go/internal/cron/scheduler.go:41 |
| internal/cron | SetSyncer | s *Scheduler | backend-go/internal/cron/scheduler.go:49 |
| internal/cron | SetConfig | s *Scheduler | backend-go/internal/cron/scheduler.go:52 |
| internal/cron | Start | s *Scheduler | backend-go/internal/cron/scheduler.go:54 |
| internal/cron | daily |  | backend-go/internal/cron/scheduler.go:83 |
| internal/cron | weekly |  | backend-go/internal/cron/scheduler.go:95 |
| internal/cron | monthly |  | backend-go/internal/cron/scheduler.go:107 |
| internal/cron | every |  | backend-go/internal/cron/scheduler.go:119 |
| internal/cron | tasks | s *Scheduler | backend-go/internal/cron/scheduler.go:124 |
| internal/cron | Tick | s *Scheduler | backend-go/internal/cron/scheduler.go:150 |
| internal/cron | runCalendar | s *Scheduler | backend-go/internal/cron/scheduler.go:175 |
| internal/cron | reviewUsers | s *Scheduler | backend-go/internal/cron/scheduler.go:221 |
| internal/cron | thresholdNotifications | s *Scheduler | backend-go/internal/cron/scheduler.go:246 |
| internal/cron | expirationNotifications | s *Scheduler | backend-go/internal/cron/scheduler.go:284 |
| internal/cron | notConnectedNotifications | s *Scheduler | backend-go/internal/cron/scheduler.go:301 |
| internal/cron | resetStrategy | s *Scheduler | backend-go/internal/cron/scheduler.go:320 |
| internal/cron | resetRolling | s *Scheduler | backend-go/internal/cron/scheduler.go:332 |
| internal/cron | resetNodes | s *Scheduler | backend-go/internal/cron/scheduler.go:351 |
| internal/cron | reviewNodes | s *Scheduler | backend-go/internal/cron/scheduler.go:377 |
| internal/cron | basicNodeData |  | backend-go/internal/cron/scheduler.go:403 |
| internal/cron | billingNotifications | s *Scheduler | backend-go/internal/cron/scheduler.go:429 |
| internal/cron | cleanUsage | s *Scheduler | backend-go/internal/cron/scheduler.go:464 |
| internal/database | Init |  | backend-go/internal/database/database.go:13 |
| internal/database | SetMaxConnections |  | backend-go/internal/database/database.go:69 |
| internal/database | SeedDefaults |  | backend-go/internal/database/default_data.go:194 |
| internal/database | EnsureSubscriptionSetting |  | backend-go/internal/database/default_data.go:272 |
| internal/database | AutoMigrate |  | backend-go/internal/database/migrate.go:15 |
| internal/database | MigrateSchema |  | backend-go/internal/database/migrate.go:26 |
| internal/database | schemaModels |  | backend-go/internal/database/migrate.go:33 |
| internal/database | ImportedZeroValue |  | backend-go/internal/database/migrate.go:83 |
| internal/database | buildImportedZeroValues |  | backend-go/internal/database/migrate.go:89 |
| internal/database | migrateLegacyHostRelations |  | backend-go/internal/database/migrate.go:132 |
| internal/database | legacyHostColumnExpr |  | backend-go/internal/database/migrate.go:248 |
| internal/database | legacyString |  | backend-go/internal/database/migrate.go:255 |
| internal/database | decodeLegacyUUIDList |  | backend-go/internal/database/migrate.go:268 |
| internal/database | applyMigrations |  | backend-go/internal/database/migrations.go:21 |
| internal/database | migrateResponseRuleHeaders |  | backend-go/internal/database/migrations.go:93 |
| internal/database | SchemaTableOrder |  | backend-go/internal/database/migrations.go:119 |
| internal/database | matchImportedForeignKeyTypes |  | backend-go/internal/database/migrations.go:131 |
| internal/database | Value | a StringArray | backend-go/internal/database/models.go:13 |
| internal/database | Scan | a *StringArray | backend-go/internal/database/models.go:26 |
| internal/database | TableName | Admin | backend-go/internal/database/models.go:107 |
| internal/database | TableName | User | backend-go/internal/database/models.go:140 |
| internal/database | TableName | UserTraffic | backend-go/internal/database/models.go:154 |
| internal/database | TableName | Node | backend-go/internal/database/models.go:195 |
| internal/database | TableName | Integration | backend-go/internal/database/models.go:208 |
| internal/database | TableName | NodesUserUsageHistory | backend-go/internal/database/models.go:220 |
| internal/database | TableName | NodesUsageHistory | backend-go/internal/database/models.go:232 |
| internal/database | TableName | Host | backend-go/internal/database/models.go:277 |
| internal/database | TableName | HostsToNode | backend-go/internal/database/models.go:288 |
| internal/database | TableName | InternalSquadHostLink | backend-go/internal/database/models.go:297 |
| internal/database | TableName | ConfigProfile | backend-go/internal/database/models.go:312 |
| internal/database | TableName | ConfigProfileInbound | backend-go/internal/database/models.go:331 |
| internal/database | TableName | ConfigProfileInboundsToNodes | backend-go/internal/database/models.go:342 |
| internal/database | TableName | PanelSetting | backend-go/internal/database/models.go:359 |
| internal/database | TableName | ApiToken | backend-go/internal/database/models.go:373 |
| internal/database | TableName | SubscriptionTemplate | backend-go/internal/database/models.go:390 |
| internal/database | TableName | SubscriptionPageConfig | backend-go/internal/database/models.go:405 |
| internal/database | TableName | ConfigProfileSnippet | backend-go/internal/database/models.go:415 |
| internal/database | TableName | SharedList | backend-go/internal/database/models.go:426 |
| internal/database | TableName | NodePlugin | backend-go/internal/database/models.go:440 |
| internal/database | TableName | InternalSquad | backend-go/internal/database/models.go:453 |
| internal/database | TableName | InternalSquadMember | backend-go/internal/database/models.go:464 |
| internal/database | TableName | InternalSquadInbound | backend-go/internal/database/models.go:475 |
| internal/database | TableName | ExternalSquadTemplate | backend-go/internal/database/models.go:487 |
| internal/database | TableName | ExternalSquad | backend-go/internal/database/models.go:508 |
| internal/database | TableName | InfraProvider | backend-go/internal/database/models.go:524 |
| internal/database | TableName | InfraBillingNode | backend-go/internal/database/models.go:540 |
| internal/database | TableName | InfraBillingHistory | backend-go/internal/database/models.go:552 |
| internal/database | TableName | HwidDevice | backend-go/internal/database/models.go:569 |
| internal/database | TableName | UserSubscriptionRequestHistory | backend-go/internal/database/models.go:584 |
| internal/database | TableName | EntityMeta | backend-go/internal/database/models.go:594 |
| internal/database | TableName | Keygen | backend-go/internal/database/models.go:610 |
| internal/database | TableName | Passkey | backend-go/internal/database/models.go:661 |
| internal/database | TableName | UserMeta | backend-go/internal/database/models.go:671 |
| internal/database | TableName | NodeMeta | backend-go/internal/database/models.go:679 |
| internal/database | TableName | TorrentBlockerReport | backend-go/internal/database/models.go:691 |
| internal/database | TableName | SubscriptionSetting | backend-go/internal/database/models.go:706 |
| internal/httpx | ColorFromID |  | backend-go/internal/httpx/color.go:11 |
| internal/httpx | ColorFromUUID |  | backend-go/internal/httpx/color.go:20 |
| internal/httpx | JSON |  | backend-go/internal/httpx/httpx.go:22 |
| internal/httpx | Response |  | backend-go/internal/httpx/httpx.go:29 |
| internal/httpx | Error |  | backend-go/internal/httpx/httpx.go:34 |
| internal/httpx | Unsupported |  | backend-go/internal/httpx/httpx.go:49 |
| internal/httpx | Decode |  | backend-go/internal/httpx/httpx.go:54 |
| internal/httpx | ClientIP |  | backend-go/internal/httpx/httpx.go:65 |
| internal/infrabilling | NewHandler |  | backend-go/internal/infrabilling/handler.go:21 |
| internal/infrabilling | formatProvider | h *Handler | backend-go/internal/infrabilling/handler.go:25 |
| internal/infrabilling | GetProviders | h *Handler | backend-go/internal/infrabilling/handler.go:84 |
| internal/infrabilling | GetProvider | h *Handler | backend-go/internal/infrabilling/handler.go:102 |
| internal/infrabilling | CreateProvider | h *Handler | backend-go/internal/infrabilling/handler.go:118 |
| internal/infrabilling | UpdateProvider | h *Handler | backend-go/internal/infrabilling/handler.go:154 |
| internal/infrabilling | DeleteProvider | h *Handler | backend-go/internal/infrabilling/handler.go:198 |
| internal/infrabilling | GetNodes | h *Handler | backend-go/internal/infrabilling/handler.go:204 |
| internal/infrabilling | CreateNode | h *Handler | backend-go/internal/infrabilling/handler.go:303 |
| internal/infrabilling | UpdateNode | h *Handler | backend-go/internal/infrabilling/handler.go:349 |
| internal/infrabilling | DeleteNode | h *Handler | backend-go/internal/infrabilling/handler.go:414 |
| internal/infrabilling | GetHistory | h *Handler | backend-go/internal/infrabilling/handler.go:420 |
| internal/infrabilling | CreateHistory | h *Handler | backend-go/internal/infrabilling/handler.go:451 |
| internal/infrabilling | DeleteHistory | h *Handler | backend-go/internal/infrabilling/handler.go:477 |
| internal/jobs | Error | e *RetryAfterError | backend-go/internal/jobs/queue.go:29 |
| internal/jobs | Unwrap | e *RetryAfterError | backend-go/internal/jobs/queue.go:30 |
| internal/jobs | Error | e *PermanentError | backend-go/internal/jobs/queue.go:35 |
| internal/jobs | Unwrap | e *PermanentError | backend-go/internal/jobs/queue.go:36 |
| internal/jobs | Permanent |  | backend-go/internal/jobs/queue.go:38 |
| internal/jobs | New |  | backend-go/internal/jobs/queue.go:45 |
| internal/jobs | Register | q *Queue | backend-go/internal/jobs/queue.go:48 |
| internal/jobs | Enqueue |  | backend-go/internal/jobs/queue.go:50 |
| internal/jobs | ID |  | backend-go/internal/jobs/queue.go:61 |
| internal/jobs | EnqueueUser |  | backend-go/internal/jobs/queue.go:73 |
| internal/jobs | EnqueueNode |  | backend-go/internal/jobs/queue.go:94 |
| internal/jobs | Cleanup |  | backend-go/internal/jobs/queue.go:105 |
| internal/jobs | claim | q *Queue | backend-go/internal/jobs/queue.go:111 |
| internal/jobs | RunOne | q *Queue | backend-go/internal/jobs/queue.go:152 |
| internal/jobs | Start | q *Queue | backend-go/internal/jobs/queue.go:204 |
| internal/keygen | NewService |  | backend-go/internal/keygen/keygen.go:28 |
| internal/keygen | EnsureKeygen | s *Service | backend-go/internal/keygen/keygen.go:34 |
| internal/keygen | GetMasterKeygen | s *Service | backend-go/internal/keygen/keygen.go:66 |
| internal/keygen | GenerateNodeSecretKey | s *Service | backend-go/internal/keygen/keygen.go:81 |
| internal/keygen | generateMasterCerts |  | backend-go/internal/keygen/keygen.go:107 |
| internal/keygen | generateNodeCert |  | backend-go/internal/keygen/keygen.go:171 |
| internal/keygen | generateJwtKeypair |  | backend-go/internal/keygen/keygen.go:223 |
| internal/metrics | gauge |  | backend-go/internal/metrics/definitions.go:9 |
| internal/metrics | counter |  | backend-go/internal/metrics/definitions.go:10 |
| internal/metrics | RecordNodeTraffic |  | backend-go/internal/metrics/definitions.go:59 |
| internal/metrics | L |  | backend-go/internal/metrics/registry.go:23 |
| internal/metrics | hash |  | backend-go/internal/metrics/registry.go:46 |
| internal/metrics | entry | m *Metric | backend-go/internal/metrics/registry.go:56 |
| internal/metrics | Set | m *Metric | backend-go/internal/metrics/registry.go:68 |
| internal/metrics | Inc | m *Metric | backend-go/internal/metrics/registry.go:78 |
| internal/metrics | Remove | m *Metric | backend-go/internal/metrics/registry.go:88 |
| internal/metrics | Reset | m *Metric | backend-go/internal/metrics/registry.go:105 |
| internal/metrics | Label | s Sample | backend-go/internal/metrics/registry.go:118 |
| internal/metrics | Samples | m *Metric | backend-go/internal/metrics/registry.go:128 |
| internal/metrics | Name | m *Metric | backend-go/internal/metrics/registry.go:140 |
| internal/metrics | newRegistry |  | backend-go/internal/metrics/registry.go:149 |
| internal/metrics | register | r *Registry | backend-go/internal/metrics/registry.go:153 |
| internal/metrics | escapeHelp |  | backend-go/internal/metrics/registry.go:164 |
| internal/metrics | escapeLabelValue |  | backend-go/internal/metrics/registry.go:168 |
| internal/metrics | formatValue |  | backend-go/internal/metrics/registry.go:172 |
| internal/metrics | Text | r *Registry | backend-go/internal/metrics/registry.go:188 |
| internal/middleware | Auth |  | backend-go/internal/middleware/auth.go:26 |
| internal/middleware | Cors |  | backend-go/internal/middleware/cors.go:9 |
| internal/middleware | Logger |  | backend-go/internal/middleware/logger.go:10 |
| internal/middleware | WriteHeader | w *statusWriter | backend-go/internal/middleware/status.go:18 |
| internal/middleware | Write | w *statusWriter | backend-go/internal/middleware/status.go:34 |
| internal/middleware | Flush | w *statusWriter | backend-go/internal/middleware/status.go:44 |
| internal/middleware | Unwrap | w *statusWriter | backend-go/internal/middleware/status.go:51 |
| internal/middleware | ContractStatus |  | backend-go/internal/middleware/status.go:55 |
| internal/nodes | BulkUpdate | s *Service | backend-go/internal/nodes/bulk.go:15 |
| internal/nodes | NewNodeClient |  | backend-go/internal/nodes/client.go:29 |
| internal/nodes | generateToken | c *Client | backend-go/internal/nodes/client.go:118 |
| internal/nodes | doRequest | c *Client | backend-go/internal/nodes/client.go:134 |
| internal/nodes | getNodePort |  | backend-go/internal/nodes/client.go:161 |
| internal/nodes | CheckHealth | c *Client | backend-go/internal/nodes/client.go:177 |
| internal/nodes | CollectTorrentReports | c *Client | backend-go/internal/nodes/client.go:239 |
| internal/nodes | SyncPlugin | c *Client | backend-go/internal/nodes/client.go:262 |
| internal/nodes | StartXray | c *Client | backend-go/internal/nodes/client.go:275 |
| internal/nodes | StopXray | c *Client | backend-go/internal/nodes/client.go:314 |
| internal/nodes | GetUsersIpList | c *Client | backend-go/internal/nodes/client.go:337 |
| internal/nodes | GetUserIpList | c *Client | backend-go/internal/nodes/client.go:382 |
| internal/nodes | GetLogs | c *Client | backend-go/internal/nodes/client.go:419 |
| internal/nodes | CheckUpdates | c *Client | backend-go/internal/nodes/client.go:450 |
| internal/nodes | ApplyUpdate | c *Client | backend-go/internal/nodes/client.go:476 |
| internal/nodes | GetSystemStats | c *Client | backend-go/internal/nodes/client.go:553 |
| internal/nodes | GetUsersStats | c *Client | backend-go/internal/nodes/client.go:576 |
| internal/nodes | GetCombinedStats | c *Client | backend-go/internal/nodes/client.go:613 |
| internal/nodes | AddUser | c *Client | backend-go/internal/nodes/client.go:662 |
| internal/nodes | RemoveUser | c *Client | backend-go/internal/nodes/client.go:691 |
| internal/nodes | Call | c *Client | backend-go/internal/nodes/commands.go:23 |
| internal/nodes | ApplyCommandJob | s *Service | backend-go/internal/nodes/commands.go:52 |
| internal/nodes | Error | e *ConfigRejectedError | backend-go/internal/nodes/config_rejection.go:27 |
| internal/nodes | summarizeXrayError |  | backend-go/internal/nodes/config_rejection.go:34 |
| internal/nodes | emitNode | s *Service | backend-go/internal/nodes/events.go:11 |
| internal/nodes | emitNodeByUUID | s *Service | backend-go/internal/nodes/events.go:16 |
| internal/nodes | EventData | s *Service | backend-go/internal/nodes/events.go:25 |
| internal/nodes | NewHandler |  | backend-go/internal/nodes/handler.go:23 |
| internal/nodes | formatNodeResponse |  | backend-go/internal/nodes/handler.go:55 |
| internal/nodes | formatNodeWith |  | backend-go/internal/nodes/handler.go:61 |
| internal/nodes | loadActiveInbounds |  | backend-go/internal/nodes/handler.go:68 |
| internal/nodes | formatNodeWithInbounds |  | backend-go/internal/nodes/handler.go:118 |
| internal/nodes | GetNodes | h *Handler | backend-go/internal/nodes/handler.go:317 |
| internal/nodes | GetTags | h *Handler | backend-go/internal/nodes/handler.go:339 |
| internal/nodes | CreateNode | h *Handler | backend-go/internal/nodes/handler.go:359 |
| internal/nodes | GetNode | h *Handler | backend-go/internal/nodes/handler.go:381 |
| internal/nodes | handleUpdateNode | h *Handler | backend-go/internal/nodes/handler.go:402 |
| internal/nodes | UpdateNode | h *Handler | backend-go/internal/nodes/handler.go:517 |
| internal/nodes | PatchNode | h *Handler | backend-go/internal/nodes/handler.go:522 |
| internal/nodes | DeleteNode | h *Handler | backend-go/internal/nodes/handler.go:527 |
| internal/nodes | EnableNode | h *Handler | backend-go/internal/nodes/handler.go:538 |
| internal/nodes | DisableNode | h *Handler | backend-go/internal/nodes/handler.go:552 |
| internal/nodes | GetTrafficSummary | h *Handler | backend-go/internal/nodes/handler.go:568 |
| internal/nodes | ResetTraffic | h *Handler | backend-go/internal/nodes/handler.go:581 |
| internal/nodes | RestartNode | h *Handler | backend-go/internal/nodes/handler.go:595 |
| internal/nodes | RestartAllNodes | h *Handler | backend-go/internal/nodes/handler.go:625 |
| internal/nodes | ReorderNodes | h *Handler | backend-go/internal/nodes/handler.go:638 |
| internal/nodes | BulkActions | h *Handler | backend-go/internal/nodes/handler.go:667 |
| internal/nodes | GetNodeLogs | h *Handler | backend-go/internal/nodes/handler.go:745 |
| internal/nodes | GetNodeUpdates | h *Handler | backend-go/internal/nodes/handler.go:794 |
| internal/nodes | ApplyNodeUpdate | h *Handler | backend-go/internal/nodes/handler.go:825 |
| internal/nodes | encodeNodeIPs |  | backend-go/internal/nodes/ips.go:21 |
| internal/nodes | decodeNodeIPs |  | backend-go/internal/nodes/ips.go:42 |
| internal/nodes | NanoToMultiplier |  | backend-go/internal/nodes/service.go:25 |
| internal/nodes | MultiplierToNano |  | backend-go/internal/nodes/service.go:35 |
| internal/nodes | NewService |  | backend-go/internal/nodes/service.go:67 |
| internal/nodes | initMetricsFromDB | s *Service | backend-go/internal/nodes/service.go:78 |
| internal/nodes | UpdateNodeMetrics | s *Service | backend-go/internal/nodes/service.go:98 |
| internal/nodes | Client | s *Service | backend-go/internal/nodes/service.go:109 |
| internal/nodes | ResetClient | s *Service | backend-go/internal/nodes/service.go:134 |
| internal/nodes | isSystemOrUnsecureProtocol |  | backend-go/internal/nodes/service.go:141 |
| internal/nodes | GetNodeActiveInboundTags | s *Service | backend-go/internal/nodes/service.go:150 |
| internal/nodes | GetNodeMetrics | s *Service | backend-go/internal/nodes/service.go:166 |
| internal/nodes | cloneMetrics |  | backend-go/internal/nodes/service.go:172 |
| internal/nodes | SetNodeMetrics | s *Service | backend-go/internal/nodes/service.go:182 |
| internal/nodes | DB | s *Service | backend-go/internal/nodes/service.go:188 |
| internal/nodes | CheckNodeHealth | s *Service | backend-go/internal/nodes/service.go:217 |
| internal/nodes | StartNode | s *Service | backend-go/internal/nodes/service.go:342 |
| internal/nodes | RestartNodesByProfile | s *Service | backend-go/internal/nodes/service.go:523 |
| internal/nodes | PollNodeStats | s *Service | backend-go/internal/nodes/service.go:551 |
| internal/nodes | StartHealthCheckLoop | s *Service | backend-go/internal/nodes/service.go:653 |
| internal/nodes | Create | s *Service | backend-go/internal/nodes/service.go:693 |
| internal/nodes | GetAll | s *Service | backend-go/internal/nodes/service.go:799 |
| internal/nodes | GetByUUID | s *Service | backend-go/internal/nodes/service.go:805 |
| internal/nodes | Update | s *Service | backend-go/internal/nodes/service.go:814 |
| internal/nodes | UpdateWithConfigProfile | s *Service | backend-go/internal/nodes/service.go:830 |
| internal/nodes | BulkUpdateConfigProfile | s *Service | backend-go/internal/nodes/service.go:851 |
| internal/nodes | updateNodeWithProfile |  | backend-go/internal/nodes/service.go:870 |
| internal/nodes | createNodeInboundLinks |  | backend-go/internal/nodes/service.go:906 |
| internal/nodes | Delete | s *Service | backend-go/internal/nodes/service.go:946 |
| internal/nodes | getVlessFlow |  | backend-go/internal/nodes/service.go:972 |
| internal/nodes | isSS2022 |  | backend-go/internal/nodes/service.go:989 |
| internal/nodes | GetUserResolvedInbounds | s *Service | backend-go/internal/nodes/service.go:1004 |
| internal/nodes | syncUserToSingleNode | s *Service | backend-go/internal/nodes/service.go:1029 |
| internal/nodes | SyncAllUsersToNode | s *Service | backend-go/internal/nodes/service.go:1109 |
| internal/nodes | SyncUserToNodes | s *Service | backend-go/internal/nodes/service.go:1134 |
| internal/nodes | RemoveUserFromNodes | s *Service | backend-go/internal/nodes/service.go:1142 |
| internal/nodes | SyncAllUsersToConnectedNodes | s *Service | backend-go/internal/nodes/service.go:1150 |
| internal/nodes | ApplyUserJob | s *Service | backend-go/internal/nodes/service.go:1160 |
| internal/nodes | ApplyRetireJob | s *Service | backend-go/internal/nodes/service.go:1205 |
| internal/nodes | ApplyNodeJob | s *Service | backend-go/internal/nodes/service.go:1224 |
| internal/nodes | SetDisabled | s *Service | backend-go/internal/nodes/service.go:1271 |
| internal/nodes | logf |  | backend-go/internal/nodes/service.go:1301 |
| internal/nodes | hkdfDerive |  | backend-go/internal/nodes/sni.go:11 |
| internal/nodes | DeriveSNI |  | backend-go/internal/nodes/sni.go:34 |
| internal/nodes | inboundUsersHash |  | backend-go/internal/nodes/start_config.go:17 |
| internal/nodes | populateConfigUsers | s *Service | backend-go/internal/nodes/start_config.go:42 |
| internal/nodes | enqueueReportCollection | s *Service | backend-go/internal/nodes/torrent.go:20 |
| internal/nodes | ApplyCollectJob | s *Service | backend-go/internal/nodes/torrent.go:30 |
| internal/nodes | storeTorrentReports | s *Service | backend-go/internal/nodes/torrent.go:49 |
| internal/nodes | ValidTrackingStart |  | backend-go/internal/nodes/traffic_tracking.go:24 |
| internal/nodes | trafficPeriodStart |  | backend-go/internal/nodes/traffic_tracking.go:31 |
| internal/nodes | trafficResetAt |  | backend-go/internal/nodes/traffic_tracking.go:40 |
| internal/nodes | applyTrackingStart |  | backend-go/internal/nodes/traffic_tracking.go:55 |
| internal/nodes | LifetimeTraffic | s *Service | backend-go/internal/nodes/traffic_tracking.go:90 |
| internal/nodes | SetUsageOptions | s *Service | backend-go/internal/nodes/usage.go:25 |
| internal/nodes | multiplyConsumption |  | backend-go/internal/nodes/usage.go:29 |
| internal/nodes | recordUserUsage | s *Service | backend-go/internal/nodes/usage.go:52 |
| internal/nodes | reorder |  | backend-go/internal/nodes/usage.go:131 |
| internal/nodessh | send | t *terminal | backend-go/internal/nodessh/terminal.go:46 |
| internal/nodessh | ask | t *terminal | backend-go/internal/nodessh/terminal.go:55 |
| internal/nodessh | PublicKey | s *browserSigner | backend-go/internal/nodessh/terminal.go:84 |
| internal/nodessh | Sign | s *browserSigner | backend-go/internal/nodessh/terminal.go:85 |
| internal/nodessh | Algorithms | s *browserSigner | backend-go/internal/nodessh/terminal.go:88 |
| internal/nodessh | SignWithAlgorithm | s *browserSigner | backend-go/internal/nodessh/terminal.go:94 |
| internal/nodessh | terminal | h *Handler | backend-go/internal/nodessh/terminal.go:122 |
| internal/nodessh | validSize |  | backend-go/internal/nodessh/terminal.go:235 |
| internal/nodessh | connect | t *terminal | backend-go/internal/nodessh/terminal.go:238 |
| internal/nodessh | Write | w terminalWriter | backend-go/internal/nodessh/terminal.go:329 |
| internal/nodessh | NewHandler |  | backend-go/internal/nodessh/tickets.go:24 |
| internal/nodessh | clientIP |  | backend-go/internal/nodessh/tickets.go:33 |
| internal/nodessh | Ticket | h *Handler | backend-go/internal/nodessh/tickets.go:43 |
| internal/nodessh | Socket | h *Handler | backend-go/internal/nodessh/tickets.go:69 |
| internal/nodessh | vaultServer |  | backend-go/internal/nodessh/vault.go:19 |
| internal/nodessh | EvaluateVault | h *Handler | backend-go/internal/nodessh/vault.go:30 |
| internal/notify | Scope | e Event | backend-go/internal/notify/notify.go:47 |
| internal/notify | New |  | backend-go/internal/notify/notify.go:75 |
| internal/notify | dashboardURL |  | backend-go/internal/notify/notify.go:123 |
| internal/notify | enabled | n *Notifier | backend-go/internal/notify/notify.go:141 |
| internal/notify | telegramTarget | n *Notifier | backend-go/internal/notify/notify.go:153 |
| internal/notify | uniqueRevision |  | backend-go/internal/notify/notify.go:183 |
| internal/notify | Emit | n *Notifier | backend-go/internal/notify/notify.go:190 |
| internal/notify | Register | n *Notifier | backend-go/internal/notify/notify.go:235 |
| internal/notify | deliverWebhook | n *Notifier | backend-go/internal/notify/notify.go:240 |
| internal/notify | deliverTelegram | n *Notifier | backend-go/internal/notify/notify.go:270 |
| internal/notify | CheckTelegram | n *Notifier | backend-go/internal/notify/notify.go:335 |
| internal/notify | SetDefault |  | backend-go/internal/notify/notify.go:366 |
| internal/notify | Emit |  | backend-go/internal/notify/notify.go:370 |
| internal/notify | toFields |  | backend-go/internal/notify/templates.go:23 |
| internal/notify | get | f fields | backend-go/internal/notify/templates.go:35 |
| internal/notify | s | f fields | backend-go/internal/notify/templates.go:49 |
| internal/notify | n | f fields | backend-go/internal/notify/templates.go:62 |
| internal/notify | t | f fields | backend-go/internal/notify/templates.go:74 |
| internal/notify | prettyBytes |  | backend-go/internal/notify/templates.go:85 |
| internal/notify | emoji |  | backend-go/internal/notify/templates.go:103 |
| internal/notify | header |  | backend-go/internal/notify/templates.go:107 |
| internal/notify | nodeHeader |  | backend-go/internal/notify/templates.go:109 |
| internal/notify | userBasic |  | backend-go/internal/notify/templates.go:116 |
| internal/notify | userFull |  | backend-go/internal/notify/templates.go:118 |
| internal/notify | userSquads |  | backend-go/internal/notify/templates.go:125 |
| internal/notify | nodeBasic |  | backend-go/internal/notify/templates.go:139 |
| internal/notify | nodeConnection |  | backend-go/internal/notify/templates.go:143 |
| internal/notify | crmPayment |  | backend-go/internal/notify/templates.go:150 |
| internal/notify | crmLink |  | backend-go/internal/notify/templates.go:156 |
| internal/notify | daysPastDue |  | backend-go/internal/notify/templates.go:160 |
| internal/notify | render | n *Notifier | backend-go/internal/notify/templates.go:171 |
| internal/notify | maskSecret |  | backend-go/internal/notify/templates.go:327 |
| internal/notify | orDefault |  | backend-go/internal/notify/templates.go:335 |
| internal/notify | knownEvent |  | backend-go/internal/notify/templates.go:359 |
| internal/prometheus | NewExporter |  | backend-go/internal/prometheus/exporter.go:43 |
| internal/prometheus | Run | e *Exporter | backend-go/internal/prometheus/exporter.go:48 |
| internal/prometheus | Export | e *Exporter | backend-go/internal/prometheus/exporter.go:67 |
| internal/prometheus | loadShortUserStats | e *Exporter | backend-go/internal/prometheus/exporter.go:87 |
| internal/prometheus | reportShortUserStats | e *Exporter | backend-go/internal/prometheus/exporter.go:118 |
| internal/prometheus | CountryEmoji |  | backend-go/internal/prometheus/exporter.go:138 |
| internal/prometheus | allNodes | e *Exporter | backend-go/internal/prometheus/exporter.go:162 |
| internal/prometheus | basicLabels |  | backend-go/internal/prometheus/exporter.go:171 |
| internal/prometheus | removeNodeSystemMetrics |  | backend-go/internal/prometheus/exporter.go:186 |
| internal/prometheus | loadAvg |  | backend-go/internal/prometheus/exporter.go:192 |
| internal/prometheus | reportNodesStats | e *Exporter | backend-go/internal/prometheus/exporter.go:200 |
| internal/prometheus | CurrentRuntimeMetric |  | backend-go/internal/prometheus/exporter.go:281 |
| internal/prometheus | reportRuntimeMetrics | e *Exporter | backend-go/internal/prometheus/exporter.go:299 |
| internal/prometheus | Sync | e *Exporter | backend-go/internal/prometheus/exporter.go:322 |
| internal/prometheus | residentSetSize |  | backend-go/internal/prometheus/rss.go:11 |
| internal/prometheus | Handler |  | backend-go/internal/prometheus/server.go:20 |
| internal/prometheus | dropConnection |  | backend-go/internal/prometheus/server.go:33 |
| internal/prometheus | writeJSON |  | backend-go/internal/prometheus/server.go:43 |
| internal/prometheus | serveMetrics |  | backend-go/internal/prometheus/server.go:50 |
| internal/prometheus | serveHealth |  | backend-go/internal/prometheus/server.go:63 |
| internal/prometheus | Serve |  | backend-go/internal/prometheus/server.go:83 |
| internal/responserules | UnmarshalJSON | h *Headers | backend-go/internal/responserules/headers.go:23 |
| internal/responserules | MarshalJSON | h Headers | backend-go/internal/responserules/headers.go:61 |
| internal/responserules | Normalize |  | backend-go/internal/responserules/headers.go:80 |
| internal/server | dashboardHandler |  | backend-go/internal/server/dashboard.go:22 |
| internal/server | serveDashboardFile |  | backend-go/internal/server/dashboard.go:93 |
| internal/server | acceptsGzip |  | backend-go/internal/server/dashboard.go:142 |
| internal/server | ensureGlobalSymlink |  | backend-go/internal/server/server.go:44 |
| internal/server | warnIfRoot |  | backend-go/internal/server/server.go:69 |
| internal/server | warnWritableExecutable |  | backend-go/internal/server/server.go:79 |
| internal/server | Run |  | backend-go/internal/server/server.go:95 |
| internal/server | Start | a *App | backend-go/internal/server/server.go:240 |
| internal/server | NewApp |  | backend-go/internal/server/server.go:243 |
| internal/serviceunit | Install |  | backend-go/internal/serviceunit/service.go:14 |
| internal/squads | NewHandler |  | backend-go/internal/squads/handler.go:25 |
| internal/squads | uniqueInboundUUIDs |  | backend-go/internal/squads/handler.go:29 |
| internal/squads | internalSquadTags |  | backend-go/internal/squads/handler.go:46 |
| internal/squads | formatInternalSquad |  | backend-go/internal/squads/handler.go:53 |
| internal/squads | GetInternalSquads | h *Handler | backend-go/internal/squads/handler.go:105 |
| internal/squads | GetInternalSquad | h *Handler | backend-go/internal/squads/handler.go:123 |
| internal/squads | CreateInternalSquad | h *Handler | backend-go/internal/squads/handler.go:139 |
| internal/squads | UpdateInternalSquad | h *Handler | backend-go/internal/squads/handler.go:210 |
| internal/squads | DeleteInternalSquad | h *Handler | backend-go/internal/squads/handler.go:295 |
| internal/squads | ReorderInternalSquads | h *Handler | backend-go/internal/squads/handler.go:323 |
| internal/squads | GetInternalSquadsTags | h *Handler | backend-go/internal/squads/handler.go:357 |
| internal/squads | SetInternalSquadsTags | h *Handler | backend-go/internal/squads/handler.go:381 |
| internal/squads | GetInternalSquadAccessibleNodes | h *Handler | backend-go/internal/squads/handler.go:417 |
| internal/squads | enqueueAffected |  | backend-go/internal/squads/handler.go:481 |
| internal/squads | SquadBulkAction | h *Handler | backend-go/internal/squads/handler.go:496 |
| internal/squads | nullableJSON |  | backend-go/internal/squads/handler.go:579 |
| internal/squads | formatExternalSquad |  | backend-go/internal/squads/handler.go:591 |
| internal/squads | GetExternalSquads | h *Handler | backend-go/internal/squads/handler.go:644 |
| internal/squads | GetExternalSquad | h *Handler | backend-go/internal/squads/handler.go:662 |
| internal/squads | CreateExternalSquad | h *Handler | backend-go/internal/squads/handler.go:678 |
| internal/squads | UpdateExternalSquad | h *Handler | backend-go/internal/squads/handler.go:733 |
| internal/squads | DeleteExternalSquad | h *Handler | backend-go/internal/squads/handler.go:853 |
| internal/squads | ReorderExternalSquads | h *Handler | backend-go/internal/squads/handler.go:861 |
| internal/squads | GetExternalSquadsTags | h *Handler | backend-go/internal/squads/handler.go:895 |
| internal/squads | SetExternalSquadsTags | h *Handler | backend-go/internal/squads/handler.go:919 |
| internal/stubs | enqueueCommands | s *StubHandler | backend-go/internal/stubs/commands.go:18 |
| internal/stubs | pluginExecute | s *StubHandler | backend-go/internal/stubs/commands.go:46 |
| internal/stubs | dropConnections | s *StubHandler | backend-go/internal/stubs/commands.go:108 |
| internal/stubs | geocheck | s *StubHandler | backend-go/internal/stubs/commands.go:161 |
| internal/stubs | geocheckResult | s *StubHandler | backend-go/internal/stubs/commands.go:184 |
| internal/stubs | userDevices | s *StubHandler | backend-go/internal/stubs/hwid.go:22 |
| internal/stubs | deviceLimit | s *StubHandler | backend-go/internal/stubs/hwid.go:33 |
| internal/stubs | CreateHwidDevice | s *StubHandler | backend-go/internal/stubs/hwid.go:55 |
| internal/stubs | DeleteHwidDevice | s *StubHandler | backend-go/internal/stubs/hwid.go:115 |
| internal/stubs | DeleteAllHwidDevices | s *StubHandler | backend-go/internal/stubs/hwid.go:150 |
| internal/stubs | formatIntegration |  | backend-go/internal/stubs/integrations.go:16 |
| internal/stubs | integrationList | s *StubHandler | backend-go/internal/stubs/integrations.go:21 |
| internal/stubs | integrationGet | s *StubHandler | backend-go/internal/stubs/integrations.go:34 |
| internal/stubs | integrationWrite | s *StubHandler | backend-go/internal/stubs/integrations.go:43 |
| internal/stubs | integrationDelete | s *StubHandler | backend-go/internal/stubs/integrations.go:126 |
| internal/stubs | pluginClone | s *StubHandler | backend-go/internal/stubs/plugins.go:16 |
| internal/stubs | pluginTags | s *StubHandler | backend-go/internal/stubs/plugins.go:40 |
| internal/stubs | pluginSetTags | s *StubHandler | backend-go/internal/stubs/plugins.go:60 |
| internal/stubs | enqueuePlugin |  | backend-go/internal/stubs/plugins.go:81 |
| internal/stubs | sharedListSync | s *StubHandler | backend-go/internal/stubs/plugins.go:94 |
| internal/stubs | snippetSync | s *StubHandler | backend-go/internal/stubs/plugins.go:150 |
| internal/stubs | validateSharedListConfig |  | backend-go/internal/stubs/shared_lists.go:24 |
| internal/stubs | validIPOrCIDR |  | backend-go/internal/stubs/shared_lists.go:60 |
| internal/stubs | validSharedListName |  | backend-go/internal/stubs/shared_lists.go:72 |
| internal/stubs | sharedListResponse |  | backend-go/internal/stubs/shared_lists.go:76 |
| internal/stubs | GetSharedLists | s *StubHandler | backend-go/internal/stubs/shared_lists.go:82 |
| internal/stubs | GetSharedListByName | s *StubHandler | backend-go/internal/stubs/shared_lists.go:100 |
| internal/stubs | decodeSharedList |  | backend-go/internal/stubs/shared_lists.go:120 |
| internal/stubs | CreateSharedList | s *StubHandler | backend-go/internal/stubs/shared_lists.go:135 |
| internal/stubs | UpdateSharedList | s *StubHandler | backend-go/internal/stubs/shared_lists.go:158 |
| internal/stubs | DeleteSharedList | s *StubHandler | backend-go/internal/stubs/shared_lists.go:178 |
| internal/stubs | NewHandler |  | backend-go/internal/stubs/stubs.go:54 |
| internal/stubs | SetSubPublicDomain | s *StubHandler | backend-go/internal/stubs/stubs.go:68 |
| internal/stubs | SetClientSource | s *StubHandler | backend-go/internal/stubs/stubs.go:72 |
| internal/stubs | getNodeClient | s *StubHandler | backend-go/internal/stubs/stubs.go:74 |
| internal/stubs | formatLastSeen |  | backend-go/internal/stubs/stubs.go:93 |
| internal/stubs | RegisterRoutes | s *StubHandler | backend-go/internal/stubs/stubs.go:128 |
| internal/stubs | formatPlugin |  | backend-go/internal/stubs/stubs.go:221 |
| internal/stubs | GetNodePlugins | s *StubHandler | backend-go/internal/stubs/stubs.go:239 |
| internal/stubs | GetNodePluginByUuid | s *StubHandler | backend-go/internal/stubs/stubs.go:255 |
| internal/stubs | CreateNodePlugin | s *StubHandler | backend-go/internal/stubs/stubs.go:269 |
| internal/stubs | UpdateNodePlugin | s *StubHandler | backend-go/internal/stubs/stubs.go:298 |
| internal/stubs | DeleteNodePlugin | s *StubHandler | backend-go/internal/stubs/stubs.go:327 |
| internal/stubs | CloneNodePlugin | s *StubHandler | backend-go/internal/stubs/stubs.go:333 |
| internal/stubs | ReorderNodePlugins | s *StubHandler | backend-go/internal/stubs/stubs.go:335 |
| internal/stubs | syncPluginToNodes | s *StubHandler | backend-go/internal/stubs/stubs.go:362 |
| internal/stubs | SyncNodePlugin | s *StubHandler | backend-go/internal/stubs/stubs.go:368 |
| internal/stubs | ExecuteNodePlugin | s *StubHandler | backend-go/internal/stubs/stubs.go:385 |
| internal/stubs | GetNodePluginsTags | s *StubHandler | backend-go/internal/stubs/stubs.go:389 |
| internal/stubs | SetNodePluginsTags | s *StubHandler | backend-go/internal/stubs/stubs.go:391 |
| internal/stubs | SyncSharedLists | s *StubHandler | backend-go/internal/stubs/stubs.go:395 |
| internal/stubs | GetNodeIntegrations | s *StubHandler | backend-go/internal/stubs/stubs.go:397 |
| internal/stubs | GetNodeIntegration | s *StubHandler | backend-go/internal/stubs/stubs.go:401 |
| internal/stubs | CreateNodeIntegration | s *StubHandler | backend-go/internal/stubs/stubs.go:405 |
| internal/stubs | UpdateNodeIntegration | s *StubHandler | backend-go/internal/stubs/stubs.go:409 |
| internal/stubs | DeleteNodeIntegration | s *StubHandler | backend-go/internal/stubs/stubs.go:413 |
| internal/stubs | GetKeygen | s *StubHandler | backend-go/internal/stubs/stubs.go:417 |
| internal/stubs | GetSnippets | s *StubHandler | backend-go/internal/stubs/stubs.go:431 |
| internal/stubs | CreateSnippet | s *StubHandler | backend-go/internal/stubs/stubs.go:452 |
| internal/stubs | UpdateSnippet | s *StubHandler | backend-go/internal/stubs/stubs.go:470 |
| internal/stubs | DeleteSnippet | s *StubHandler | backend-go/internal/stubs/stubs.go:474 |
| internal/stubs | SyncSnippets | s *StubHandler | backend-go/internal/stubs/stubs.go:483 |
| internal/stubs | GetApiTokens | s *StubHandler | backend-go/internal/stubs/stubs.go:485 |
| internal/stubs | CreateApiToken | s *StubHandler | backend-go/internal/stubs/stubs.go:511 |
| internal/stubs | DeleteApiToken | s *StubHandler | backend-go/internal/stubs/stubs.go:558 |
| internal/stubs | GetPasskeys | s *StubHandler | backend-go/internal/stubs/stubs.go:564 |
| internal/stubs | UpdatePasskey | s *StubHandler | backend-go/internal/stubs/stubs.go:588 |
| internal/stubs | DeletePasskey | s *StubHandler | backend-go/internal/stubs/stubs.go:603 |
| internal/stubs | GetPasskeyRegOptions | s *StubHandler | backend-go/internal/stubs/stubs.go:614 |
| internal/stubs | VerifyPasskeyReg | s *StubHandler | backend-go/internal/stubs/stubs.go:618 |
| internal/stubs | GetPasskeyAuthOptions | s *StubHandler | backend-go/internal/stubs/stubs.go:622 |
| internal/stubs | VerifyPasskeyAuth | s *StubHandler | backend-go/internal/stubs/stubs.go:626 |
| internal/stubs | GetOtt | s *StubHandler | backend-go/internal/stubs/stubs.go:630 |
| internal/stubs | CreateSshTicket | s *StubHandler | backend-go/internal/stubs/stubs.go:634 |
| internal/stubs | EvaluateVault | s *StubHandler | backend-go/internal/stubs/stubs.go:638 |
| internal/stubs | OAuth2TelegramCallback | s *StubHandler | backend-go/internal/stubs/stubs.go:642 |
| internal/stubs | OAuth2Authorize | s *StubHandler | backend-go/internal/stubs/stubs.go:646 |
| internal/stubs | OAuth2Callback | s *StubHandler | backend-go/internal/stubs/stubs.go:650 |
| internal/stubs | GetHwidStats | s *StubHandler | backend-go/internal/stubs/stubs.go:654 |
| internal/stubs | GetHwidTopUsers | s *StubHandler | backend-go/internal/stubs/stubs.go:745 |
| internal/stubs | GetHwidDevices | s *StubHandler | backend-go/internal/stubs/stubs.go:787 |
| internal/stubs | GetUserHwidDevices | s *StubHandler | backend-go/internal/stubs/stubs.go:837 |
| internal/stubs | ConnectionsByUser | s *StubHandler | backend-go/internal/stubs/stubs.go:860 |
| internal/stubs | ConnectionsByUserResult | s *StubHandler | backend-go/internal/stubs/stubs.go:949 |
| internal/stubs | ConnectionsByNode | s *StubHandler | backend-go/internal/stubs/stubs.go:981 |
| internal/stubs | ConnectionsByNodeResult | s *StubHandler | backend-go/internal/stubs/stubs.go:1091 |
| internal/stubs | GeocheckByNode | s *StubHandler | backend-go/internal/stubs/stubs.go:1117 |
| internal/stubs | GeocheckByNodeResult | s *StubHandler | backend-go/internal/stubs/stubs.go:1119 |
| internal/stubs | DropConnections | s *StubHandler | backend-go/internal/stubs/stubs.go:1123 |
| internal/stubs | GetNodeMetadata | s *StubHandler | backend-go/internal/stubs/stubs.go:1127 |
| internal/stubs | UpsertNodeMetadata | s *StubHandler | backend-go/internal/stubs/stubs.go:1154 |
| internal/stubs | GetUserMetadata | s *StubHandler | backend-go/internal/stubs/stubs.go:1182 |
| internal/stubs | UpsertUserMetadata | s *StubHandler | backend-go/internal/stubs/stubs.go:1208 |
| internal/stubs | subscriptions | s *StubHandler | backend-go/internal/stubs/stubs.go:1236 |
| internal/stubs | GetAllSubscriptions | s *StubHandler | backend-go/internal/stubs/stubs.go:1244 |
| internal/stubs | GetSubscriptionById | s *StubHandler | backend-go/internal/stubs/stubs.go:1248 |
| internal/stubs | GetSubscriptionByShortUuid | s *StubHandler | backend-go/internal/stubs/stubs.go:1252 |
| internal/stubs | GetRawSubscriptionByShortUuid | s *StubHandler | backend-go/internal/stubs/stubs.go:1256 |
| internal/stubs | GetSubscriptionByUsername | s *StubHandler | backend-go/internal/stubs/stubs.go:1260 |
| internal/stubs | GetConnectionKeysByUserId | s *StubHandler | backend-go/internal/stubs/stubs.go:1264 |
| internal/stubs | GetSubpageConfigByShortUuid | s *StubHandler | backend-go/internal/stubs/stubs.go:1268 |
| internal/stubs | GetSubHistory | s *StubHandler | backend-go/internal/stubs/stubs.go:1272 |
| internal/stubs | GetSubHistoryStats | s *StubHandler | backend-go/internal/stubs/stubs.go:1347 |
| internal/stubs | colorFromUUID |  | backend-go/internal/stubs/stubs.go:1426 |
| internal/stubs | colorFromID |  | backend-go/internal/stubs/stubs.go:1437 |
| internal/stubs | parseDateRange |  | backend-go/internal/stubs/stubs.go:1441 |
| internal/stubs | GetBandwidthStatsNodes | s *StubHandler | backend-go/internal/stubs/stubs.go:1460 |
| internal/stubs | GetBandwidthStatsUsers | s *StubHandler | backend-go/internal/stubs/stubs.go:1606 |
| internal/stubs | GetBandwidthStatsNodeUsers | s *StubHandler | backend-go/internal/stubs/stubs.go:1768 |
| internal/stubs | GetBandwidthNodesUsage | s *StubHandler | backend-go/internal/stubs/stubs.go:1875 |
| internal/stubs | SetConfig | s *StubHandler | backend-go/internal/stubs/system_tools.go:24 |
| internal/stubs | nullableList |  | backend-go/internal/stubs/system_tools.go:26 |
| internal/stubs | GetSystemConfiguration | s *StubHandler | backend-go/internal/stubs/system_tools.go:33 |
| internal/stubs | GetStatsDigest | s *StubHandler | backend-go/internal/stubs/system_tools.go:60 |
| internal/stubs | GenerateX25519 | s *StubHandler | backend-go/internal/stubs/system_tools.go:109 |
| internal/stubs | DebugSrrMatcher | s *StubHandler | backend-go/internal/stubs/system_tools.go:127 |
| internal/stubs | squadNodes | s *StubHandler | backend-go/internal/stubs/system_tools.go:167 |
| internal/stubs | dayRange |  | backend-go/internal/stubs/system_tools.go:186 |
| internal/stubs | squadExists | s *StubHandler | backend-go/internal/stubs/system_tools.go:195 |
| internal/stubs | GetBandwidthSquadUsage | s *StubHandler | backend-go/internal/stubs/system_tools.go:204 |
| internal/stubs | GetBandwidthSquadUserUsage | s *StubHandler | backend-go/internal/stubs/system_tools.go:267 |
| internal/stubs | parseTableQuery |  | backend-go/internal/stubs/torrent_blocker.go:32 |
| internal/stubs | orderByTableSorting |  | backend-go/internal/stubs/torrent_blocker.go:64 |
| internal/stubs | jsonText |  | backend-go/internal/stubs/torrent_blocker.go:85 |
| internal/stubs | likeOperator |  | backend-go/internal/stubs/torrent_blocker.go:100 |
| internal/stubs | GetTorrentBlockerReports | s *StubHandler | backend-go/internal/stubs/torrent_blocker.go:107 |
| internal/stubs | GetTorrentBlockerStats | s *StubHandler | backend-go/internal/stubs/torrent_blocker.go:216 |
| internal/stubs | TruncateTorrentBlockerReports | s *StubHandler | backend-go/internal/stubs/torrent_blocker.go:273 |
| internal/subscription | template | s *subSettings | backend-go/internal/subscription/data.go:35 |
| internal/subscription | jsonPresent |  | backend-go/internal/subscription/data.go:40 |
| internal/subscription | hasContent |  | backend-go/internal/subscription/data.go:46 |
| internal/subscription | parseHeaderObject |  | backend-go/internal/subscription/data.go:63 |
| internal/subscription | loadSettings | h *Handler | backend-go/internal/subscription/data.go:76 |
| internal/subscription | applySquadOverrides | h *Handler | backend-go/internal/subscription/data.go:104 |
| internal/subscription | parseHostOverrides |  | backend-go/internal/subscription/data.go:180 |
| internal/subscription | squadTemplateName | h *Handler | backend-go/internal/subscription/data.go:202 |
| internal/subscription | templates | h *Handler | backend-go/internal/subscription/data.go:220 |
| internal/subscription | nullable |  | backend-go/internal/subscription/data.go:252 |
| internal/subscription | templateUser |  | backend-go/internal/subscription/data.go:260 |
| internal/subscription | parseJSONColumn |  | backend-go/internal/subscription/data.go:275 |
| internal/subscription | oneOf |  | backend-go/internal/subscription/data.go:288 |
| internal/subscription | templateHost |  | backend-go/internal/subscription/data.go:298 |
| internal/subscription | hostsForUser | h *Handler | backend-go/internal/subscription/data.go:343 |
| internal/subscription | parseAgeRecipient |  | backend-go/internal/subscription/encrypt.go:16 |
| internal/subscription | encryptResponseBody |  | backend-go/internal/subscription/encrypt.go:31 |
| internal/subscription | expressETag |  | backend-go/internal/subscription/express.go:20 |
| internal/subscription | expressFresh |  | backend-go/internal/subscription/express.go:32 |
| internal/subscription | withCharset |  | backend-go/internal/subscription/express.go:67 |
| internal/subscription | expressType |  | backend-go/internal/subscription/express.go:77 |
| internal/subscription | expressSend |  | backend-go/internal/subscription/express.go:88 |
| internal/subscription | expressJSON |  | backend-go/internal/subscription/express.go:120 |
| internal/subscription | nestError |  | backend-go/internal/subscription/express.go:129 |
| internal/subscription | NewHandler |  | backend-go/internal/subscription/handler.go:26 |
| internal/subscription | RunHistoryWriter | h *Handler | backend-go/internal/subscription/handler.go:32 |
| internal/subscription | WaitHistoryWriter | h *Handler | backend-go/internal/subscription/handler.go:36 |
| internal/subscription | SetDisableHistory | h *Handler | backend-go/internal/subscription/handler.go:39 |
| internal/subscription | GetSubscriptionInfo | h *Handler | backend-go/internal/subscription/handler.go:44 |
| internal/subscription | daysLeft |  | backend-go/internal/subscription/handler.go:59 |
| internal/subscription | prettyBytes |  | backend-go/internal/subscription/handler.go:63 |
| internal/subscription | subscriptionInfo | h *Handler | backend-go/internal/subscription/handler.go:69 |
| internal/subscription | stringsToAny |  | backend-go/internal/subscription/handler.go:116 |
| internal/subscription | newHistoryWriter |  | backend-go/internal/subscription/history.go:33 |
| internal/subscription | add | w *historyWriter | backend-go/internal/subscription/history.go:39 |
| internal/subscription | Run | w *historyWriter | backend-go/internal/subscription/history.go:54 |
| internal/subscription | isRunning | w *historyWriter | backend-go/internal/subscription/history.go:88 |
| internal/subscription | Wait | w *historyWriter | backend-go/internal/subscription/history.go:95 |
| internal/subscription | collect | w *historyWriter | backend-go/internal/subscription/history.go:109 |
| internal/subscription | write | w *historyWriter | backend-go/internal/subscription/history.go:121 |
| internal/subscription | truncateHeader |  | backend-go/internal/subscription/hwid.go:22 |
| internal/subscription | truncateUTF16 |  | backend-go/internal/subscription/hwid.go:31 |
| internal/subscription | extractHwidHeaders |  | backend-go/internal/subscription/hwid.go:56 |
| internal/subscription | optionalIP |  | backend-go/internal/subscription/hwid.go:84 |
| internal/subscription | upsertHwidDevice |  | backend-go/internal/subscription/hwid.go:93 |
| internal/subscription | upsertHwidQuietly | h *Handler | backend-go/internal/subscription/hwid.go:108 |
| internal/subscription | checkHwidDeviceLimit | h *Handler | backend-go/internal/subscription/hwid.go:117 |
| internal/subscription | protectedUser | h *Handler | backend-go/internal/subscription/protected.go:19 |
| internal/subscription | InfoProtected | h *Handler | backend-go/internal/subscription/protected.go:35 |
| internal/subscription | ListProtected | h *Handler | backend-go/internal/subscription/protected.go:50 |
| internal/subscription | RawProtected | h *Handler | backend-go/internal/subscription/protected.go:80 |
| internal/subscription | ConnectionKeys | h *Handler | backend-go/internal/subscription/protected.go:176 |
| internal/subscription | SubpageConfig | h *Handler | backend-go/internal/subscription/protected.go:225 |
| internal/subscription | optionalString |  | backend-go/internal/subscription/protected.go:252 |
| internal/subscription | formatInt |  | backend-go/internal/subscription/protected.go:259 |
| internal/subscription | nodeHeaders |  | backend-go/internal/subscription/serve.go:49 |
| internal/subscription | matchesAny |  | backend-go/internal/subscription/serve.go:83 |
| internal/subscription | resolveExtendedClients |  | backend-go/internal/subscription/serve.go:93 |
| internal/subscription | responseRules | h *Handler | backend-go/internal/subscription/serve.go:115 |
| internal/subscription | GetSubscription | h *Handler | backend-go/internal/subscription/serve.go:202 |
| internal/subscription | notFound |  | backend-go/internal/subscription/serve.go:217 |
| internal/subscription | findUser | h *Handler | backend-go/internal/subscription/serve.go:221 |
| internal/subscription | serve | h *Handler | backend-go/internal/subscription/serve.go:231 |
| internal/subscription | finalize | h *Handler | backend-go/internal/subscription/serve.go:334 |
| internal/subscription | profileHeaders | h *Handler | backend-go/internal/subscription/serve.go:354 |
| internal/subscription | recordRequest | h *Handler | backend-go/internal/subscription/serve.go:383 |
| internal/subscription | MatchSRRRules |  | backend-go/internal/subscription/srr.go:65 |
| internal/subscription | Match | config *SRRConfig | backend-go/internal/subscription/srr.go:77 |
| internal/subscription | matchRule |  | backend-go/internal/subscription/srr.go:96 |
| internal/subscription | matchCondition |  | backend-go/internal/subscription/srr.go:120 |
| internal/subscription | handleOverrideClientType |  | backend-go/internal/subscription/srr.go:165 |
| internal/subtemplates | NewHandler |  | backend-go/internal/subtemplates/handler.go:24 |
| internal/subtemplates | formatTemplateResponse |  | backend-go/internal/subtemplates/handler.go:28 |
| internal/subtemplates | GetAllTemplates | h *Handler | backend-go/internal/subtemplates/handler.go:56 |
| internal/subtemplates | GetTemplateByUuid | h *Handler | backend-go/internal/subtemplates/handler.go:78 |
| internal/subtemplates | CreateTemplate | h *Handler | backend-go/internal/subtemplates/handler.go:96 |
| internal/subtemplates | UpdateTemplate | h *Handler | backend-go/internal/subtemplates/handler.go:157 |
| internal/subtemplates | DeleteTemplate | h *Handler | backend-go/internal/subtemplates/handler.go:206 |
| internal/subtemplates | ReorderTemplates | h *Handler | backend-go/internal/subtemplates/handler.go:212 |
| internal/subtemplates | GetTemplateTags | h *Handler | backend-go/internal/subtemplates/handler.go:246 |
| internal/subtemplates | SetTemplateTags | h *Handler | backend-go/internal/subtemplates/handler.go:270 |
| internal/subtemplates | formatSubpageConfigResponse |  | backend-go/internal/subtemplates/handler.go:293 |
| internal/subtemplates | GetAllConfigs | h *Handler | backend-go/internal/subtemplates/handler.go:313 |
| internal/subtemplates | GetConfigByUuid | h *Handler | backend-go/internal/subtemplates/handler.go:335 |
| internal/subtemplates | CreateConfig | h *Handler | backend-go/internal/subtemplates/handler.go:351 |
| internal/subtemplates | UpdateConfig | h *Handler | backend-go/internal/subtemplates/handler.go:396 |
| internal/subtemplates | subpageChanged |  | backend-go/internal/subtemplates/handler.go:442 |
| internal/subtemplates | DeleteConfig | h *Handler | backend-go/internal/subtemplates/handler.go:450 |
| internal/subtemplates | CloneConfig | h *Handler | backend-go/internal/subtemplates/handler.go:477 |
| internal/subtemplates | ReorderConfigs | h *Handler | backend-go/internal/subtemplates/handler.go:522 |
| internal/subtemplates | GetConfigTags | h *Handler | backend-go/internal/subtemplates/handler.go:556 |
| internal/subtemplates | SetConfigTags | h *Handler | backend-go/internal/subtemplates/handler.go:580 |
| internal/subtpl | cached |  | backend-go/internal/subtpl/crypto.go:17 |
| internal/subtpl | x25519PublicKey |  | backend-go/internal/subtpl/crypto.go:33 |
| internal/subtpl | mldsa65PublicKey |  | backend-go/internal/subtpl/crypto.go:44 |
| internal/subtpl | encryptionFromDecryption |  | backend-go/internal/subtpl/crypto.go:54 |
| internal/subtpl | stringAt |  | backend-go/internal/subtpl/crypto.go:120 |
| internal/subtpl | inboundKeys |  | backend-go/internal/subtpl/crypto.go:127 |
| internal/subtpl | NextTrafficResetAt |  | backend-go/internal/subtpl/export.go:6 |
| internal/subtpl | parseResolvedFromRemark |  | backend-go/internal/subtpl/fromobject.go:11 |
| internal/subtpl | optString |  | backend-go/internal/subtpl/fromobject.go:26 |
| internal/subtpl | num |  | backend-go/internal/subtpl/fromobject.go:28 |
| internal/subtpl | strList |  | backend-go/internal/subtpl/fromobject.go:33 |
| internal/subtpl | resolvedFromObject |  | backend-go/internal/subtpl/fromobject.go:44 |
| internal/subtpl | definedOrUndefined |  | backend-go/internal/subtpl/fromobject.go:117 |
| internal/subtpl | GenerateLinks |  | backend-go/internal/subtpl/gen_links.go:12 |
| internal/subtpl | LinkList |  | backend-go/internal/subtpl/gen_links.go:21 |
| internal/subtpl | contains |  | backend-go/internal/subtpl/gen_links.go:41 |
| internal/subtpl | buildShareLink |  | backend-go/internal/subtpl/gen_links.go:53 |
| internal/subtpl | setTruthy |  | backend-go/internal/subtpl/gen_links.go:108 |
| internal/subtpl | applyTransportParams |  | backend-go/internal/subtpl/gen_links.go:114 |
| internal/subtpl | joinOrEmpty |  | backend-go/internal/subtpl/gen_links.go:157 |
| internal/subtpl | applySecurityParams |  | backend-go/internal/subtpl/gen_links.go:167 |
| internal/subtpl | applyBase64Mapper |  | backend-go/internal/subtpl/gen_links.go:195 |
| internal/subtpl | sanitizeLink |  | backend-go/internal/subtpl/gen_links.go:222 |
| internal/subtpl | nullToEmpty |  | backend-go/internal/subtpl/gen_links.go:262 |
| internal/subtpl | jsNumber |  | backend-go/internal/subtpl/gen_links.go:270 |
| internal/subtpl | serializeLink |  | backend-go/internal/subtpl/gen_links.go:294 |
| internal/subtpl | applyFieldMap |  | backend-go/internal/subtpl/gen_mihomo.go:35 |
| internal/subtpl | GenerateMihomo |  | backend-go/internal/subtpl/gen_mihomo.go:51 |
| internal/subtpl | mihomoNode |  | backend-go/internal/subtpl/gen_mihomo.go:76 |
| internal/subtpl | clashType |  | backend-go/internal/subtpl/gen_mihomo.go:106 |
| internal/subtpl | clashNetwork |  | backend-go/internal/subtpl/gen_mihomo.go:113 |
| internal/subtpl | mihomoProtocolFields |  | backend-go/internal/subtpl/gen_mihomo.go:123 |
| internal/subtpl | clashSecurityFields |  | backend-go/internal/subtpl/gen_mihomo.go:145 |
| internal/subtpl | clashFingerprint |  | backend-go/internal/subtpl/gen_mihomo.go:182 |
| internal/subtpl | clashWSOpts |  | backend-go/internal/subtpl/gen_mihomo.go:196 |
| internal/subtpl | mihomoTransportOpts |  | backend-go/internal/subtpl/gen_mihomo.go:237 |
| internal/subtpl | nullStrOrEmpty |  | backend-go/internal/subtpl/gen_mihomo.go:258 |
| internal/subtpl | mihomoXhttpOpts |  | backend-go/internal/subtpl/gen_mihomo.go:265 |
| internal/subtpl | mihomoDownloadSettings |  | backend-go/internal/subtpl/gen_mihomo.go:295 |
| internal/subtpl | mihomoHysteria2 |  | backend-go/internal/subtpl/gen_mihomo.go:335 |
| internal/subtpl | findHysteria2Mask |  | backend-go/internal/subtpl/gen_mihomo.go:393 |
| internal/subtpl | GenerateClash |  | backend-go/internal/subtpl/gen_mihomo.go:425 |
| internal/subtpl | renderClashFamily |  | backend-go/internal/subtpl/gen_mihomo.go:465 |
| internal/subtpl | groupRemarks |  | backend-go/internal/subtpl/gen_mihomo.go:529 |
| internal/subtpl | GenerateSingbox |  | backend-go/internal/subtpl/gen_singbox.go:21 |
| internal/subtpl | singboxOutbound |  | backend-go/internal/subtpl/gen_singbox.go:34 |
| internal/subtpl | singboxProtocolFields |  | backend-go/internal/subtpl/gen_singbox.go:57 |
| internal/subtpl | parsePositiveInt |  | backend-go/internal/subtpl/gen_singbox.go:86 |
| internal/subtpl | jsParseInt |  | backend-go/internal/subtpl/gen_singbox.go:104 |
| internal/subtpl | singboxMultiplex |  | backend-go/internal/subtpl/gen_singbox.go:121 |
| internal/subtpl | singboxHysteria2 |  | backend-go/internal/subtpl/gen_singbox.go:152 |
| internal/subtpl | parseIntRange |  | backend-go/internal/subtpl/gen_singbox.go:182 |
| internal/subtpl | parsePortRanges |  | backend-go/internal/subtpl/gen_singbox.go:210 |
| internal/subtpl | parseDuration |  | backend-go/internal/subtpl/gen_singbox.go:229 |
| internal/subtpl | singboxTransport |  | backend-go/internal/subtpl/gen_singbox.go:243 |
| internal/subtpl | singboxWS |  | backend-go/internal/subtpl/gen_singbox.go:268 |
| internal/subtpl | singboxHeaders |  | backend-go/internal/subtpl/gen_singbox.go:291 |
| internal/subtpl | resolveFingerprint |  | backend-go/internal/subtpl/gen_singbox.go:312 |
| internal/subtpl | trimmedList |  | backend-go/internal/subtpl/gen_singbox.go:321 |
| internal/subtpl | singboxSecurity |  | backend-go/internal/subtpl/gen_singbox.go:329 |
| internal/subtpl | singboxQuicTLS |  | backend-go/internal/subtpl/gen_singbox.go:365 |
| internal/subtpl | renderSingbox |  | backend-go/internal/subtpl/gen_singbox.go:383 |
| internal/subtpl | GenerateXrayJSON |  | backend-go/internal/subtpl/gen_xray_json.go:19 |
| internal/subtpl | xrayMeta |  | backend-go/internal/subtpl/gen_xray_json.go:47 |
| internal/subtpl | buildXrayOutbound |  | backend-go/internal/subtpl/gen_xray_json.go:54 |
| internal/subtpl | xrayProtocolSettings |  | backend-go/internal/subtpl/gen_xray_json.go:70 |
| internal/subtpl | spreadHeaders |  | backend-go/internal/subtpl/gen_xray_json.go:92 |
| internal/subtpl | xrayStreamSettings |  | backend-go/internal/subtpl/gen_xray_json.go:100 |
| internal/subtpl | splitAny |  | backend-go/internal/subtpl/gen_xray_json.go:175 |
| internal/subtpl | buildTaggedOutbounds |  | backend-go/internal/subtpl/gen_xray_json.go:187 |
| internal/subtpl | resolveInjectedHosts |  | backend-go/internal/subtpl/gen_xray_json.go:218 |
| internal/subtpl | sharesTag |  | backend-go/internal/subtpl/gen_xray_json.go:282 |
| internal/subtpl | applyTemplateInjector |  | backend-go/internal/subtpl/gen_xray_json.go:291 |
| internal/subtpl/js | EncodeURIComponent |  | backend-go/internal/subtpl/js/js.go:16 |
| internal/subtpl/js | Base64 |  | backend-go/internal/subtpl/js/js.go:31 |
| internal/subtpl/js | Base64Bytes |  | backend-go/internal/subtpl/js/js.go:34 |
| internal/subtpl/js | Base64URL |  | backend-go/internal/subtpl/js/js.go:37 |
| internal/subtpl/js | DecodeBase64 |  | backend-go/internal/subtpl/js/js.go:41 |
| internal/subtpl/js | DecodeBase64String |  | backend-go/internal/subtpl/js/js.go:70 |
| internal/subtpl/js | PrettyBytes |  | backend-go/internal/subtpl/js/js.go:76 |
| internal/subtpl/js | DayjsFormat |  | backend-go/internal/subtpl/js/js.go:98 |
| internal/subtpl/js | dayjsToken |  | backend-go/internal/subtpl/js/js.go:131 |
| internal/subtpl/js | ISOString |  | backend-go/internal/subtpl/js/js.go:198 |
| internal/subtpl | isAllowedHostPath |  | backend-go/internal/subtpl/mapper.go:19 |
| internal/subtpl | isBlockedByPrimitive |  | backend-go/internal/subtpl/mapper.go:38 |
| internal/subtpl | applyHostMapper |  | backend-go/internal/subtpl/mapper.go:56 |
| internal/subtpl | str |  | backend-go/internal/subtpl/model.go:222 |
| internal/subtpl | objOrNull |  | backend-go/internal/subtpl/model.go:229 |
| internal/subtpl | intOrNull |  | backend-go/internal/subtpl/model.go:236 |
| internal/subtpl | strings2any |  | backend-go/internal/subtpl/model.go:243 |
| internal/subtpl | Object | r *Resolved | backend-go/internal/subtpl/model.go:253 |
| internal/subtpl | mapperOps | r *Resolved | backend-go/internal/subtpl/model.go:349 |
| internal/subtpl/ojson | New |  | backend-go/internal/subtpl/ojson/ojson.go:32 |
| internal/subtpl/ojson | init | o *Object | backend-go/internal/subtpl/ojson/ojson.go:40 |
| internal/subtpl/ojson | Set | o *Object | backend-go/internal/subtpl/ojson/ojson.go:47 |
| internal/subtpl/ojson | Get | o *Object | backend-go/internal/subtpl/ojson/ojson.go:57 |
| internal/subtpl/ojson | Value | o *Object | backend-go/internal/subtpl/ojson/ojson.go:66 |
| internal/subtpl/ojson | Has | o *Object | backend-go/internal/subtpl/ojson/ojson.go:72 |
| internal/subtpl/ojson | Delete | o *Object | backend-go/internal/subtpl/ojson/ojson.go:78 |
| internal/subtpl/ojson | Keys | o *Object | backend-go/internal/subtpl/ojson/ojson.go:93 |
| internal/subtpl/ojson | Len | o *Object | backend-go/internal/subtpl/ojson/ojson.go:101 |
| internal/subtpl/ojson | Spread | o *Object | backend-go/internal/subtpl/ojson/ojson.go:109 |
| internal/subtpl/ojson | Clone |  | backend-go/internal/subtpl/ojson/ojson.go:120 |
| internal/subtpl/ojson | Parse |  | backend-go/internal/subtpl/ojson/ojson.go:142 |
| internal/subtpl/ojson | MustParse |  | backend-go/internal/subtpl/ojson/ojson.go:156 |
| internal/subtpl/ojson | parseValue |  | backend-go/internal/subtpl/ojson/ojson.go:164 |
| internal/subtpl/ojson | FromGo |  | backend-go/internal/subtpl/ojson/ojson.go:207 |
| internal/subtpl/ojson | Stringify |  | backend-go/internal/subtpl/ojson/ojson.go:217 |
| internal/subtpl/ojson | MarshalJSON | o *Object | backend-go/internal/subtpl/ojson/ojson.go:224 |
| internal/subtpl/ojson | StringifyIndent |  | backend-go/internal/subtpl/ojson/ojson.go:232 |
| internal/subtpl/ojson | FormatNumber |  | backend-go/internal/subtpl/ojson/ojson.go:239 |
| internal/subtpl/ojson | writeValue |  | backend-go/internal/subtpl/ojson/ojson.go:258 |
| internal/subtpl/ojson | writeString |  | backend-go/internal/subtpl/ojson/ojson.go:351 |
| internal/subtpl/ojson | IsNonEmptyObject |  | backend-go/internal/subtpl/ojson/ojson.go:383 |
| internal/subtpl/ojson | Truthy |  | backend-go/internal/subtpl/ojson/ojson.go:389 |
| internal/subtpl/ojson | ToPath |  | backend-go/internal/subtpl/ojson/path.go:16 |
| internal/subtpl/ojson | Get |  | backend-go/internal/subtpl/ojson/path.go:38 |
| internal/subtpl/ojson | isObjectLike |  | backend-go/internal/subtpl/ojson/path.go:77 |
| internal/subtpl/ojson | Set |  | backend-go/internal/subtpl/ojson/path.go:88 |
| internal/subtpl/ojson | setIn |  | backend-go/internal/subtpl/ojson/path.go:96 |
| internal/subtpl/ojson | Unset |  | backend-go/internal/subtpl/ojson/path.go:134 |
| internal/subtpl | Render |  | backend-go/internal/subtpl/render.go:32 |
| internal/subtpl | resolveRandomizedValue |  | backend-go/internal/subtpl/resolve.go:39 |
| internal/subtpl | override |  | backend-go/internal/subtpl/resolve.go:58 |
| internal/subtpl | ptrAny |  | backend-go/internal/subtpl/resolve.go:68 |
| internal/subtpl | asStringPtr |  | backend-go/internal/subtpl/resolve.go:75 |
| internal/subtpl | asString |  | backend-go/internal/subtpl/resolve.go:82 |
| internal/subtpl | toNonEmptyRecord |  | backend-go/internal/subtpl/resolve.go:89 |
| internal/subtpl | get |  | backend-go/internal/subtpl/resolve.go:96 |
| internal/subtpl | getDefined |  | backend-go/internal/subtpl/resolve.go:104 |
| internal/subtpl | ResolveProxyConfig |  | backend-go/internal/subtpl/resolve.go:109 |
| internal/subtpl | earlyExitRemarks |  | backend-go/internal/subtpl/resolve.go:159 |
| internal/subtpl | nonNil |  | backend-go/internal/subtpl/resolve.go:190 |
| internal/subtpl | applyShuffle |  | backend-go/internal/subtpl/resolve.go:197 |
| internal/subtpl | applyHostOverrides |  | backend-go/internal/subtpl/resolve.go:221 |
| internal/subtpl | deduplicateRemark |  | backend-go/internal/subtpl/resolve.go:233 |
| internal/subtpl | itoa |  | backend-go/internal/subtpl/resolve.go:246 |
| internal/subtpl | setVlessRouteForUuid |  | backend-go/internal/subtpl/resolve.go:251 |
| internal/subtpl | getVlessFlow |  | backend-go/internal/subtpl/resolve.go:259 |
| internal/subtpl | resolveProtocol |  | backend-go/internal/subtpl/resolve.go:283 |
| internal/subtpl | jsString |  | backend-go/internal/subtpl/resolve.go:327 |
| internal/subtpl | resolveTransport |  | backend-go/internal/subtpl/resolve.go:354 |
| internal/subtpl | nullish |  | backend-go/internal/subtpl/resolve.go:415 |
| internal/subtpl | nullishString |  | backend-go/internal/subtpl/resolve.go:422 |
| internal/subtpl | firstTruthy |  | backend-go/internal/subtpl/resolve.go:429 |
| internal/subtpl | resolveTCP |  | backend-go/internal/subtpl/resolve.go:438 |
| internal/subtpl | resolveFinalServerName |  | backend-go/internal/subtpl/resolve.go:469 |
| internal/subtpl | resolveSecurity |  | backend-go/internal/subtpl/resolve.go:489 |
| internal/subtpl | rawServerName |  | backend-go/internal/subtpl/resolve.go:555 |
| internal/subtpl | orNull |  | backend-go/internal/subtpl/resolve.go:562 |
| internal/subtpl | buildResolved |  | backend-go/internal/subtpl/resolve.go:569 |
| internal/subtpl | createFallbackHosts |  | backend-go/internal/subtpl/resolve.go:611 |
| internal/subtpl | TemplateValues |  | backend-go/internal/subtpl/template.go:23 |
| internal/subtpl | ReplaceTemplate |  | backend-go/internal/subtpl/template.go:123 |
| internal/subtpl | nextTrafficResetAt |  | backend-go/internal/subtpl/template.go:150 |
| internal/subtpl | addMonths |  | backend-go/internal/subtpl/template.go:195 |
| internal/subtpl | LoadYAML |  | backend-go/internal/subtpl/yaml.go:16 |
| internal/subtpl | yamlValue |  | backend-go/internal/subtpl/yaml.go:27 |
| internal/subtpl | yamlMerge |  | backend-go/internal/subtpl/yaml.go:73 |
| internal/subtpl | yamlScalar |  | backend-go/internal/subtpl/yaml.go:100 |
| internal/subtpl | DumpYAML |  | backend-go/internal/subtpl/yaml_dump.go:19 |
| internal/subtpl | buildYAML |  | backend-go/internal/subtpl/yaml_dump.go:57 |
| internal/subtpl | yamlNumber |  | backend-go/internal/subtpl/yaml_dump.go:98 |
| internal/subtpl | nextLine |  | backend-go/internal/subtpl/yaml_dump.go:131 |
| internal/subtpl | writeNode | d *yamlDumper | backend-go/internal/subtpl/yaml_dump.go:135 |
| internal/subtpl | writeFlowSequence | d *yamlDumper | backend-go/internal/subtpl/yaml_dump.go:173 |
| internal/subtpl | writeBlockSequence | d *yamlDumper | backend-go/internal/subtpl/yaml_dump.go:181 |
| internal/subtpl | writeFlowMapping | d *yamlDumper | backend-go/internal/subtpl/yaml_dump.go:198 |
| internal/subtpl | writeBlockMapping | d *yamlDumper | backend-go/internal/subtpl/yaml_dump.go:215 |
| internal/subtpl | newScalarLayout |  | backend-go/internal/subtpl/yaml_dump.go:256 |
| internal/subtpl | allows | l *scalarLayout | backend-go/internal/subtpl/yaml_dump.go:277 |
| internal/subtpl | canUsePlain | l *scalarLayout | backend-go/internal/subtpl/yaml_dump.go:288 |
| internal/subtpl | canUseSingle | l *scalarLayout | backend-go/internal/subtpl/yaml_dump.go:305 |
| internal/subtpl | canUseBlock | l *scalarLayout | backend-go/internal/subtpl/yaml_dump.go:318 |
| internal/subtpl | isJSWhitespace |  | backend-go/internal/subtpl/yaml_dump.go:334 |
| internal/subtpl | availableWidth | l *scalarLayout | backend-go/internal/subtpl/yaml_dump.go:342 |
| internal/subtpl | applyRules | l *scalarLayout | backend-go/internal/subtpl/yaml_dump.go:347 |
| internal/subtpl | render | l *scalarLayout | backend-go/internal/subtpl/yaml_dump.go:387 |
| internal/subtpl | encodeFlowBreaks |  | backend-go/internal/subtpl/yaml_dump.go:404 |
| internal/subtpl | indentLines |  | backend-go/internal/subtpl/yaml_dump.go:417 |
| internal/subtpl | blockHeader |  | backend-go/internal/subtpl/yaml_dump.go:434 |
| internal/subtpl | dropEndingNewline |  | backend-go/internal/subtpl/yaml_dump.go:450 |
| internal/subtpl | isMoreIndented |  | backend-go/internal/subtpl/yaml_dump.go:454 |
| internal/subtpl | foldLine |  | backend-go/internal/subtpl/yaml_dump.go:457 |
| internal/subtpl | foldBlockScalar |  | backend-go/internal/subtpl/yaml_dump.go:487 |
| internal/subtpl | escapeYAMLString |  | backend-go/internal/subtpl/yaml_dump.go:521 |
| internal/subtpl | escapeYAMLRune |  | backend-go/internal/subtpl/yaml_dump.go:538 |
| internal/subtpl | utf16Len |  | backend-go/internal/subtpl/yaml_dump.go:574 |
| internal/subtpl | isPrintable |  | backend-go/internal/subtpl/yaml_dump.go:587 |
| internal/subtpl | isNsChar |  | backend-go/internal/subtpl/yaml_dump.go:593 |
| internal/subtpl | isIndicator |  | backend-go/internal/subtpl/yaml_dump.go:597 |
| internal/subtpl | plainScalar |  | backend-go/internal/subtpl/yaml_dump.go:603 |
| internal/subtpl | jsParseFloat |  | backend-go/internal/subtpl/yaml_dump.go:696 |
| internal/subtpl | finite |  | backend-go/internal/subtpl/yaml_dump.go:708 |
| internal/subtpl | resolvesInt |  | backend-go/internal/subtpl/yaml_dump.go:710 |
| internal/subtpl | resolvesFloat |  | backend-go/internal/subtpl/yaml_dump.go:731 |
| internal/subtpl | resolvesTimestamp |  | backend-go/internal/subtpl/yaml_dump.go:751 |
| internal/subtpl | implicitTag |  | backend-go/internal/subtpl/yaml_dump.go:780 |
| internal/system | CurrentChannel |  | backend-go/internal/system/channel.go:32 |
| internal/system | validChannel |  | backend-go/internal/system/channel.go:39 |
| internal/system | releaseDownloadBase |  | backend-go/internal/system/channel.go:43 |
| internal/system | releaseAPIURL |  | backend-go/internal/system/channel.go:50 |
| internal/system | dockerTag |  | backend-go/internal/system/channel.go:57 |
| internal/system | readRequestedChannel |  | backend-go/internal/system/channel.go:68 |
| internal/system | parseChannel |  | backend-go/internal/system/channel.go:87 |
| internal/system | NewHandler |  | backend-go/internal/system/handler.go:41 |
| internal/system | formatPrettyBytes |  | backend-go/internal/system/handler.go:149 |
| internal/system | calcBaseStat |  | backend-go/internal/system/handler.go:177 |
| internal/system | GetMetadata | h *Handler | backend-go/internal/system/handler.go:190 |
| internal/system | formatSubscriptionSettings |  | backend-go/internal/system/handler.go:208 |
| internal/system | GetSubscriptionSettings | h *Handler | backend-go/internal/system/handler.go:246 |
| internal/system | UpdateSubscriptionSettings | h *Handler | backend-go/internal/system/handler.go:254 |
| internal/system | GetHttpStats | h *Handler | backend-go/internal/system/handler.go:311 |
| internal/system | GetHealth | h *Handler | backend-go/internal/system/handler.go:322 |
| internal/system | GetStats | h *Handler | backend-go/internal/system/handler.go:326 |
| internal/system | computeStats | h *Handler | backend-go/internal/system/handler.go:338 |
| internal/system | GetBandwidthStats | h *Handler | backend-go/internal/system/handler.go:406 |
| internal/system | GetNodesStatistics | h *Handler | backend-go/internal/system/handler.go:473 |
| internal/system | GetRecap | h *Handler | backend-go/internal/system/handler.go:513 |
| internal/system | GetSettings | h *Handler | backend-go/internal/system/handler.go:573 |
| internal/system | UpdateSettings | h *Handler | backend-go/internal/system/handler.go:679 |
| internal/system | RestoreBackup | h *Handler | backend-go/internal/system/handler.go:733 |
| internal/system | hostMemory |  | backend-go/internal/system/host_memory.go:14 |
| internal/system | readProcMeminfo |  | backend-go/internal/system/host_memory.go:24 |
| internal/system | add | t *trafficByTag | backend-go/internal/system/nodes_metrics.go:21 |
| internal/system | stats | t *trafficByTag | backend-go/internal/system/nodes_metrics.go:37 |
| internal/system | GetNodesMetrics | h *Handler | backend-go/internal/system/nodes_metrics.go:51 |
| internal/system | NewBackupRestoreService |  | backend-go/internal/system/restore.go:27 |
| internal/system | RestoreFromTarGz | s *BackupRestoreService | backend-go/internal/system/restore.go:31 |
| internal/system | restoreSqlGz | s *BackupRestoreService | backend-go/internal/system/restore.go:64 |
| internal/system | parseDumpTime |  | backend-go/internal/system/restore.go:207 |
| internal/system | consumePostgresCopyDump |  | backend-go/internal/system/restore.go:216 |
| internal/system | parseCopyHeader |  | backend-go/internal/system/restore.go:329 |
| internal/system | unquoteCopyIdentifier |  | backend-go/internal/system/restore.go:363 |
| internal/system | decodePostgresCopyField |  | backend-go/internal/system/restore.go:371 |
| internal/system | isHexDigit |  | backend-go/internal/system/restore.go:437 |
| internal/system | Inc | rc *RouteCounter | backend-go/internal/system/route_counter.go:21 |
| internal/system | GetStats | rc *RouteCounter | backend-go/internal/system/route_counter.go:32 |
| internal/system | RouteCounterMiddleware |  | backend-go/internal/system/route_counter.go:52 |
| internal/system | ApplyRelease |  | backend-go/internal/system/selfupdate.go:34 |
| internal/system | trustedExecutable |  | backend-go/internal/system/selfupdate.go:96 |
| internal/system | rootOnlyWritable |  | backend-go/internal/system/selfupdate.go:119 |
| internal/system | download |  | backend-go/internal/system/selfupdate.go:134 |
| internal/system | readChecksums |  | backend-go/internal/system/selfupdate.go:158 |
| internal/system | verifyChecksum |  | backend-go/internal/system/selfupdate.go:175 |
| internal/system | installFrontend |  | backend-go/internal/system/selfupdate.go:195 |
| internal/system | extractTarGz |  | backend-go/internal/system/selfupdate.go:226 |
| internal/system | installBinary |  | backend-go/internal/system/selfupdate.go:286 |
| internal/system | NewTools |  | backend-go/internal/system/tools.go:24 |
| internal/system | Register | t *Tools | backend-go/internal/system/tools.go:25 |
| internal/system | authenticate | t *Tools | backend-go/internal/system/tools.go:36 |
| internal/system | claims | t *Tools | backend-go/internal/system/tools.go:89 |
| internal/system | queues | t *Tools | backend-go/internal/system/tools.go:133 |
| internal/system | retry | t *Tools | backend-go/internal/system/tools.go:173 |
| internal/system | cancel | t *Tools | backend-go/internal/system/tools.go:178 |
| internal/system | transition | t *Tools | backend-go/internal/system/tools.go:182 |
| internal/system | docs | t *Tools | backend-go/internal/system/tools.go:213 |
| internal/system | openapi | t *Tools | backend-go/internal/system/tools.go:223 |
| internal/system | fetchRelease |  | backend-go/internal/system/updates.go:38 |
| internal/system | releaseVersion |  | backend-go/internal/system/updates.go:61 |
| internal/system | IsRunningInDocker |  | backend-go/internal/system/updates.go:69 |
| internal/system | CheckUpdate | h *Handler | backend-go/internal/system/updates.go:87 |
| internal/system | DockerUpdateCommand |  | backend-go/internal/system/updates.go:125 |
| internal/system | installerCommand |  | backend-go/internal/system/updates.go:142 |
| internal/system | updateHelperInstalled |  | backend-go/internal/system/updates.go:156 |
| internal/system | ApplyUpdate | h *Handler | backend-go/internal/system/updates.go:161 |
| internal/testdb | Open |  | backend-go/internal/testdb/testdb.go:22 |
| internal/tokens | NewHandler |  | backend-go/internal/tokens/handler.go:26 |
| internal/tokens | GetScopes | h *Handler | backend-go/internal/tokens/handler.go:52 |
| internal/tokens | GetApiTokens | h *Handler | backend-go/internal/tokens/handler.go:57 |
| internal/tokens | tokenEvent |  | backend-go/internal/tokens/handler.go:90 |
| internal/tokens | CreateApiToken | h *Handler | backend-go/internal/tokens/handler.go:97 |
| internal/tokens | DeleteApiToken | h *Handler | backend-go/internal/tokens/handler.go:163 |
| internal/tokens | GetOtt | h *Handler | backend-go/internal/tokens/handler.go:185 |
| internal/users | SetSubPublicDomain |  | backend-go/internal/users/events.go:15 |
| internal/users | eventData |  | backend-go/internal/users/events.go:35 |
| internal/users | loadRelations |  | backend-go/internal/users/events.go:44 |
| internal/users | emitLoaded |  | backend-go/internal/users/events.go:56 |
| internal/users | emitUser |  | backend-go/internal/users/events.go:60 |
| internal/users | EmitHwidDevice |  | backend-go/internal/users/events.go:76 |
| internal/users | SetStatusFor | s *Service | backend-go/internal/users/events.go:88 |
| internal/users | EmitForUsers |  | backend-go/internal/users/events.go:106 |
| internal/users | EventData |  | backend-go/internal/users/events.go:136 |
| internal/users | NewHandler |  | backend-go/internal/users/handler.go:25 |
| internal/users | FormatUser |  | backend-go/internal/users/handler.go:43 |
| internal/users | GetUsers | h *Handler | backend-go/internal/users/handler.go:137 |
| internal/users | GetTags | h *Handler | backend-go/internal/users/handler.go:181 |
| internal/users | CreateUser | h *Handler | backend-go/internal/users/handler.go:196 |
| internal/users | GetUser | h *Handler | backend-go/internal/users/handler.go:215 |
| internal/users | UpdateUser | h *Handler | backend-go/internal/users/handler.go:237 |
| internal/users | DeleteUser | h *Handler | backend-go/internal/users/handler.go:268 |
| internal/users | ResetTraffic | h *Handler | backend-go/internal/users/handler.go:287 |
| internal/users | EnableUser | h *Handler | backend-go/internal/users/handler.go:313 |
| internal/users | DisableUser | h *Handler | backend-go/internal/users/handler.go:317 |
| internal/users | setEnabled | h *Handler | backend-go/internal/users/handler.go:321 |
| internal/users | ExtendUser | h *Handler | backend-go/internal/users/handler.go:357 |
| internal/users | RevokeUser | h *Handler | backend-go/internal/users/handler.go:378 |
| internal/users | GetUserByShortUuid | h *Handler | backend-go/internal/users/handler.go:403 |
| internal/users | GetUserByUsername | h *Handler | backend-go/internal/users/handler.go:417 |
| internal/users | ResolveUser | h *Handler | backend-go/internal/users/handler.go:432 |
| internal/users | GetUsersStream | h *Handler | backend-go/internal/users/handler.go:450 |
| internal/users | GetUserAccessibleNodes | h *Handler | backend-go/internal/users/handler.go:500 |
| internal/users | GetUserSubscriptionRequestHistory | h *Handler | backend-go/internal/users/handler.go:551 |
| internal/users | BulkExtendExpirationDate | h *Handler | backend-go/internal/users/handler.go:599 |
| internal/users | BulkAllExtendExpirationDate | h *Handler | backend-go/internal/users/handler.go:616 |
| internal/users | BulkUpdate | h *Handler | backend-go/internal/users/handler.go:632 |
| internal/users | BulkAllUpdate | h *Handler | backend-go/internal/users/handler.go:649 |
| internal/users | BulkResetTraffic | h *Handler | backend-go/internal/users/handler.go:664 |
| internal/users | BulkAllResetTraffic | h *Handler | backend-go/internal/users/handler.go:680 |
| internal/users | BulkRevokeSubscription | h *Handler | backend-go/internal/users/handler.go:689 |
| internal/users | BulkDelete | h *Handler | backend-go/internal/users/handler.go:705 |
| internal/users | BulkDeleteByStatus | h *Handler | backend-go/internal/users/handler.go:721 |
| internal/users | BulkUpdateSquads | h *Handler | backend-go/internal/users/handler.go:737 |
| internal/users | BulkUserAction | h *Handler | backend-go/internal/users/handler.go:754 |
| internal/users | PatchUser | h *Handler | backend-go/internal/users/handler.go:763 |
| internal/users | mutate | s *Service | backend-go/internal/users/lifecycle.go:21 |
| internal/users | mutateNotify | s *Service | backend-go/internal/users/lifecycle.go:25 |
| internal/users | byIDs |  | backend-go/internal/users/lifecycle.go:102 |
| internal/users | allUsers |  | backend-go/internal/users/lifecycle.go:105 |
| internal/users | deleteUser |  | backend-go/internal/users/lifecycle.go:107 |
| internal/users | Delete | s *Service | backend-go/internal/users/lifecycle.go:116 |
| internal/users | BulkDelete | s *Service | backend-go/internal/users/lifecycle.go:119 |
| internal/users | BulkDeleteByStatus | s *Service | backend-go/internal/users/lifecycle.go:122 |
| internal/users | resetUserTraffic |  | backend-go/internal/users/lifecycle.go:129 |
| internal/users | ResetTraffic | s *Service | backend-go/internal/users/lifecycle.go:145 |
| internal/users | BulkResetTraffic | s *Service | backend-go/internal/users/lifecycle.go:148 |
| internal/users | BulkAllResetTraffic | s *Service | backend-go/internal/users/lifecycle.go:151 |
| internal/users | SetStatus | s *Service | backend-go/internal/users/lifecycle.go:152 |
| internal/users | Enable | s *Service | backend-go/internal/users/lifecycle.go:165 |
| internal/users | Disable | s *Service | backend-go/internal/users/lifecycle.go:176 |
| internal/users | validStatus |  | backend-go/internal/users/lifecycle.go:186 |
| internal/users | extendMutation |  | backend-go/internal/users/lifecycle.go:190 |
| internal/users | validDays |  | backend-go/internal/users/lifecycle.go:206 |
| internal/users | Extend | s *Service | backend-go/internal/users/lifecycle.go:212 |
| internal/users | BulkExtendExpirationDate | s *Service | backend-go/internal/users/lifecycle.go:221 |
| internal/users | BulkAllExtendExpirationDate | s *Service | backend-go/internal/users/lifecycle.go:227 |
| internal/users | updateMany | s *Service | backend-go/internal/users/lifecycle.go:234 |
| internal/users | BulkUpdate | s *Service | backend-go/internal/users/lifecycle.go:265 |
| internal/users | BulkAllUpdate | s *Service | backend-go/internal/users/lifecycle.go:268 |
| internal/users | BulkUpdateSquads | s *Service | backend-go/internal/users/lifecycle.go:271 |
| internal/users | revokeMutation |  | backend-go/internal/users/lifecycle.go:275 |
| internal/users | Revoke | s *Service | backend-go/internal/users/lifecycle.go:292 |
| internal/users | BulkRevokeSubscription | s *Service | backend-go/internal/users/lifecycle.go:301 |
| internal/users | NewService |  | backend-go/internal/users/service.go:29 |
| internal/users | SetSyncer | s *Service | backend-go/internal/users/service.go:37 |
| internal/users | GenerateShortUUID |  | backend-go/internal/users/service.go:43 |
| internal/users | GenerateRandomPassword |  | backend-go/internal/users/service.go:56 |
| internal/users | SetShortUUIDLength |  | backend-go/internal/users/service.go:64 |
| internal/users | NewShortUUID |  | backend-go/internal/users/service.go:72 |
| internal/users | NewPassword |  | backend-go/internal/users/service.go:75 |
| internal/users | loadSquadsForUsers | s *Service | backend-go/internal/users/service.go:102 |
| internal/users | loadSquads |  | backend-go/internal/users/service.go:106 |
| internal/users | Create | s *Service | backend-go/internal/users/service.go:142 |
| internal/users | GetAll | s *Service | backend-go/internal/users/service.go:254 |
| internal/users | GetStream | s *Service | backend-go/internal/users/service.go:420 |
| internal/users | GetTags | s *Service | backend-go/internal/users/service.go:474 |
| internal/users | GetByID | s *Service | backend-go/internal/users/service.go:489 |
| internal/users | GetByShortUUID | s *Service | backend-go/internal/users/service.go:499 |
| internal/users | GetByUsername | s *Service | backend-go/internal/users/service.go:509 |
| internal/users | normalizeUserFields |  | backend-go/internal/users/service.go:519 |
| internal/users | Update | s *Service | backend-go/internal/users/service.go:583 |
| internal/users | Resolve | s *Service | backend-go/internal/users/service.go:644 |
| internal/users | AccessibleNodes | s *Service | backend-go/internal/users/service.go:673 |
| . | main |  | backend-go/main.go:5 |
