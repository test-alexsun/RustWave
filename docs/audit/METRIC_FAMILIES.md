# Prometheus families

Source: `d709bad01dc0ceacb20012a3afdf528eddfd061f`.

31 families, exact HELP/TYPE and label keys from definitions.go + exporter.go. Units follow names/help; values require controlled event fixtures.

| Name | TYPE | HELP | Labels |
| --- | --- | --- | --- |
| remnawave_node_online_users | gauge | Number of online users on a node | node_uuid,app=remnawave |
| remnawave_node_status | gauge | Node connection status (1 - connected, 0 - disconnected) | node_uuid,app=remnawave |
| remnawave_users_status | gauge | Counter for users statuses, updated every 1 minute | status,app=remnawave |
| remnawave_users_online_stats | gauge | Counter for online stats of distinct users, updated every 1 minute | metricType,app=remnawave |
| remnawave_users_total | gauge | Total number of users, updated every 1 minute | type,app=remnawave |
| remnawave_node_inbound_upload_bytes | counter | Inbound upload bytes, updated every 30 seconds | node_uuid,tag,app=remnawave |
| remnawave_node_inbound_download_bytes | counter | Inbound download bytes, updated every 30 seconds | node_uuid,tag,app=remnawave |
| remnawave_node_outbound_upload_bytes | counter | Outbound upload bytes, updated every 30 seconds | node_uuid,tag,app=remnawave |
| remnawave_node_outbound_download_bytes | counter | Outbound download bytes, updated every 30 seconds | node_uuid,tag,app=remnawave |
| remnawave_process_rss_bytes | gauge | Process resident set size in bytes. | instance_id, instance_name,app=remnawave |
| remnawave_process_heap_used_bytes | gauge | Process heap used in bytes. | instance_id, instance_name,app=remnawave |
| remnawave_process_heap_total_bytes | gauge | Process total heap size in bytes. | instance_id, instance_name,app=remnawave |
| remnawave_process_external_bytes | gauge | Process external memory in bytes (C++ objects bound to JS). | instance_id, instance_name,app=remnawave |
| remnawave_process_array_buffers_bytes | gauge | Process ArrayBuffers memory in bytes. | instance_id, instance_name,app=remnawave |
| remnawave_process_event_loop_delay_ms | gauge | Mean event loop delay in milliseconds. | instance_id, instance_name,app=remnawave |
| remnawave_process_event_loop_p99_ms | gauge | Event loop delay p99 in milliseconds. | instance_id, instance_name,app=remnawave |
| remnawave_process_active_handles | gauge | Number of active resource handles. | instance_id, instance_name,app=remnawave |
| remnawave_process_uptime_seconds | gauge | Process uptime in seconds. | instance_id, instance_name,app=remnawave |
| remnawave_node_network_rx_bytes_per_sec | gauge | Node network receive speed in bytes per second | node_uuid,app=remnawave |
| remnawave_node_network_tx_bytes_per_sec | gauge | Node network transmit speed in bytes per second | node_uuid,app=remnawave |
| remnawave_node_network_rx_bytes_total | gauge | Node network total received bytes since boot from default interface | node_uuid,app=remnawave |
| remnawave_node_network_tx_bytes_total | gauge | Node network total transmitted bytes since boot from default interface | node_uuid,app=remnawave |
| remnawave_node_memory_total_bytes | gauge | Node total memory in bytes | node_uuid,app=remnawave |
| remnawave_node_memory_free_bytes | gauge | Node free memory in bytes | node_uuid,app=remnawave |
| remnawave_node_uptime_seconds | gauge | Node OS uptime in seconds | node_uuid,app=remnawave |
| remnawave_node_cpu_count | gauge | Node CPU count | node_uuid,app=remnawave |
| remnawave_node_cpu_load_avg_1m | gauge | Node CPU load average 1 minute | node_uuid,app=remnawave |
| remnawave_node_cpu_load_avg_5m | gauge | Node CPU load average 5 minutes | node_uuid,app=remnawave |
| remnawave_node_cpu_load_avg_15m | gauge | Node CPU load average 15 minutes | node_uuid,app=remnawave |
| remnawave_node_system_info | gauge | Node system info | node_uuid,arch,cpu_model,hostname,platform,release,version,app=remnawave |
| remnawave_node_basic_info | gauge | Node basic info | node_uuid,node_name,node_country_emoji,provider_name,tags,app=remnawave |
