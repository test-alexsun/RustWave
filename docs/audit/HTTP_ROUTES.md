# HTTP / WebSocket route inventory

Source: `d709bad01dc0ceacb20012a3afdf528eddfd061f`.

248 explicit main-listener method/path operations; includes WS upgrade GET and 2 HEAD. Static GET/HEAD wildcard and metrics listener GET /metrics, GET /health are counted separately. CORS preflight is middleware, not an extra registered operation. No Rust implementation.

| ID | Method | Path | Handler | Registration | Authentication |
| --- | --- | --- | --- | --- | --- |
| API-001 | POST | /api/auth/login | authHandler.Login | backend-go/internal/server/server.go:317 | public (handler checks); SSH uses ticket + protocol |
| API-002 | POST | /api/auth/oauth2/authorize | stubHandler.OAuth2Authorize | backend-go/internal/server/server.go:322 | public (handler checks); SSH uses ticket + protocol |
| API-003 | POST | /api/auth/oauth2/callback | stubHandler.OAuth2Callback | backend-go/internal/server/server.go:323 | public (handler checks); SSH uses ticket + protocol |
| API-004 | POST | /api/auth/oauth2/tg/callback | stubHandler.OAuth2TelegramCallback | backend-go/internal/server/server.go:324 | public (handler checks); SSH uses ticket + protocol |
| API-005 | GET | /api/auth/passkey/authentication/options | stubHandler.GetPasskeyAuthOptions | backend-go/internal/server/server.go:320 | public (handler checks); SSH uses ticket + protocol |
| API-006 | POST | /api/auth/passkey/authentication/verify | stubHandler.VerifyPasskeyAuth | backend-go/internal/server/server.go:321 | public (handler checks); SSH uses ticket + protocol |
| API-007 | POST | /api/auth/register | authHandler.Register | backend-go/internal/server/server.go:318 | public (handler checks); SSH uses ticket + protocol |
| API-008 | GET | /api/auth/status | authHandler.GetStatus | backend-go/internal/server/server.go:315 | public (handler checks); SSH uses ticket + protocol |
| API-009 | HEAD | /api/auth/status | authHandler.GetStatus | backend-go/internal/server/server.go:316 | public (handler checks); SSH uses ticket + protocol |
| API-010 | GET | /api/backend-tools/openapi.json | t.openapi | backend-go/internal/system/tools.go:33 | OTT -> rw-tools cookie; admin + same-origin mutation |
| API-011 | GET | /api/backend-tools/queues | t.queues | backend-go/internal/system/tools.go:28 | OTT -> rw-tools cookie; admin + same-origin mutation |
| API-012 | POST | /api/backend-tools/queues/{id}/cancel | t.cancel | backend-go/internal/system/tools.go:30 | OTT -> rw-tools cookie; admin + same-origin mutation |
| API-013 | POST | /api/backend-tools/queues/{id}/retry | t.retry | backend-go/internal/system/tools.go:29 | OTT -> rw-tools cookie; admin + same-origin mutation |
| API-014 | GET | /api/backend-tools/scalar | t.docs | backend-go/internal/system/tools.go:32 | OTT -> rw-tools cookie; admin + same-origin mutation |
| API-015 | GET | /api/backend-tools/swagger | t.docs | backend-go/internal/system/tools.go:31 | OTT -> rw-tools cookie; admin + same-origin mutation |
| API-016 | GET | /api/bandwidth-stats/internal-squads/{squadUuid}/users/{userId}/usage | s.GetBandwidthSquadUserUsage | backend-go/internal/stubs/stubs.go:213 | Bearer JWT/API token + scopes/AdminOnly |
| API-017 | GET | /api/bandwidth-stats/internal-squads/{uuid}/usage | s.GetBandwidthSquadUsage | backend-go/internal/stubs/stubs.go:212 | Bearer JWT/API token + scopes/AdminOnly |
| API-018 | GET | /api/bandwidth-stats/nodes | s.GetBandwidthStatsNodes | backend-go/internal/stubs/stubs.go:211 | Bearer JWT/API token + scopes/AdminOnly |
| API-019 | POST | /api/bandwidth-stats/nodes/usage | s.GetBandwidthNodesUsage | backend-go/internal/stubs/stubs.go:207 | Bearer JWT/API token + scopes/AdminOnly |
| API-020 | POST | /api/bandwidth-stats/nodes/users | s.GetBandwidthStatsNodeUsers | backend-go/internal/stubs/stubs.go:208 | Bearer JWT/API token + scopes/AdminOnly |
| API-021 | GET | /api/bandwidth-stats/nodes/{uuid}/users | s.GetBandwidthStatsNodeUsers | backend-go/internal/stubs/stubs.go:209 | Bearer JWT/API token + scopes/AdminOnly |
| API-022 | GET | /api/bandwidth-stats/users/{userId} | s.GetBandwidthStatsUsers | backend-go/internal/stubs/stubs.go:210 | Bearer JWT/API token + scopes/AdminOnly |
| API-023 | GET | /api/config-profiles | cpHandler.GetProfiles | backend-go/internal/server/server.go:431 | Bearer JWT/API token + scopes/AdminOnly |
| API-024 | PATCH | /api/config-profiles | cpHandler.UpdateConfigProfile | backend-go/internal/server/server.go:434 | Bearer JWT/API token + scopes/AdminOnly |
| API-025 | POST | /api/config-profiles | cpHandler.CreateConfigProfile | backend-go/internal/server/server.go:432 | Bearer JWT/API token + scopes/AdminOnly |
| API-026 | POST | /api/config-profiles/actions/reorder | cpHandler.ReorderConfigProfiles | backend-go/internal/server/server.go:437 | Bearer JWT/API token + scopes/AdminOnly |
| API-027 | GET | /api/config-profiles/inbounds | cpHandler.GetAllInbounds | backend-go/internal/server/server.go:430 | Bearer JWT/API token + scopes/AdminOnly |
| API-028 | GET | /api/config-profiles/tags | cpHandler.GetConfigProfilesTags | backend-go/internal/server/server.go:428 | Bearer JWT/API token + scopes/AdminOnly |
| API-029 | PATCH | /api/config-profiles/tags | cpHandler.SetConfigProfilesTags | backend-go/internal/server/server.go:429 | Bearer JWT/API token + scopes/AdminOnly |
| API-030 | DELETE | /api/config-profiles/{uuid} | cpHandler.DeleteConfigProfile | backend-go/internal/server/server.go:436 | Bearer JWT/API token + scopes/AdminOnly |
| API-031 | GET | /api/config-profiles/{uuid} | cpHandler.GetConfigProfile | backend-go/internal/server/server.go:433 | Bearer JWT/API token + scopes/AdminOnly |
| API-032 | PATCH | /api/config-profiles/{uuid} | cpHandler.UpdateConfigProfile | backend-go/internal/server/server.go:435 | Bearer JWT/API token + scopes/AdminOnly |
| API-033 | GET | /api/config-profiles/{uuid}/computed-config | cpHandler.GetComputedConfig | backend-go/internal/server/server.go:439 | Bearer JWT/API token + scopes/AdminOnly |
| API-034 | GET | /api/config-profiles/{uuid}/inbounds | cpHandler.GetProfileInbounds | backend-go/internal/server/server.go:438 | Bearer JWT/API token + scopes/AdminOnly |
| API-035 | GET | /api/connections/by-node/{jobId} | s.ConnectionsByNodeResult | backend-go/internal/stubs/stubs.go:186 | Bearer JWT/API token + scopes/AdminOnly |
| API-036 | POST | /api/connections/by-node/{nodeUuid} | s.ConnectionsByNode | backend-go/internal/stubs/stubs.go:185 | Bearer JWT/API token + scopes/AdminOnly |
| API-037 | GET | /api/connections/by-user/{jobId} | s.ConnectionsByUserResult | backend-go/internal/stubs/stubs.go:184 | Bearer JWT/API token + scopes/AdminOnly |
| API-038 | POST | /api/connections/by-user/{userId} | s.ConnectionsByUser | backend-go/internal/stubs/stubs.go:183 | Bearer JWT/API token + scopes/AdminOnly |
| API-039 | POST | /api/connections/drop | s.DropConnections | backend-go/internal/stubs/stubs.go:189 | Bearer JWT/API token + scopes/AdminOnly |
| API-040 | GET | /api/connections/geocheck/{jobId} | s.GeocheckByNodeResult | backend-go/internal/stubs/stubs.go:188 | Bearer JWT/API token + scopes/AdminOnly |
| API-041 | POST | /api/connections/geocheck/{nodeUuid} | s.GeocheckByNode | backend-go/internal/stubs/stubs.go:187 | Bearer JWT/API token + scopes/AdminOnly |
| API-042 | GET | /api/external-squads | squadsHandler.GetExternalSquads | backend-go/internal/server/server.go:455 | Bearer JWT/API token + scopes/AdminOnly |
| API-043 | PATCH | /api/external-squads | squadsHandler.UpdateExternalSquad | backend-go/internal/server/server.go:458 | Bearer JWT/API token + scopes/AdminOnly |
| API-044 | POST | /api/external-squads | squadsHandler.CreateExternalSquad | backend-go/internal/server/server.go:456 | Bearer JWT/API token + scopes/AdminOnly |
| API-045 | POST | /api/external-squads/actions/reorder | squadsHandler.ReorderExternalSquads | backend-go/internal/server/server.go:460 | Bearer JWT/API token + scopes/AdminOnly |
| API-046 | GET | /api/external-squads/tags | squadsHandler.GetExternalSquadsTags | backend-go/internal/server/server.go:461 | Bearer JWT/API token + scopes/AdminOnly |
| API-047 | PATCH | /api/external-squads/tags | squadsHandler.SetExternalSquadsTags | backend-go/internal/server/server.go:462 | Bearer JWT/API token + scopes/AdminOnly |
| API-048 | DELETE | /api/external-squads/{uuid} | squadsHandler.DeleteExternalSquad | backend-go/internal/server/server.go:459 | Bearer JWT/API token + scopes/AdminOnly |
| API-049 | GET | /api/external-squads/{uuid} | squadsHandler.GetExternalSquad | backend-go/internal/server/server.go:457 | Bearer JWT/API token + scopes/AdminOnly |
| API-050 | POST | /api/external-squads/{uuid}/bulk-actions/add-users | squadsHandler.SquadBulkAction | backend-go/internal/server/server.go:463 | Bearer JWT/API token + scopes/AdminOnly |
| API-051 | DELETE | /api/external-squads/{uuid}/bulk-actions/remove-users | squadsHandler.SquadBulkAction | backend-go/internal/server/server.go:464 | Bearer JWT/API token + scopes/AdminOnly |
| API-052 | GET | /api/hosts | cpHandler.GetHosts | backend-go/internal/server/server.go:415 | Bearer JWT/API token + scopes/AdminOnly |
| API-053 | PATCH | /api/hosts | cpHandler.UpdateHost | backend-go/internal/server/server.go:418 | Bearer JWT/API token + scopes/AdminOnly |
| API-054 | POST | /api/hosts | cpHandler.CreateHost | backend-go/internal/server/server.go:416 | Bearer JWT/API token + scopes/AdminOnly |
| API-055 | POST | /api/hosts/actions/clone | cpHandler.CloneHost | backend-go/internal/server/server.go:421 | Bearer JWT/API token + scopes/AdminOnly |
| API-056 | POST | /api/hosts/actions/reorder | cpHandler.ReorderHosts | backend-go/internal/server/server.go:422 | Bearer JWT/API token + scopes/AdminOnly |
| API-057 | POST | /api/hosts/bulk/delete | cpHandler.BulkDeleteHosts | backend-go/internal/server/server.go:423 | Bearer JWT/API token + scopes/AdminOnly |
| API-058 | POST | /api/hosts/bulk/disable | cpHandler.BulkDisableHosts | backend-go/internal/server/server.go:424 | Bearer JWT/API token + scopes/AdminOnly |
| API-059 | POST | /api/hosts/bulk/enable | cpHandler.BulkEnableHosts | backend-go/internal/server/server.go:425 | Bearer JWT/API token + scopes/AdminOnly |
| API-060 | PATCH | /api/hosts/bulk/update | cpHandler.BulkUpdateHosts | backend-go/internal/server/server.go:426 | Bearer JWT/API token + scopes/AdminOnly |
| API-061 | POST | /api/hosts/preview | cpHandler.Preview | backend-go/internal/server/server.go:420 | Bearer JWT/API token + scopes/AdminOnly |
| API-062 | GET | /api/hosts/tags | cpHandler.GetHostsTags | backend-go/internal/server/server.go:414 | Bearer JWT/API token + scopes/AdminOnly |
| API-063 | DELETE | /api/hosts/{uuid} | cpHandler.DeleteHost | backend-go/internal/server/server.go:419 | Bearer JWT/API token + scopes/AdminOnly |
| API-064 | GET | /api/hosts/{uuid} | cpHandler.GetHost | backend-go/internal/server/server.go:417 | Bearer JWT/API token + scopes/AdminOnly |
| API-065 | GET | /api/hwid/devices | s.GetHwidDevices | backend-go/internal/stubs/stubs.go:177 | Bearer JWT/API token + scopes/AdminOnly |
| API-066 | POST | /api/hwid/devices | s.CreateHwidDevice | backend-go/internal/stubs/stubs.go:178 | Bearer JWT/API token + scopes/AdminOnly |
| API-067 | POST | /api/hwid/devices/delete | s.DeleteHwidDevice | backend-go/internal/stubs/stubs.go:179 | Bearer JWT/API token + scopes/AdminOnly |
| API-068 | POST | /api/hwid/devices/delete-all | s.DeleteAllHwidDevices | backend-go/internal/stubs/stubs.go:180 | Bearer JWT/API token + scopes/AdminOnly |
| API-069 | GET | /api/hwid/devices/stats | s.GetHwidStats | backend-go/internal/stubs/stubs.go:175 | Bearer JWT/API token + scopes/AdminOnly |
| API-070 | GET | /api/hwid/devices/top-users | s.GetHwidTopUsers | backend-go/internal/stubs/stubs.go:176 | Bearer JWT/API token + scopes/AdminOnly |
| API-071 | GET | /api/hwid/devices/{userId} | s.GetUserHwidDevices | backend-go/internal/stubs/stubs.go:181 | Bearer JWT/API token + scopes/AdminOnly |
| API-072 | GET | /api/infra-billing/history | infrabillingHandler.GetHistory | backend-go/internal/server/server.go:494 | Bearer JWT/API token + scopes/AdminOnly |
| API-073 | POST | /api/infra-billing/history | infrabillingHandler.CreateHistory | backend-go/internal/server/server.go:495 | Bearer JWT/API token + scopes/AdminOnly |
| API-074 | DELETE | /api/infra-billing/history/{uuid} | infrabillingHandler.DeleteHistory | backend-go/internal/server/server.go:496 | Bearer JWT/API token + scopes/AdminOnly |
| API-075 | GET | /api/infra-billing/nodes | infrabillingHandler.GetNodes | backend-go/internal/server/server.go:490 | Bearer JWT/API token + scopes/AdminOnly |
| API-076 | PATCH | /api/infra-billing/nodes | infrabillingHandler.UpdateNode | backend-go/internal/server/server.go:492 | Bearer JWT/API token + scopes/AdminOnly |
| API-077 | POST | /api/infra-billing/nodes | infrabillingHandler.CreateNode | backend-go/internal/server/server.go:491 | Bearer JWT/API token + scopes/AdminOnly |
| API-078 | DELETE | /api/infra-billing/nodes/{uuid} | infrabillingHandler.DeleteNode | backend-go/internal/server/server.go:493 | Bearer JWT/API token + scopes/AdminOnly |
| API-079 | GET | /api/infra-billing/providers | infrabillingHandler.GetProviders | backend-go/internal/server/server.go:485 | Bearer JWT/API token + scopes/AdminOnly |
| API-080 | PATCH | /api/infra-billing/providers | infrabillingHandler.UpdateProvider | backend-go/internal/server/server.go:488 | Bearer JWT/API token + scopes/AdminOnly |
| API-081 | POST | /api/infra-billing/providers | infrabillingHandler.CreateProvider | backend-go/internal/server/server.go:486 | Bearer JWT/API token + scopes/AdminOnly |
| API-082 | DELETE | /api/infra-billing/providers/{uuid} | infrabillingHandler.DeleteProvider | backend-go/internal/server/server.go:489 | Bearer JWT/API token + scopes/AdminOnly |
| API-083 | GET | /api/infra-billing/providers/{uuid} | infrabillingHandler.GetProvider | backend-go/internal/server/server.go:487 | Bearer JWT/API token + scopes/AdminOnly |
| API-084 | GET | /api/internal-squads | squadsHandler.GetInternalSquads | backend-go/internal/server/server.go:441 | Bearer JWT/API token + scopes/AdminOnly |
| API-085 | PATCH | /api/internal-squads | squadsHandler.UpdateInternalSquad | backend-go/internal/server/server.go:444 | Bearer JWT/API token + scopes/AdminOnly |
| API-086 | POST | /api/internal-squads | squadsHandler.CreateInternalSquad | backend-go/internal/server/server.go:442 | Bearer JWT/API token + scopes/AdminOnly |
| API-087 | POST | /api/internal-squads/actions/reorder | squadsHandler.ReorderInternalSquads | backend-go/internal/server/server.go:446 | Bearer JWT/API token + scopes/AdminOnly |
| API-088 | GET | /api/internal-squads/tags | squadsHandler.GetInternalSquadsTags | backend-go/internal/server/server.go:447 | Bearer JWT/API token + scopes/AdminOnly |
| API-089 | PATCH | /api/internal-squads/tags | squadsHandler.SetInternalSquadsTags | backend-go/internal/server/server.go:448 | Bearer JWT/API token + scopes/AdminOnly |
| API-090 | DELETE | /api/internal-squads/{uuid} | squadsHandler.DeleteInternalSquad | backend-go/internal/server/server.go:445 | Bearer JWT/API token + scopes/AdminOnly |
| API-091 | GET | /api/internal-squads/{uuid} | squadsHandler.GetInternalSquad | backend-go/internal/server/server.go:443 | Bearer JWT/API token + scopes/AdminOnly |
| API-092 | GET | /api/internal-squads/{uuid}/accessible-nodes | squadsHandler.GetInternalSquadAccessibleNodes | backend-go/internal/server/server.go:449 | Bearer JWT/API token + scopes/AdminOnly |
| API-093 | POST | /api/internal-squads/{uuid}/bulk-actions/add-many-users | squadsHandler.SquadBulkAction | backend-go/internal/server/server.go:451 | Bearer JWT/API token + scopes/AdminOnly |
| API-094 | POST | /api/internal-squads/{uuid}/bulk-actions/add-users | squadsHandler.SquadBulkAction | backend-go/internal/server/server.go:450 | Bearer JWT/API token + scopes/AdminOnly |
| API-095 | DELETE | /api/internal-squads/{uuid}/bulk-actions/remove-many-users | squadsHandler.SquadBulkAction | backend-go/internal/server/server.go:453 | Bearer JWT/API token + scopes/AdminOnly |
| API-096 | DELETE | /api/internal-squads/{uuid}/bulk-actions/remove-users | squadsHandler.SquadBulkAction | backend-go/internal/server/server.go:452 | Bearer JWT/API token + scopes/AdminOnly |
| API-097 | GET | /api/keygen | s.GetKeygen | backend-go/internal/stubs/stubs.go:158 | Bearer JWT/API token + scopes/AdminOnly |
| API-098 | GET | /api/metadata/node/{uuid} | s.GetNodeMetadata | backend-go/internal/stubs/stubs.go:191 | Bearer JWT/API token + scopes/AdminOnly |
| API-099 | PUT | /api/metadata/node/{uuid} | s.UpsertNodeMetadata | backend-go/internal/stubs/stubs.go:192 | Bearer JWT/API token + scopes/AdminOnly |
| API-100 | GET | /api/metadata/user/{userId} | s.GetUserMetadata | backend-go/internal/stubs/stubs.go:193 | Bearer JWT/API token + scopes/AdminOnly |
| API-101 | PUT | /api/metadata/user/{userId} | s.UpsertUserMetadata | backend-go/internal/stubs/stubs.go:194 | Bearer JWT/API token + scopes/AdminOnly |
| API-102 | GET | /api/node-integrations | s.GetNodeIntegrations | backend-go/internal/stubs/stubs.go:152 | Bearer JWT/API token + scopes/AdminOnly |
| API-103 | PATCH | /api/node-integrations | s.UpdateNodeIntegration | backend-go/internal/stubs/stubs.go:155 | Bearer JWT/API token + scopes/AdminOnly |
| API-104 | POST | /api/node-integrations | s.CreateNodeIntegration | backend-go/internal/stubs/stubs.go:153 | Bearer JWT/API token + scopes/AdminOnly |
| API-105 | DELETE | /api/node-integrations/{uuid} | s.DeleteNodeIntegration | backend-go/internal/stubs/stubs.go:156 | Bearer JWT/API token + scopes/AdminOnly |
| API-106 | GET | /api/node-integrations/{uuid} | s.GetNodeIntegration | backend-go/internal/stubs/stubs.go:154 | Bearer JWT/API token + scopes/AdminOnly |
| API-107 | GET | /api/node-plugins | s.GetNodePlugins | backend-go/internal/stubs/stubs.go:142 | Bearer JWT/API token + scopes/AdminOnly |
| API-108 | PATCH | /api/node-plugins | s.UpdateNodePlugin | backend-go/internal/stubs/stubs.go:145 | Bearer JWT/API token + scopes/AdminOnly |
| API-109 | POST | /api/node-plugins | s.CreateNodePlugin | backend-go/internal/stubs/stubs.go:143 | Bearer JWT/API token + scopes/AdminOnly |
| API-110 | POST | /api/node-plugins/actions/clone | s.CloneNodePlugin | backend-go/internal/stubs/stubs.go:147 | Bearer JWT/API token + scopes/AdminOnly |
| API-111 | POST | /api/node-plugins/actions/reorder | s.ReorderNodePlugins | backend-go/internal/stubs/stubs.go:148 | Bearer JWT/API token + scopes/AdminOnly |
| API-112 | POST | /api/node-plugins/actions/sync | s.SyncNodePlugin | backend-go/internal/stubs/stubs.go:149 | Bearer JWT/API token + scopes/AdminOnly |
| API-113 | POST | /api/node-plugins/executor | s.ExecuteNodePlugin | backend-go/internal/stubs/stubs.go:150 | Bearer JWT/API token + scopes/AdminOnly |
| API-114 | DELETE | /api/node-plugins/shared-lists | s.DeleteSharedList | backend-go/internal/stubs/stubs.go:137 | Bearer JWT/API token + scopes/AdminOnly |
| API-115 | GET | /api/node-plugins/shared-lists | s.GetSharedLists | backend-go/internal/stubs/stubs.go:134 | Bearer JWT/API token + scopes/AdminOnly |
| API-116 | PATCH | /api/node-plugins/shared-lists | s.UpdateSharedList | backend-go/internal/stubs/stubs.go:136 | Bearer JWT/API token + scopes/AdminOnly |
| API-117 | POST | /api/node-plugins/shared-lists | s.CreateSharedList | backend-go/internal/stubs/stubs.go:135 | Bearer JWT/API token + scopes/AdminOnly |
| API-118 | POST | /api/node-plugins/shared-lists/actions/sync | s.SyncSharedLists | backend-go/internal/stubs/stubs.go:138 | Bearer JWT/API token + scopes/AdminOnly |
| API-119 | GET | /api/node-plugins/shared-lists/by-name | s.GetSharedListByName | backend-go/internal/stubs/stubs.go:133 | Bearer JWT/API token + scopes/AdminOnly |
| API-120 | GET | /api/node-plugins/tags | s.GetNodePluginsTags | backend-go/internal/stubs/stubs.go:140 | Bearer JWT/API token + scopes/AdminOnly |
| API-121 | PATCH | /api/node-plugins/tags | s.SetNodePluginsTags | backend-go/internal/stubs/stubs.go:141 | Bearer JWT/API token + scopes/AdminOnly |
| API-122 | GET | /api/node-plugins/torrent-blocker | s.GetTorrentBlockerReports | backend-go/internal/stubs/stubs.go:130 | Bearer JWT/API token + scopes/AdminOnly |
| API-123 | GET | /api/node-plugins/torrent-blocker/stats | s.GetTorrentBlockerStats | backend-go/internal/stubs/stubs.go:129 | Bearer JWT/API token + scopes/AdminOnly |
| API-124 | DELETE | /api/node-plugins/torrent-blocker/truncate | s.TruncateTorrentBlockerReports | backend-go/internal/stubs/stubs.go:131 | Bearer JWT/API token + scopes/AdminOnly |
| API-125 | DELETE | /api/node-plugins/{uuid} | s.DeleteNodePlugin | backend-go/internal/stubs/stubs.go:146 | Bearer JWT/API token + scopes/AdminOnly |
| API-126 | GET | /api/node-plugins/{uuid} | s.GetNodePluginByUuid | backend-go/internal/stubs/stubs.go:144 | Bearer JWT/API token + scopes/AdminOnly |
| API-127 | POST | /api/node-ssh/vault/evaluate | s.EvaluateVault | backend-go/internal/stubs/stubs.go:173 | Bearer JWT/API token + scopes/AdminOnly |
| API-128 | GET | /api/node-ssh/ws | sshHandler.Socket | backend-go/internal/server/server.go:311 | public (handler checks); SSH uses ticket + protocol |
| API-129 | POST | /api/node-ssh/{uuid}/ticket | s.CreateSshTicket | backend-go/internal/stubs/stubs.go:172 | Bearer JWT/API token + scopes/AdminOnly |
| API-130 | GET | /api/nodes | nodeHandler.GetNodes | backend-go/internal/server/server.go:393 | Bearer JWT/API token + scopes/AdminOnly |
| API-131 | PATCH | /api/nodes | nodeHandler.PatchNode | backend-go/internal/server/server.go:397 | Bearer JWT/API token + scopes/AdminOnly |
| API-132 | POST | /api/nodes | nodeHandler.CreateNode | backend-go/internal/server/server.go:396 | Bearer JWT/API token + scopes/AdminOnly |
| API-133 | POST | /api/nodes/actions/reorder | nodeHandler.ReorderNodes | backend-go/internal/server/server.go:409 | Bearer JWT/API token + scopes/AdminOnly |
| API-134 | POST | /api/nodes/actions/restart-all | nodeHandler.RestartAllNodes | backend-go/internal/server/server.go:408 | Bearer JWT/API token + scopes/AdminOnly |
| API-135 | POST | /api/nodes/bulk-actions | nodeHandler.BulkActions | backend-go/internal/server/server.go:410 | Bearer JWT/API token + scopes/AdminOnly |
| API-136 | POST | /api/nodes/bulk-actions/profile-modification | nodeHandler.BulkActions | backend-go/internal/server/server.go:411 | Bearer JWT/API token + scopes/AdminOnly |
| API-137 | POST | /api/nodes/bulk-actions/update | nodeHandler.BulkActions | backend-go/internal/server/server.go:412 | Bearer JWT/API token + scopes/AdminOnly |
| API-138 | GET | /api/nodes/tags | nodeHandler.GetTags | backend-go/internal/server/server.go:394 | Bearer JWT/API token + scopes/AdminOnly |
| API-139 | GET | /api/nodes/traffic-summary | nodeHandler.GetTrafficSummary | backend-go/internal/server/server.go:395 | Bearer JWT/API token + scopes/AdminOnly |
| API-140 | DELETE | /api/nodes/{uuid} | nodeHandler.DeleteNode | backend-go/internal/server/server.go:403 | Bearer JWT/API token + scopes/AdminOnly |
| API-141 | GET | /api/nodes/{uuid} | nodeHandler.GetNode | backend-go/internal/server/server.go:398 | Bearer JWT/API token + scopes/AdminOnly |
| API-142 | PATCH | /api/nodes/{uuid} | nodeHandler.UpdateNode | backend-go/internal/server/server.go:402 | Bearer JWT/API token + scopes/AdminOnly |
| API-143 | POST | /api/nodes/{uuid}/actions/disable | nodeHandler.DisableNode | backend-go/internal/server/server.go:405 | Bearer JWT/API token + scopes/AdminOnly |
| API-144 | POST | /api/nodes/{uuid}/actions/enable | nodeHandler.EnableNode | backend-go/internal/server/server.go:404 | Bearer JWT/API token + scopes/AdminOnly |
| API-145 | POST | /api/nodes/{uuid}/actions/reset-traffic | nodeHandler.ResetTraffic | backend-go/internal/server/server.go:406 | Bearer JWT/API token + scopes/AdminOnly |
| API-146 | POST | /api/nodes/{uuid}/actions/restart | nodeHandler.RestartNode | backend-go/internal/server/server.go:407 | Bearer JWT/API token + scopes/AdminOnly |
| API-147 | GET | /api/nodes/{uuid}/logs | nodeHandler.GetNodeLogs | backend-go/internal/server/server.go:399 | Bearer JWT/API token + scopes/AdminOnly |
| API-148 | GET | /api/nodes/{uuid}/updates | nodeHandler.GetNodeUpdates | backend-go/internal/server/server.go:400 | Bearer JWT/API token + scopes/AdminOnly |
| API-149 | POST | /api/nodes/{uuid}/updates/apply | nodeHandler.ApplyNodeUpdate | backend-go/internal/server/server.go:401 | Bearer JWT/API token + scopes/AdminOnly |
| API-150 | DELETE | /api/passkeys | s.DeletePasskey | backend-go/internal/stubs/stubs.go:168 | Bearer JWT/API token + scopes/AdminOnly |
| API-151 | GET | /api/passkeys | s.GetPasskeys | backend-go/internal/stubs/stubs.go:166 | Bearer JWT/API token + scopes/AdminOnly |
| API-152 | PATCH | /api/passkeys | s.UpdatePasskey | backend-go/internal/stubs/stubs.go:167 | Bearer JWT/API token + scopes/AdminOnly |
| API-153 | GET | /api/passkeys/registration/options | s.GetPasskeyRegOptions | backend-go/internal/stubs/stubs.go:169 | Bearer JWT/API token + scopes/AdminOnly |
| API-154 | POST | /api/passkeys/registration/verify | s.VerifyPasskeyReg | backend-go/internal/stubs/stubs.go:170 | Bearer JWT/API token + scopes/AdminOnly |
| API-155 | GET | /api/remnawave-settings | sysHandler.GetSettings | backend-go/internal/server/server.go:350 | Bearer JWT/API token + scopes/AdminOnly |
| API-156 | PATCH | /api/remnawave-settings | sysHandler.UpdateSettings | backend-go/internal/server/server.go:351 | Bearer JWT/API token + scopes/AdminOnly |
| API-157 | DELETE | /api/snippets | s.DeleteSnippet | backend-go/internal/stubs/stubs.go:163 | Bearer JWT/API token + scopes/AdminOnly |
| API-158 | GET | /api/snippets | s.GetSnippets | backend-go/internal/stubs/stubs.go:160 | Bearer JWT/API token + scopes/AdminOnly |
| API-159 | PATCH | /api/snippets | s.UpdateSnippet | backend-go/internal/stubs/stubs.go:162 | Bearer JWT/API token + scopes/AdminOnly |
| API-160 | POST | /api/snippets | s.CreateSnippet | backend-go/internal/stubs/stubs.go:161 | Bearer JWT/API token + scopes/AdminOnly |
| API-161 | POST | /api/snippets/actions/sync | s.SyncSnippets | backend-go/internal/stubs/stubs.go:164 | Bearer JWT/API token + scopes/AdminOnly |
| API-162 | GET | /api/sub/{shortUuid} | subHandler.GetSubscription | backend-go/internal/server/server.go:326 | public (handler checks); SSH uses ticket + protocol |
| API-163 | GET | /api/sub/{shortUuid}/info | subHandler.GetSubscriptionInfo | backend-go/internal/server/server.go:327 | public (handler checks); SSH uses ticket + protocol |
| API-164 | GET | /api/sub/{shortUuid}/{clientType} | subHandler.GetSubscription | backend-go/internal/server/server.go:328 | public (handler checks); SSH uses ticket + protocol |
| API-165 | GET | /api/subscription-page-configs | subtemplatesHandler.GetAllConfigs | backend-go/internal/server/server.go:475 | Bearer JWT/API token + scopes/AdminOnly |
| API-166 | PATCH | /api/subscription-page-configs | subtemplatesHandler.UpdateConfig | backend-go/internal/server/server.go:478 | Bearer JWT/API token + scopes/AdminOnly |
| API-167 | POST | /api/subscription-page-configs | subtemplatesHandler.CreateConfig | backend-go/internal/server/server.go:476 | Bearer JWT/API token + scopes/AdminOnly |
| API-168 | POST | /api/subscription-page-configs/actions/clone | subtemplatesHandler.CloneConfig | backend-go/internal/server/server.go:480 | Bearer JWT/API token + scopes/AdminOnly |
| API-169 | POST | /api/subscription-page-configs/actions/reorder | subtemplatesHandler.ReorderConfigs | backend-go/internal/server/server.go:481 | Bearer JWT/API token + scopes/AdminOnly |
| API-170 | GET | /api/subscription-page-configs/tags | subtemplatesHandler.GetConfigTags | backend-go/internal/server/server.go:482 | Bearer JWT/API token + scopes/AdminOnly |
| API-171 | PATCH | /api/subscription-page-configs/tags | subtemplatesHandler.SetConfigTags | backend-go/internal/server/server.go:483 | Bearer JWT/API token + scopes/AdminOnly |
| API-172 | DELETE | /api/subscription-page-configs/{uuid} | subtemplatesHandler.DeleteConfig | backend-go/internal/server/server.go:479 | Bearer JWT/API token + scopes/AdminOnly |
| API-173 | GET | /api/subscription-page-configs/{uuid} | subtemplatesHandler.GetConfigByUuid | backend-go/internal/server/server.go:477 | Bearer JWT/API token + scopes/AdminOnly |
| API-174 | GET | /api/subscription-request-history | s.GetSubHistory | backend-go/internal/stubs/stubs.go:205 | Bearer JWT/API token + scopes/AdminOnly |
| API-175 | GET | /api/subscription-request-history/stats | s.GetSubHistoryStats | backend-go/internal/stubs/stubs.go:204 | Bearer JWT/API token + scopes/AdminOnly |
| API-176 | GET | /api/subscription-settings | sysHandler.GetSubscriptionSettings | backend-go/internal/server/server.go:342 | Bearer JWT/API token + scopes/AdminOnly |
| API-177 | PATCH | /api/subscription-settings | sysHandler.UpdateSubscriptionSettings | backend-go/internal/server/server.go:343 | Bearer JWT/API token + scopes/AdminOnly |
| API-178 | GET | /api/subscription-templates | subtemplatesHandler.GetAllTemplates | backend-go/internal/server/server.go:466 | Bearer JWT/API token + scopes/AdminOnly |
| API-179 | PATCH | /api/subscription-templates | subtemplatesHandler.UpdateTemplate | backend-go/internal/server/server.go:469 | Bearer JWT/API token + scopes/AdminOnly |
| API-180 | POST | /api/subscription-templates | subtemplatesHandler.CreateTemplate | backend-go/internal/server/server.go:467 | Bearer JWT/API token + scopes/AdminOnly |
| API-181 | POST | /api/subscription-templates/actions/reorder | subtemplatesHandler.ReorderTemplates | backend-go/internal/server/server.go:471 | Bearer JWT/API token + scopes/AdminOnly |
| API-182 | GET | /api/subscription-templates/tags | subtemplatesHandler.GetTemplateTags | backend-go/internal/server/server.go:472 | Bearer JWT/API token + scopes/AdminOnly |
| API-183 | PATCH | /api/subscription-templates/tags | subtemplatesHandler.SetTemplateTags | backend-go/internal/server/server.go:473 | Bearer JWT/API token + scopes/AdminOnly |
| API-184 | DELETE | /api/subscription-templates/{uuid} | subtemplatesHandler.DeleteTemplate | backend-go/internal/server/server.go:470 | Bearer JWT/API token + scopes/AdminOnly |
| API-185 | GET | /api/subscription-templates/{uuid} | subtemplatesHandler.GetTemplateByUuid | backend-go/internal/server/server.go:468 | Bearer JWT/API token + scopes/AdminOnly |
| API-186 | GET | /api/subscriptions | s.GetAllSubscriptions | backend-go/internal/stubs/stubs.go:196 | Bearer JWT/API token + scopes/AdminOnly |
| API-187 | GET | /api/subscriptions/by-id/{userId} | s.GetSubscriptionById | backend-go/internal/stubs/stubs.go:197 | Bearer JWT/API token + scopes/AdminOnly |
| API-188 | GET | /api/subscriptions/by-short-uuid/{shortUuid} | s.GetSubscriptionByShortUuid | backend-go/internal/stubs/stubs.go:198 | Bearer JWT/API token + scopes/AdminOnly |
| API-189 | GET | /api/subscriptions/by-short-uuid/{shortUuid}/raw | s.GetRawSubscriptionByShortUuid | backend-go/internal/stubs/stubs.go:199 | Bearer JWT/API token + scopes/AdminOnly |
| API-190 | GET | /api/subscriptions/by-username/{username} | s.GetSubscriptionByUsername | backend-go/internal/stubs/stubs.go:200 | Bearer JWT/API token + scopes/AdminOnly |
| API-191 | GET | /api/subscriptions/connection-keys/{userId} | s.GetConnectionKeysByUserId | backend-go/internal/stubs/stubs.go:201 | Bearer JWT/API token + scopes/AdminOnly |
| API-192 | GET | /api/subscriptions/subpage-config/{shortUuid} | s.GetSubpageConfigByShortUuid | backend-go/internal/stubs/stubs.go:202 | Bearer JWT/API token + scopes/AdminOnly |
| API-193 | POST | /api/system/actions/restore | sysHandler.RestoreBackup | backend-go/internal/server/server.go:352 | Bearer JWT/API token + scopes/AdminOnly |
| API-194 | GET | /api/system/configuration | s.GetSystemConfiguration | backend-go/internal/stubs/stubs.go:215 | Bearer JWT/API token + scopes/AdminOnly |
| API-195 | GET | /api/system/health | sysHandler.GetHealth | backend-go/internal/server/server.go:313 | public (handler checks); SSH uses ticket + protocol |
| API-196 | HEAD | /api/system/health | sysHandler.GetHealth | backend-go/internal/server/server.go:314 | public (handler checks); SSH uses ticket + protocol |
| API-197 | GET | /api/system/metadata | sysHandler.GetMetadata | backend-go/internal/server/server.go:333 | Bearer JWT/API token + scopes/AdminOnly |
| API-198 | GET | /api/system/nodes/metrics | sysHandler.GetNodesMetrics | backend-go/internal/server/server.go:347 | Bearer JWT/API token + scopes/AdminOnly |
| API-199 | GET | /api/system/stats | sysHandler.GetStats | backend-go/internal/server/server.go:344 | Bearer JWT/API token + scopes/AdminOnly |
| API-200 | GET | /api/system/stats/bandwidth | sysHandler.GetBandwidthStats | backend-go/internal/server/server.go:345 | Bearer JWT/API token + scopes/AdminOnly |
| API-201 | GET | /api/system/stats/digest | s.GetStatsDigest | backend-go/internal/stubs/stubs.go:216 | Bearer JWT/API token + scopes/AdminOnly |
| API-202 | GET | /api/system/stats/http | sysHandler.GetHttpStats | backend-go/internal/server/server.go:349 | Bearer JWT/API token + scopes/AdminOnly |
| API-203 | GET | /api/system/stats/nodes | sysHandler.GetNodesStatistics | backend-go/internal/server/server.go:346 | Bearer JWT/API token + scopes/AdminOnly |
| API-204 | GET | /api/system/stats/recap | sysHandler.GetRecap | backend-go/internal/server/server.go:348 | Bearer JWT/API token + scopes/AdminOnly |
| API-205 | POST | /api/system/testers/srr-matcher | s.DebugSrrMatcher | backend-go/internal/stubs/stubs.go:217 | Bearer JWT/API token + scopes/AdminOnly |
| API-206 | GET | /api/system/tools/x25519/generate | s.GenerateX25519 | backend-go/internal/stubs/stubs.go:218 | Bearer JWT/API token + scopes/AdminOnly |
| API-207 | POST | /api/system/updates/apply | sysHandler.ApplyUpdate | backend-go/internal/server/server.go:335 | Bearer JWT/API token + scopes/AdminOnly |
| API-208 | GET | /api/system/updates/check | sysHandler.CheckUpdate | backend-go/internal/server/server.go:334 | Bearer JWT/API token + scopes/AdminOnly |
| API-209 | GET | /api/tokens | tokensHandler.GetApiTokens | backend-go/internal/server/server.go:336 | Bearer JWT/API token + scopes/AdminOnly |
| API-210 | POST | /api/tokens | tokensHandler.CreateApiToken | backend-go/internal/server/server.go:337 | Bearer JWT/API token + scopes/AdminOnly |
| API-211 | POST | /api/tokens/ott | tokensHandler.GetOtt | backend-go/internal/server/server.go:340 | Bearer JWT/API token + scopes/AdminOnly |
| API-212 | GET | /api/tokens/scopes | tokensHandler.GetScopes | backend-go/internal/server/server.go:339 | Bearer JWT/API token + scopes/AdminOnly |
| API-213 | DELETE | /api/tokens/{uuid} | tokensHandler.DeleteApiToken | backend-go/internal/server/server.go:338 | Bearer JWT/API token + scopes/AdminOnly |
| API-214 | GET | /api/users | userHandler.GetUsers | backend-go/internal/server/server.go:354 | Bearer JWT/API token + scopes/AdminOnly |
| API-215 | PATCH | /api/users | userHandler.PatchUser | backend-go/internal/server/server.go:358 | Bearer JWT/API token + scopes/AdminOnly |
| API-216 | POST | /api/users | userHandler.CreateUser | backend-go/internal/server/server.go:357 | Bearer JWT/API token + scopes/AdminOnly |
| API-217 | POST | /api/users/actions/resolve | userHandler.ResolveUser | backend-go/internal/server/server.go:360 | Bearer JWT/API token + scopes/AdminOnly |
| API-218 | POST | /api/users/bulk-actions | userHandler.BulkUserAction | backend-go/internal/server/server.go:373 | Bearer JWT/API token + scopes/AdminOnly |
| API-219 | POST | /api/users/bulk-actions/delete | userHandler.BulkUserAction | backend-go/internal/server/server.go:375 | Bearer JWT/API token + scopes/AdminOnly |
| API-220 | POST | /api/users/bulk-actions/profile-modification | userHandler.BulkUserAction | backend-go/internal/server/server.go:377 | Bearer JWT/API token + scopes/AdminOnly |
| API-221 | POST | /api/users/bulk-actions/reset-traffic | userHandler.BulkUserAction | backend-go/internal/server/server.go:374 | Bearer JWT/API token + scopes/AdminOnly |
| API-222 | POST | /api/users/bulk-actions/status-modification | userHandler.BulkUserAction | backend-go/internal/server/server.go:376 | Bearer JWT/API token + scopes/AdminOnly |
| API-223 | POST | /api/users/bulk-actions/template-modification | userHandler.BulkUserAction | backend-go/internal/server/server.go:378 | Bearer JWT/API token + scopes/AdminOnly |
| API-224 | POST | /api/users/bulk/all/extend-expiration-date | userHandler.BulkAllExtendExpirationDate | backend-go/internal/server/server.go:362 | Bearer JWT/API token + scopes/AdminOnly |
| API-225 | POST | /api/users/bulk/all/reset-traffic | userHandler.BulkAllResetTraffic | backend-go/internal/server/server.go:363 | Bearer JWT/API token + scopes/AdminOnly |
| API-226 | POST | /api/users/bulk/all/update | userHandler.BulkAllUpdate | backend-go/internal/server/server.go:364 | Bearer JWT/API token + scopes/AdminOnly |
| API-227 | POST | /api/users/bulk/delete | userHandler.BulkDelete | backend-go/internal/server/server.go:365 | Bearer JWT/API token + scopes/AdminOnly |
| API-228 | POST | /api/users/bulk/delete-by-status | userHandler.BulkDeleteByStatus | backend-go/internal/server/server.go:366 | Bearer JWT/API token + scopes/AdminOnly |
| API-229 | POST | /api/users/bulk/extend-expiration-date | userHandler.BulkExtendExpirationDate | backend-go/internal/server/server.go:367 | Bearer JWT/API token + scopes/AdminOnly |
| API-230 | POST | /api/users/bulk/reset-traffic | userHandler.BulkResetTraffic | backend-go/internal/server/server.go:368 | Bearer JWT/API token + scopes/AdminOnly |
| API-231 | POST | /api/users/bulk/revoke-subscription | userHandler.BulkRevokeSubscription | backend-go/internal/server/server.go:369 | Bearer JWT/API token + scopes/AdminOnly |
| API-232 | POST | /api/users/bulk/update | userHandler.BulkUpdate | backend-go/internal/server/server.go:370 | Bearer JWT/API token + scopes/AdminOnly |
| API-233 | POST | /api/users/bulk/update-squads | userHandler.BulkUpdateSquads | backend-go/internal/server/server.go:371 | Bearer JWT/API token + scopes/AdminOnly |
| API-234 | GET | /api/users/by-short-uuid/{shortUuid} | userHandler.GetUserByShortUuid | backend-go/internal/server/server.go:383 | Bearer JWT/API token + scopes/AdminOnly |
| API-235 | GET | /api/users/by-username/{username} | userHandler.GetUserByUsername | backend-go/internal/server/server.go:384 | Bearer JWT/API token + scopes/AdminOnly |
| API-236 | POST | /api/users/resolve | userHandler.ResolveUser | backend-go/internal/server/server.go:359 | Bearer JWT/API token + scopes/AdminOnly |
| API-237 | GET | /api/users/stream | userHandler.GetUsersStream | backend-go/internal/server/server.go:355 | Bearer JWT/API token + scopes/AdminOnly |
| API-238 | GET | /api/users/tags | userHandler.GetTags | backend-go/internal/server/server.go:356 | Bearer JWT/API token + scopes/AdminOnly |
| API-239 | DELETE | /api/users/{userId} | userHandler.DeleteUser | backend-go/internal/server/server.go:382 | Bearer JWT/API token + scopes/AdminOnly |
| API-240 | GET | /api/users/{userId} | userHandler.GetUser | backend-go/internal/server/server.go:380 | Bearer JWT/API token + scopes/AdminOnly |
| API-241 | PATCH | /api/users/{userId} | userHandler.UpdateUser | backend-go/internal/server/server.go:381 | Bearer JWT/API token + scopes/AdminOnly |
| API-242 | GET | /api/users/{userId}/accessible-nodes | userHandler.GetUserAccessibleNodes | backend-go/internal/server/server.go:385 | Bearer JWT/API token + scopes/AdminOnly |
| API-243 | POST | /api/users/{userId}/actions/disable | userHandler.DisableUser | backend-go/internal/server/server.go:389 | Bearer JWT/API token + scopes/AdminOnly |
| API-244 | POST | /api/users/{userId}/actions/enable | userHandler.EnableUser | backend-go/internal/server/server.go:388 | Bearer JWT/API token + scopes/AdminOnly |
| API-245 | POST | /api/users/{userId}/actions/extend | userHandler.ExtendUser | backend-go/internal/server/server.go:390 | Bearer JWT/API token + scopes/AdminOnly |
| API-246 | POST | /api/users/{userId}/actions/reset-traffic | userHandler.ResetTraffic | backend-go/internal/server/server.go:387 | Bearer JWT/API token + scopes/AdminOnly |
| API-247 | POST | /api/users/{userId}/actions/revoke | userHandler.RevokeUser | backend-go/internal/server/server.go:391 | Bearer JWT/API token + scopes/AdminOnly |
| API-248 | GET | /api/users/{userId}/subscription-request-history | userHandler.GetUserSubscriptionRequestHistory | backend-go/internal/server/server.go:386 | Bearer JWT/API token + scopes/AdminOnly |
