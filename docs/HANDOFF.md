# Передача следующей сессии

Завершить проверку этапа 00; этап 01 выполнять только после отдельного запуска пользователем. Прочитать [отчёт](stages/STAGE_00_BOOTSTRAP.md), [lock](UPSTREAM_LOCK.md), [upstream-инструкции](UPSTREAM_AGENTS.md) и [политику](GATE_POLICY.md). Ветка rustwave-dev основана на d709bad01dc0ceacb20012a3afdf528eddfd061f; main опубликован на том же commit. Последний commit и чистоту дерева проверить через `git log -1` и `git status --short --branch`.

Bootstrap commit 5ef1552 опубликован в origin/rustwave-dev с GitHub noreply; за ним следует commit с уточнением отчёта. Git identity глобально не настроена. Fixtures и CI RustWave ещё не созданы. Go, Bun, Docker и gh локально не найдены. Тестов RustWave для повторного запуска пока нет. Не трогать production на VPS.
