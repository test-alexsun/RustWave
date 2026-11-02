# Обязательные gates

Полный нормативный текст: [GLOBAL_PARITY_GATES.md](../codex/stage/GLOBAL_PARITY_GATES.md). Контракт определяется Go backend, закреплённым frontend и внешними схемами и fixtures. HTTP 200 и OpenAPI недостаточны.

Frontend: карта callsite/hook/parser/schema/UI route → method/path/params/auth/response; сравнение missing/null/empty, типов, точности чисел, времени, порядка, enum, вложенности, paging, ошибок, headers/cookies и side effects. Нужны differential Go↔Rust и потребительские проверки React, включая login, CRUD, settings, subscriptions и empty/error states. Не ослаблять схемы ради прохождения.

Детерминизм: pin версий, UTC, locale, clock, сортировки, чистых DB fixtures и test-only PRNG; контролировать сеть, фоновые задачи и конкуренцию; повторять в разных порядках на обеих БД. Production CSPRNG не подменять; нормализацию каждого поля обосновать. Flaky — FAIL.

Gate fail-closed: manifest обязательных ID и машинное сопоставление expected/executed; failed, skipped, ignored, xfail, todo, pending, not_run, unexpected_pass, unknown и filtered-out исключают PASS. Отсутствующий результат — not_run. Проверить отрицательным тестом. Не уменьшать покрытие и не подменять fixtures. Stable запрещён при любом незакрытом обязательном сценарии.

Static: сравнивать roots, base path, SPA fallback, GET/HEAD, 404, API/assets isolation, gzip, WASM и MIME, cache, range, traversal и приватные файлы. Metrics: Prometheus families, HELP, TYPE, labels, units и семантику, listener, auth, enabled/disabled и system stats на обеих БД. См. отдельные матрицы; не считать NOT_TESTED прохождением.
