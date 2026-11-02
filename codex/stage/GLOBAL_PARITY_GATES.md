# RustWave — глобальная политика строгой совместимости (версия 2)

**Обязательно для Codex GPT-6 High на всех этапах.** Источник: `aaaSaZaN/gowave` на SHA из `docs/UPSTREAM_LOCK.md`; назначение: `test-alexsun/RustWave`; испытательный Debian 13 VPS только через `ssh de126-2` с действующей проверкой host key. Никаких изменений production без отдельного разрешения.

## 1. Frontend/API-shape parity — P1

- Зафиксируй исходный React frontend, Bun lock, `@remnawave/backend-contract` и реальное поведение Go backend. Не обновляй их произвольно. Составь карту **frontend callsite / hook / parser / schema / экран (UI route) → endpoint, method, params, auth, response**.
- Для каждого свойства ответа сравни структуру и тип: отсутствует vs `null` vs пустое значение, string/number/boolean, integer precision и большие значения, date/time с timezone, nullable/optional поля, массивы и порядок (где релевантен), enum case, nested objects, paging totals, error envelope (`timestamp`, `path`, `message`, `errorCode`), статус, headers/cookies, события/side effects.
- API-форма валидируется двумя способами: **дифференциально Go↔Rust** и **потребительским контрактом существующего React** (скрипты/typecheck/схемы + браузерные сценарии и сетевые traces). Успешный OpenAPI check или 200 HTTP недостаточен. Нельзя ослаблять Zod/TypeScript schema или менять frontend под Rust; любое доказанное исключение документируется как расхождение.
- Отдельные обязательные сценарии: initial load, login/session refresh/logout, users list/filters/CRUD, squads, profiles/inbounds/hosts, settings, errors/validation/bulk, subscription UX, loading/empty states. Redact токены и персональные данные из trace.
- Выходные файлы RustWave: `docs/FRONTEND_API_SHAPE_MATRIX.md`, `docs/FRONTEND_API_PARITY.md` и executable fixtures/tests. Матрица указывает ID, client callsite, endpoint, Go fixture, Rust fixture, SQLite/PG status, integration test и результат `NOT_TESTED|FAIL|PASS`.

## 2. Determinism — P1/P3

- Зафиксируй версии исходного Go/React/контракта, Rust/dependencies и test toolchain, timestamps/UTC, locale, sorting, начальную DB fixture, clock и управляемый PRNG. Для безопасной криптографии production-источник случайности не заменяется; детерминизм только через dependency injection в test builds или semantically checked test vectors.
- Запусти сценарии многократно с чистого состояния, разным порядком запуска и по обеим БД. Контролируй job queue, outbox, background tick, network replies, retry/backoff, таймауты и конкуренцию. Реальный nondeterminism не маскировать глобальным удалением полей или широкими regex.
- Флакующий сценарий => FAIL до установления причины. При исправлении только корректируй source/tests, не перегенерируй эталон из Rust.

## 3. No-skips / fail-closed CI — P0/P3

- Для **обязательного набора текущего этапа и release gate** разрешён PASS только при `failed=0`, `skipped=0`, `ignored=0`, `xfail=0`, `pending=0`, `todo=0`, `not_run=0`, `unexpected_pass=0`, `unknown_status=0`. Отсутствующий результат трактуй как **not run**, не как PASS.
- Используй test manifest (ID сценария × frontend/backend × SQLite/PostgreSQL × architecture, если требуется) и машинный parser результатов (`go test -json`, Rust test runner, Bun test + browser e2e, JUnit/JSON), проверяющий полное множество исполненных обязательных ID. Не полагайся на grep по логам или общее число запусков. Сохраняй список обнаруженных skipped/ignored/filtered и причину.
- Если часть тестов относится к будущим этапам, помечай их `NOT_TESTED`; нельзя объявлять **глобальную** совместимость или stable release до полного закрытия. Не применяй запрет пропусков к явно отдельным необязательным exploratory тестам, но не учитывай их как доказательство parity.
- Не используй `continue-on-error`, blanket `if: false`, `|| true`, пустую матрицу, тестовые заглушки и подмену fixtures для обхода gate. Контроль проверять negative test: намеренно skipped обязательный кейс в изолированном workflow должен приводить к отказу релиза.

## 4. Static-serving parity — P1

- Сравни реальные GoWave static roots и порядок их поиска, `PANEL_BASE_PATH`, `index.html` SPA fallback, `GET/HEAD`, file vs extensionless 404, `/api/*` isolation, `/assets/*` fallback, `.gz` sibling / `Accept-Encoding` и `Content-Encoding`, `Content-Type`, `Content-Length`, caching (`ETag`, `Last-Modified`, `Cache-Control`), compression/Range (если поддерживается Go), path traversal / URL encoding, отсутствие отдачи приватных файлов.
- Проверяй одинаковый frontend/dist build, статус, заголовки и декодированное содержимое либо raw bytes где это семантически обязательно. Сверяй разные mount points и неправильные пути. Не подменяй Go 404 Rust SPA index.
- Обязательные файлы: `docs/STATIC_SERVING_PARITY.md`, differential tests `tests/compatibility/static/`.

## 5. Metrics parity — P1

- Снимай эталон Prometheus output, health/system statistics и поведение listener: `METRICS_ENABLED`, `METRICS_PORT` (исходный default 3001), bind/loopback, auth, запрещённые/неразрешённые запросы, HTTP method, Content-Type, ошибки.
- Сопоставь метрики по имени, `HELP`, `TYPE`, типу/ключам labels, units и стабильной семантике значений; проверь counters/gauges, отсутствие кардинальности/label drift и динамику метрик после контролируемых событий. Значения uptime/latency допускается сравнивать по объяснённым допускам при зафиксированном времени, но имена и shape метрик не нормализовать.
- Проверяй сценарии metrics enabled/disabled и метрики на SQLite/PG, не смешивай техническую экспозицию и внутренние панели статистики. Ожидания выведи из зафиксированной версии GoWave.
- Обязательные файлы: `docs/METRICS_PARITY.md`, differential tests `tests/compatibility/metrics/`.

## 6. Отчёты и решение gate

Каждый этап сохраняет `docs/stages/STAGE_NN_*.md`, обновляет `docs/PROGRESS.md` и `docs/HANDOFF.md`, указывает exact tested scope / expected IDs / executed IDs / passed / failed / skipped / not_run и URL конкретных CI runs. `PASS` возможен лишь когда **все задачи текущего этапа** и обязательные для него тесты реально выполнены. Для release: полная API/DB/frontend-shape/static/metrics/functions parity matrix без незакрытых обязательных сценариев и все CI gates PASS. Слово «100%» относится к объявленному проверяемому инвентарю, а не к математически доказанной эквивалентности всех возможных входов.
