# RustWave: правила работы

Выполняйте только порученный этап. Перед работой прочитайте docs/PROGRESS.md, docs/HANDOFF.md, docs/UPSTREAM_LOCK.md, относящиеся отчёты и [upstream-инструкции](docs/UPSTREAM_AGENTS.md); соблюдайте их при отсутствии противоречий. Проверяйте состояние Git и remote, не перезаписывайте чужие изменения, не используйте force push. Рабочая ветка — rustwave-dev. После каждого этапа обновляйте отчёт, progress и handoff, фиксируйте команды и фактические результаты.

Для каждого следующего этапа читайте его инструкции и общие правила из `codex/stage/`. Отчёты этапов сохраняйте в `docs/stages/`; обновляйте `docs/PROGRESS.md` и `docs/HANDOFF.md` и фиксируйте результаты в Git.

Приоритеты: сохранность данных, доказуемая 100% совместимость по полному инвентарю, равная функциональность SQLite/PostgreSQL, безопасность, затем минимизация RAM/CPU. Сохраняйте AGPL-3.0 и атрибуцию. Не считайте компиляцию доказательством совместимости.

Следуйте docs/GATE_POLICY.md: frontend callsite → method/path/shape, missing/null/empty, headers/errors/UI; детерминированные UTC/clock/test-only PRNG/DB fixtures; manifest expected/executed IDs и fail-closed no-skips; static roots/SPA/HEAD/404/gzip/WASM; Prometheus families/HELP/TYPE/labels/auth/enabled/disabled/system stats. Stable запрещён при любом обязательном пробеле. Отчёты сохраняйте в Markdown.

На VPS используйте только ssh de126-2, проверку host key и изолированные тесты; не затрагивайте production. При изменении host key остановитесь и запросите независимую проверку fingerprint. Секреты и данные БД не публикуйте.
