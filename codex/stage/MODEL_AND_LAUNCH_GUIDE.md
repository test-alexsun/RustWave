# RustWave — выбор модели и короткие команды запуска этапов

**Проект:** https://github.com/test-alexsun/RustWave  
**Эталон:** https://github.com/aaaSaZaN/gowave  
**Debian 13:** `ssh de126-2`

Этот файл дополняет, а не заменяет 16 подробных `STAGE_XX_*.md` и `GLOBAL_PARITY_GATES.md`.

## Подготовка

1. Распакуй ZIP и скопируй все `.md` из `RustWave_Codex_Stages/` в **`codex/stage/`** локальной рабочей копии RustWave; не удаляй существующие файлы проекта. Коммитить сами промпты допустимо, но секреты из окружения — нет.
2. В интерфейсе Codex вручную выбери указанную модель и Thinking Effort. Сам текст команды не меняет модель.
3. Вставляй в Codex **ровно один** блок ниже. Codex должен прочитать исходный подробный промпт по указанному пути, а не полагаться на краткое описание.
4. После этапа проверяй `docs/stages/`, `docs/PROGRESS.md`, `docs/HANDOFF.md`, commits и CI; не переходи дальше при PARTIAL/BLOCKED/FAIL.
5. Никаких изменений действующих сервисов `de126-2` или production баз без отдельного разрешения. Test infrastructure — изолированная.

**Доступность моделей:** имена Astra/Sol/Terra приведены по предыдущим рекомендациям и могут отсутствовать в конкретной сборке Codex. Если модель не предлагается, используй наиболее сильную доступную модель GPT-6, `High` или `Extra High` (если доступен). Не вводи имя модели в поле чата вместо выбора в меню.

## Поэтапные команды (копировать отдельно)

### Этап 00: Инициализация репозитория, доступы, SSH, правила передачи этапов

**Модель:** GPT-6.1 Terra — **Thinking:** Medium

```text
Выполни только этап 00 проекта RustWave по полному промпту:
codex/stage/STAGE_00_BOOTSTRAP.md

Контекст:
- GitHub: https://github.com/test-alexsun/RustWave
- Эталон: https://github.com/aaaSaZaN/gowave
- VPS Debian 13: ssh de126-2 (только безопасные изолированные операции)

До начала прочитай AGENTS.md, docs/GATE_POLICY.md,
docs/UPSTREAM_LOCK.md, docs/PROGRESS.md, docs/HANDOFF.md,
релевантные отчёты завершённых этапов и
codex/stage/GLOBAL_PARITY_GATES.md.
Если эти файлы ещё не созданы на этапе 00 — создай по указанию STAGE_00.

Ключевой фокус: read-only SSH preflight, upstream lock, AGENTS/GATE_POLICY.
Сохраняй 100% API/frontend-shape parity как цель, подтверждаемую
дифференциальными тестами Go↔Rust; полную функциональность
на SQLite и PostgreSQL; статические ресурсы и метрики.
Для обязательных тестов этапа: deterministic fixtures,
no skipped/ignored/xfail/todo/not_run, fail-closed gate.
Никаких фиктивных PASS и скрытых несовпадений.

После работы создай docs/stages/STAGE_00_BOOTSTRAP.md, обнови
PROGRESS.md и HANDOFF.md, сохрани фактические тесты,
commit SHA, CI URL и блокеры; безопасно commit и push
в разрешённую ветку RustWave.
Остановись после текущего этапа, не запускай следующий.
```

### Этап 01: Полный аудит GoWave и исходные измерения

**Модель:** GPT-6 Astra — **Thinking:** High

```text
Выполни только этап 01 проекта RustWave по полному промпту:
codex/stage/STAGE_01_AUDIT.md

Контекст:
- GitHub: https://github.com/test-alexsun/RustWave
- Эталон: https://github.com/aaaSaZaN/gowave
- VPS Debian 13: ssh de126-2 (только безопасные изолированные операции)

До начала прочитай AGENTS.md, docs/GATE_POLICY.md,
docs/UPSTREAM_LOCK.md, docs/PROGRESS.md, docs/HANDOFF.md,
релевантные отчёты завершённых этапов и
codex/stage/GLOBAL_PARITY_GATES.md.
Если эти файлы ещё не созданы на этапе 00 — создай по указанию STAGE_00.

Ключевой фокус: полная функциональная матрица, baseline, без догадок.
Сохраняй 100% API/frontend-shape parity как цель, подтверждаемую
дифференциальными тестами Go↔Rust; полную функциональность
на SQLite и PostgreSQL; статические ресурсы и метрики.
Для обязательных тестов этапа: deterministic fixtures,
no skipped/ignored/xfail/todo/not_run, fail-closed gate.
Никаких фиктивных PASS и скрытых несовпадений.

После работы создай docs/stages/STAGE_01_AUDIT.md, обнови
PROGRESS.md и HANDOFF.md, сохрани фактические тесты,
commit SHA, CI URL и блокеры; безопасно commit и push
в разрешённую ветку RustWave.
Остановись после текущего этапа, не запускай следующий.
```

### Этап 02: Контракт API и потребительский контракт React

**Модель:** GPT-6 Astra — **Thinking:** Extra High

```text
Выполни только этап 02 проекта RustWave по полному промпту:
codex/stage/STAGE_02_API_CONTRACT.md

Контекст:
- GitHub: https://github.com/test-alexsun/RustWave
- Эталон: https://github.com/aaaSaZaN/gowave
- VPS Debian 13: ssh de126-2 (только безопасные изолированные операции)

До начала прочитай AGENTS.md, docs/GATE_POLICY.md,
docs/UPSTREAM_LOCK.md, docs/PROGRESS.md, docs/HANDOFF.md,
релевантные отчёты завершённых этапов и
codex/stage/GLOBAL_PARITY_GATES.md.
Если эти файлы ещё не созданы на этапе 00 — создай по указанию STAGE_00.

Ключевой фокус: frontend callsites, JSON shape, Go fixtures, determinism.
Сохраняй 100% API/frontend-shape parity как цель, подтверждаемую
дифференциальными тестами Go↔Rust; полную функциональность
на SQLite и PostgreSQL; статические ресурсы и метрики.
Для обязательных тестов этапа: deterministic fixtures,
no skipped/ignored/xfail/todo/not_run, fail-closed gate.
Никаких фиктивных PASS и скрытых несовпадений.

После работы создай docs/stages/STAGE_02_API_CONTRACT.md, обнови
PROGRESS.md и HANDOFF.md, сохрани фактические тесты,
commit SHA, CI URL и блокеры; безопасно commit и push
в разрешённую ветку RustWave.
Остановись после текущего этапа, не запускай следующий.
```

### Этап 03: Дизайн SQLite и PostgreSQL и совместимости схем

**Модель:** GPT-6 Astra — **Thinking:** High

```text
Выполни только этап 03 проекта RustWave по полному промпту:
codex/stage/STAGE_03_DATABASE_DESIGN.md

Контекст:
- GitHub: https://github.com/test-alexsun/RustWave
- Эталон: https://github.com/aaaSaZaN/gowave
- VPS Debian 13: ssh de126-2 (только безопасные изолированные операции)

До начала прочитай AGENTS.md, docs/GATE_POLICY.md,
docs/UPSTREAM_LOCK.md, docs/PROGRESS.md, docs/HANDOFF.md,
релевантные отчёты завершённых этапов и
codex/stage/GLOBAL_PARITY_GATES.md.
Если эти файлы ещё не созданы на этапе 00 — создай по указанию STAGE_00.

Ключевой фокус: сохранение миграций, UUID, транзакций, обе БД.
Сохраняй 100% API/frontend-shape parity как цель, подтверждаемую
дифференциальными тестами Go↔Rust; полную функциональность
на SQLite и PostgreSQL; статические ресурсы и метрики.
Для обязательных тестов этапа: deterministic fixtures,
no skipped/ignored/xfail/todo/not_run, fail-closed gate.
Никаких фиктивных PASS и скрытых несовпадений.

После работы создай docs/stages/STAGE_03_DATABASE_DESIGN.md, обнови
PROGRESS.md и HANDOFF.md, сохрани фактические тесты,
commit SHA, CI URL и блокеры; безопасно commit и push
в разрешённую ветку RustWave.
Остановись после текущего этапа, не запускай следующий.
```

### Этап 04: Каркас Rust/Axum/Tokio/SQLx и начальный CI

**Модель:** GPT-6.1 Sol — **Thinking:** High

```text
Выполни только этап 04 проекта RustWave по полному промпту:
codex/stage/STAGE_04_RUST_CORE.md

Контекст:
- GitHub: https://github.com/test-alexsun/RustWave
- Эталон: https://github.com/aaaSaZaN/gowave
- VPS Debian 13: ssh de126-2 (только безопасные изолированные операции)

До начала прочитай AGENTS.md, docs/GATE_POLICY.md,
docs/UPSTREAM_LOCK.md, docs/PROGRESS.md, docs/HANDOFF.md,
релевантные отчёты завершённых этапов и
codex/stage/GLOBAL_PARITY_GATES.md.
Если эти файлы ещё не созданы на этапе 00 — создай по указанию STAGE_00.

Ключевой фокус: рабочая компиляция, tests, без фиктивных endpoints.
Сохраняй 100% API/frontend-shape parity как цель, подтверждаемую
дифференциальными тестами Go↔Rust; полную функциональность
на SQLite и PostgreSQL; статические ресурсы и метрики.
Для обязательных тестов этапа: deterministic fixtures,
no skipped/ignored/xfail/todo/not_run, fail-closed gate.
Никаких фиктивных PASS и скрытых несовпадений.

После работы создай docs/stages/STAGE_04_RUST_CORE.md, обнови
PROGRESS.md и HANDOFF.md, сохрани фактические тесты,
commit SHA, CI URL и блокеры; безопасно commit и push
в разрешённую ветку RustWave.
Остановись после текущего этапа, не запускай следующий.
```

### Этап 05: Полноценный SQLite backend

**Модель:** GPT-6.1 Sol — **Thinking:** High

```text
Выполни только этап 05 проекта RustWave по полному промпту:
codex/stage/STAGE_05_SQLITE.md

Контекст:
- GitHub: https://github.com/test-alexsun/RustWave
- Эталон: https://github.com/aaaSaZaN/gowave
- VPS Debian 13: ssh de126-2 (только безопасные изолированные операции)

До начала прочитай AGENTS.md, docs/GATE_POLICY.md,
docs/UPSTREAM_LOCK.md, docs/PROGRESS.md, docs/HANDOFF.md,
релевантные отчёты завершённых этапов и
codex/stage/GLOBAL_PARITY_GATES.md.
Если эти файлы ещё не созданы на этапе 00 — создай по указанию STAGE_00.

Ключевой фокус: WAL, migrations, backup, корректность.
Сохраняй 100% API/frontend-shape parity как цель, подтверждаемую
дифференциальными тестами Go↔Rust; полную функциональность
на SQLite и PostgreSQL; статические ресурсы и метрики.
Для обязательных тестов этапа: deterministic fixtures,
no skipped/ignored/xfail/todo/not_run, fail-closed gate.
Никаких фиктивных PASS и скрытых несовпадений.

После работы создай docs/stages/STAGE_05_SQLITE.md, обнови
PROGRESS.md и HANDOFF.md, сохрани фактические тесты,
commit SHA, CI URL и блокеры; безопасно commit и push
в разрешённую ветку RustWave.
Остановись после текущего этапа, не запускай следующий.
```

### Этап 06: PostgreSQL backend и SQL-паритет с SQLite

**Модель:** GPT-6 Astra — **Thinking:** High

```text
Выполни только этап 06 проекта RustWave по полному промпту:
codex/stage/STAGE_06_POSTGRES.md

Контекст:
- GitHub: https://github.com/test-alexsun/RustWave
- Эталон: https://github.com/aaaSaZaN/gowave
- VPS Debian 13: ssh de126-2 (только безопасные изолированные операции)

До начала прочитай AGENTS.md, docs/GATE_POLICY.md,
docs/UPSTREAM_LOCK.md, docs/PROGRESS.md, docs/HANDOFF.md,
релевантные отчёты завершённых этапов и
codex/stage/GLOBAL_PARITY_GATES.md.
Если эти файлы ещё не созданы на этапе 00 — создай по указанию STAGE_00.

Ключевой фокус: транзакции, схемы, стабильная интерпретация полей.
Сохраняй 100% API/frontend-shape parity как цель, подтверждаемую
дифференциальными тестами Go↔Rust; полную функциональность
на SQLite и PostgreSQL; статические ресурсы и метрики.
Для обязательных тестов этапа: deterministic fixtures,
no skipped/ignored/xfail/todo/not_run, fail-closed gate.
Никаких фиктивных PASS и скрытых несовпадений.

После работы создай docs/stages/STAGE_06_POSTGRES.md, обнови
PROGRESS.md и HANDOFF.md, сохрани фактические тесты,
commit SHA, CI URL и блокеры; безопасно commit и push
в разрешённую ветку RustWave.
Остановись после текущего этапа, не запускай следующий.
```

### Этап 07: Аутентификация и авторизация

**Модель:** GPT-6 Astra — **Thinking:** Extra High

```text
Выполни только этап 07 проекта RustWave по полному промпту:
codex/stage/STAGE_07_AUTH.md

Контекст:
- GitHub: https://github.com/test-alexsun/RustWave
- Эталон: https://github.com/aaaSaZaN/gowave
- VPS Debian 13: ssh de126-2 (только безопасные изолированные операции)

До начала прочитай AGENTS.md, docs/GATE_POLICY.md,
docs/UPSTREAM_LOCK.md, docs/PROGRESS.md, docs/HANDOFF.md,
релевантные отчёты завершённых этапов и
codex/stage/GLOBAL_PARITY_GATES.md.
Если эти файлы ещё не созданы на этапе 00 — создай по указанию STAGE_00.

Ключевой фокус: JWT/cookies/OAuth/permissions, безопасность.
Сохраняй 100% API/frontend-shape parity как цель, подтверждаемую
дифференциальными тестами Go↔Rust; полную функциональность
на SQLite и PostgreSQL; статические ресурсы и метрики.
Для обязательных тестов этапа: deterministic fixtures,
no skipped/ignored/xfail/todo/not_run, fail-closed gate.
Никаких фиктивных PASS и скрытых несовпадений.

После работы создай docs/stages/STAGE_07_AUTH.md, обнови
PROGRESS.md и HANDOFF.md, сохрани фактические тесты,
commit SHA, CI URL и блокеры; безопасно commit и push
в разрешённую ветку RustWave.
Остановись после текущего этапа, не запускай следующий.
```

### Этап 08: Domain API, profiles/inbounds/hosts, React parity

**Модель:** GPT-6 Astra — **Thinking:** Extra High

```text
Выполни только этап 08 проекта RustWave по полному промпту:
codex/stage/STAGE_08_DOMAIN_API.md

Контекст:
- GitHub: https://github.com/test-alexsun/RustWave
- Эталон: https://github.com/aaaSaZaN/gowave
- VPS Debian 13: ssh de126-2 (только безопасные изолированные операции)

До начала прочитай AGENTS.md, docs/GATE_POLICY.md,
docs/UPSTREAM_LOCK.md, docs/PROGRESS.md, docs/HANDOFF.md,
релевантные отчёты завершённых этапов и
codex/stage/GLOBAL_PARITY_GATES.md.
Если эти файлы ещё не созданы на этапе 00 — создай по указанию STAGE_00.

Ключевой фокус: реальные UI и Go↔Rust E2E, обе БД.
Сохраняй 100% API/frontend-shape parity как цель, подтверждаемую
дифференциальными тестами Go↔Rust; полную функциональность
на SQLite и PostgreSQL; статические ресурсы и метрики.
Для обязательных тестов этапа: deterministic fixtures,
no skipped/ignored/xfail/todo/not_run, fail-closed gate.
Никаких фиктивных PASS и скрытых несовпадений.

После работы создай docs/stages/STAGE_08_DOMAIN_API.md, обнови
PROGRESS.md и HANDOFF.md, сохрани фактические тесты,
commit SHA, CI URL и блокеры; безопасно commit и push
в разрешённую ветку RustWave.
Остановись после текущего этапа, не запускай следующий.
```

### Этап 09: Nodes, RPC, TLS, WebSocket и очередь задач

**Модель:** GPT-6 Astra — **Thinking:** High

```text
Выполни только этап 09 проекта RustWave по полному промпту:
codex/stage/STAGE_09_NODES.md

Контекст:
- GitHub: https://github.com/test-alexsun/RustWave
- Эталон: https://github.com/aaaSaZaN/gowave
- VPS Debian 13: ssh de126-2 (только безопасные изолированные операции)

До начала прочитай AGENTS.md, docs/GATE_POLICY.md,
docs/UPSTREAM_LOCK.md, docs/PROGRESS.md, docs/HANDOFF.md,
релевантные отчёты завершённых этапов и
codex/stage/GLOBAL_PARITY_GATES.md.
Если эти файлы ещё не созданы на этапе 00 — создай по указанию STAGE_00.

Ключевой фокус: outbox, recovery, безопасность тестовых нод.
Сохраняй 100% API/frontend-shape parity как цель, подтверждаемую
дифференциальными тестами Go↔Rust; полную функциональность
на SQLite и PostgreSQL; статические ресурсы и метрики.
Для обязательных тестов этапа: deterministic fixtures,
no skipped/ignored/xfail/todo/not_run, fail-closed gate.
Никаких фиктивных PASS и скрытых несовпадений.

После работы создай docs/stages/STAGE_09_NODES.md, обнови
PROGRESS.md и HANDOFF.md, сохрани фактические тесты,
commit SHA, CI URL и блокеры; безопасно commit и push
в разрешённую ветку RustWave.
Остановись после текущего этапа, не запускай следующий.
```

### Этап 10: Форматы подписок и криптография

**Модель:** GPT-6 Astra — **Thinking:** Extra High

```text
Выполни только этап 10 проекта RustWave по полному промпту:
codex/stage/STAGE_10_SUBSCRIPTIONS.md

Контекст:
- GitHub: https://github.com/test-alexsun/RustWave
- Эталон: https://github.com/aaaSaZaN/gowave
- VPS Debian 13: ssh de126-2 (только безопасные изолированные операции)

До начала прочитай AGENTS.md, docs/GATE_POLICY.md,
docs/UPSTREAM_LOCK.md, docs/PROGRESS.md, docs/HANDOFF.md,
релевантные отчёты завершённых этапов и
codex/stage/GLOBAL_PARITY_GATES.md.
Если эти файлы ещё не созданы на этапе 00 — создай по указанию STAGE_00.

Ключевой фокус: byte parity, golden fixtures, deterministic vectors.
Сохраняй 100% API/frontend-shape parity как цель, подтверждаемую
дифференциальными тестами Go↔Rust; полную функциональность
на SQLite и PostgreSQL; статические ресурсы и метрики.
Для обязательных тестов этапа: deterministic fixtures,
no skipped/ignored/xfail/todo/not_run, fail-closed gate.
Никаких фиктивных PASS и скрытых несовпадений.

После работы создай docs/stages/STAGE_10_SUBSCRIPTIONS.md, обнови
PROGRESS.md и HANDOFF.md, сохрани фактические тесты,
commit SHA, CI URL и блокеры; безопасно commit и push
в разрешённую ветку RustWave.
Остановись после текущего этапа, не запускай следующий.
```

### Этап 11: Остальные функции, static-serving и metrics

**Модель:** GPT-6 Astra — **Thinking:** High

```text
Выполни только этап 11 проекта RustWave по полному промпту:
codex/stage/STAGE_11_REMAINING_FEATURES.md

Контекст:
- GitHub: https://github.com/test-alexsun/RustWave
- Эталон: https://github.com/aaaSaZaN/gowave
- VPS Debian 13: ssh de126-2 (только безопасные изолированные операции)

До начала прочитай AGENTS.md, docs/GATE_POLICY.md,
docs/UPSTREAM_LOCK.md, docs/PROGRESS.md, docs/HANDOFF.md,
релевантные отчёты завершённых этапов и
codex/stage/GLOBAL_PARITY_GATES.md.
Если эти файлы ещё не созданы на этапе 00 — создай по указанию STAGE_00.

Ключевой фокус: SPA, gzip/WASM, Prometheus family/schema/auth.
Сохраняй 100% API/frontend-shape parity как цель, подтверждаемую
дифференциальными тестами Go↔Rust; полную функциональность
на SQLite и PostgreSQL; статические ресурсы и метрики.
Для обязательных тестов этапа: deterministic fixtures,
no skipped/ignored/xfail/todo/not_run, fail-closed gate.
Никаких фиктивных PASS и скрытых несовпадений.

После работы создай docs/stages/STAGE_11_REMAINING_FEATURES.md, обнови
PROGRESS.md и HANDOFF.md, сохрани фактические тесты,
commit SHA, CI URL и блокеры; безопасно commit и push
в разрешённую ветку RustWave.
Остановись после текущего этапа, не запускай следующий.
```

### Этап 12: Инсталлятор Debian 13 с выбором БД

**Модель:** GPT-6.1 Sol — **Thinking:** High

```text
Выполни только этап 12 проекта RustWave по полному промпту:
codex/stage/STAGE_12_INSTALLER.md

Контекст:
- GitHub: https://github.com/test-alexsun/RustWave
- Эталон: https://github.com/aaaSaZaN/gowave
- VPS Debian 13: ssh de126-2 (только безопасные изолированные операции)

До начала прочитай AGENTS.md, docs/GATE_POLICY.md,
docs/UPSTREAM_LOCK.md, docs/PROGRESS.md, docs/HANDOFF.md,
релевантные отчёты завершённых этапов и
codex/stage/GLOBAL_PARITY_GATES.md.
Если эти файлы ещё не созданы на этапе 00 — создай по указанию STAGE_00.

Ключевой фокус: SQLite/PostgreSQL, native/Docker, rollback.
Сохраняй 100% API/frontend-shape parity как цель, подтверждаемую
дифференциальными тестами Go↔Rust; полную функциональность
на SQLite и PostgreSQL; статические ресурсы и метрики.
Для обязательных тестов этапа: deterministic fixtures,
no skipped/ignored/xfail/todo/not_run, fail-closed gate.
Никаких фиктивных PASS и скрытых несовпадений.

После работы создай docs/stages/STAGE_12_INSTALLER.md, обнови
PROGRESS.md и HANDOFF.md, сохрани фактические тесты,
commit SHA, CI URL и блокеры; безопасно commit и push
в разрешённую ветку RustWave.
Остановись после текущего этапа, не запускай следующий.
```

### Этап 13: Строгие GitHub Actions и E2E release gates

**Модель:** GPT-6 Astra — **Thinking:** Extra High

```text
Выполни только этап 13 проекта RustWave по полному промпту:
codex/stage/STAGE_13_CI_E2E.md

Контекст:
- GitHub: https://github.com/test-alexsun/RustWave
- Эталон: https://github.com/aaaSaZaN/gowave
- VPS Debian 13: ssh de126-2 (только безопасные изолированные операции)

До начала прочитай AGENTS.md, docs/GATE_POLICY.md,
docs/UPSTREAM_LOCK.md, docs/PROGRESS.md, docs/HANDOFF.md,
релевантные отчёты завершённых этапов и
codex/stage/GLOBAL_PARITY_GATES.md.
Если эти файлы ещё не созданы на этапе 00 — создай по указанию STAGE_00.

Ключевой фокус: expected vs executed IDs, no skipped, frontend/static/metrics.
Сохраняй 100% API/frontend-shape parity как цель, подтверждаемую
дифференциальными тестами Go↔Rust; полную функциональность
на SQLite и PostgreSQL; статические ресурсы и метрики.
Для обязательных тестов этапа: deterministic fixtures,
no skipped/ignored/xfail/todo/not_run, fail-closed gate.
Никаких фиктивных PASS и скрытых несовпадений.

После работы создай docs/stages/STAGE_13_CI_E2E.md, обнови
PROGRESS.md и HANDOFF.md, сохрани фактические тесты,
commit SHA, CI URL и блокеры; безопасно commit и push
в разрешённую ветку RustWave.
Остановись после текущего этапа, не запускай следующий.
```

### Этап 14: Бенчмарки Go и Rust на SSH de126-2

**Модель:** GPT-6.1 Sol — **Thinking:** High

```text
Выполни только этап 14 проекта RustWave по полному промпту:
codex/stage/STAGE_14_DEBIAN_BENCH.md

Контекст:
- GitHub: https://github.com/test-alexsun/RustWave
- Эталон: https://github.com/aaaSaZaN/gowave
- VPS Debian 13: ssh de126-2 (только безопасные изолированные операции)

До начала прочитай AGENTS.md, docs/GATE_POLICY.md,
docs/UPSTREAM_LOCK.md, docs/PROGRESS.md, docs/HANDOFF.md,
релевантные отчёты завершённых этапов и
codex/stage/GLOBAL_PARITY_GATES.md.
Если эти файлы ещё не созданы на этапе 00 — создай по указанию STAGE_00.

Ключевой фокус: Go/Rust × SQLite/PG, реальные измерения.
Сохраняй 100% API/frontend-shape parity как цель, подтверждаемую
дифференциальными тестами Go↔Rust; полную функциональность
на SQLite и PostgreSQL; статические ресурсы и метрики.
Для обязательных тестов этапа: deterministic fixtures,
no skipped/ignored/xfail/todo/not_run, fail-closed gate.
Никаких фиктивных PASS и скрытых несовпадений.

После работы создай docs/stages/STAGE_14_DEBIAN_BENCH.md, обнови
PROGRESS.md и HANDOFF.md, сохрани фактические тесты,
commit SHA, CI URL и блокеры; безопасно commit и push
в разрешённую ветку RustWave.
Остановись после текущего этапа, не запускай следующий.
```

### Этап 15: Независимая финальная проверка и release candidate

**Модель:** GPT-6 Astra — **Thinking:** Extra High

```text
Выполни только этап 15 проекта RustWave по полному промпту:
codex/stage/STAGE_15_RELEASE.md

Контекст:
- GitHub: https://github.com/test-alexsun/RustWave
- Эталон: https://github.com/aaaSaZaN/gowave
- VPS Debian 13: ssh de126-2 (только безопасные изолированные операции)

До начала прочитай AGENTS.md, docs/GATE_POLICY.md,
docs/UPSTREAM_LOCK.md, docs/PROGRESS.md, docs/HANDOFF.md,
релевантные отчёты завершённых этапов и
codex/stage/GLOBAL_PARITY_GATES.md.
Если эти файлы ещё не созданы на этапе 00 — создай по указанию STAGE_00.

Ключевой фокус: все обязательные gates и безопасная публикация.
Сохраняй 100% API/frontend-shape parity как цель, подтверждаемую
дифференциальными тестами Go↔Rust; полную функциональность
на SQLite и PostgreSQL; статические ресурсы и метрики.
Для обязательных тестов этапа: deterministic fixtures,
no skipped/ignored/xfail/todo/not_run, fail-closed gate.
Никаких фиктивных PASS и скрытых несовпадений.

После работы создай docs/stages/STAGE_15_RELEASE.md, обнови
PROGRESS.md и HANDOFF.md, сохрани фактические тесты,
commit SHA, CI URL и блокеры; безопасно commit и push
в разрешённую ветку RustWave.
Остановись после текущего этапа, не запускай следующий.
```

## Продолжить текущий этап после исчерпания лимита

```text
Продолжи только незавершённый этап RustWave. Прочитай
AGENTS.md, docs/GATE_POLICY.md, docs/PROGRESS.md,
docs/HANDOFF.md, docs/UPSTREAM_LOCK.md,
последний docs/stages/STAGE_*.md и
codex/stage/RESUME_STAGE.md.
Проверь git status/branch, последний commit, CI, тесты,
открытые блокеры; не повторяй уже завершённую работу.
Соблюдай GLOBAL_PARITY_GATES.md, требования SQLite/PG
и защиту VPS de126-2. Доделай текущий этап, обнови
MD-отчёты, сделай commit и push при наличии доступа.
Не переходи к следующему этапу автоматически.
```
