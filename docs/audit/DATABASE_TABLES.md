# Database model mapping

Source: `d709bad01dc0ceacb20012a3afdf528eddfd061f`.

37 explicit TableName methods + 3 default GORM names from schemaModels; additionally gowave_migrations. SQL migrations are authoritative. Some join models are referenced via associations rather than direct package expressions.

| Go model | SQL table |
| --- | --- |
| Admin | admin |
| ApiToken | api_tokens |
| AuthChallenge | auth_challenges |
| ConfigProfile | config_profiles |
| ConfigProfileInbound | config_profile_inbounds |
| ConfigProfileInboundsToNodes | config_profile_inbounds_to_nodes |
| ConfigProfileSnippet | config_profile_snippets |
| EntityMeta | entity_meta |
| ExternalSquad | external_squads |
| ExternalSquadTemplate | external_squads_templates |
| Host | hosts |
| HostsToNode | hosts_to_nodes |
| HwidDevice | hwid_user_devices |
| InfraBillingHistory | infra_billing_history |
| InfraBillingNode | infra_billing_nodes |
| InfraProvider | infra_providers |
| Integration | integrations |
| InternalSquad | internal_squads |
| InternalSquadHostLink | internal_squad_host_links |
| InternalSquadInbound | internal_squad_inbounds |
| InternalSquadMember | internal_squad_members |
| Job | jobs |
| Keygen | keygen |
| Node | nodes |
| NodeMeta | node_meta |
| NodePlugin | node_plugin |
| NodesUsageHistory | nodes_usage_history |
| NodesUserUsageHistory | nodes_user_usage_history |
| PanelSetting | remnawave_settings |
| Passkey | passkeys |
| ScheduledExecution | scheduled_executions |
| SharedList | shared_lists |
| SubscriptionPageConfig | subscription_page_config |
| SubscriptionSetting | subscription_settings |
| SubscriptionTemplate | subscription_templates |
| TorrentBlockerReport | torrent_blocker_reports |
| User | users |
| UserMeta | user_meta |
| UserSubscriptionRequestHistory | user_subscription_request_history |
| UserTraffic | user_traffic |
