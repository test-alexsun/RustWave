# RustWave — поэтапные промпты для Codex (комплект v3)

**Целевой репозиторий:** https://github.com/test-alexsun/RustWave  
**Исходник:** https://github.com/aaaSaZaN/gowave  
**Тестовый Debian 13:** SSH alias `de126-2`  
**Зафиксированный upstream SHA при подготовке:** `d709bad01dc0ceacb20012a3afdf528eddfd061f`

## Новое в комплекте v3

- Файл [`MODEL_AND_LAUNCH_GUIDE.md`](MODEL_AND_LAUNCH_GUIDE.md): **модель, уровень мышления и короткая команда для копирования** по каждому из 16 этапов.
- Рекомендация модели продублирована в заголовке каждого полного `STAGE_XX_*.md` (сама инструкция этапа сохранена).
- Требования v2 к frontend/API-shape, determinism/no-skips, static-serving и metrics остаются **обязательными** во всех 16 этапах и описаны в [`GLOBAL_PARITY_GATES.md`](GLOBAL_PARITY_GATES.md).
- Комплект предназначен для последовательного выполнения: один stage — один результат в `.md` с сохранением handoff, Git и CI. Инсталляция поддерживает **SQLite и PostgreSQL** с выбором на этапе 12.

### Куда положить промпты

Распакуй архив, затем скопируй файлы из папки `RustWave_Codex_Stages/` в каталог `codex/stages/` внутри локальной копии `test-alexsun/RustWave`. После этого запуски из `MODEL_AND_LAUNCH_GUIDE.md` смогут находить полные этапы по указанным путям. При первой инициализации пустого репозитория можно передать Codex полный текст `STAGE_00_BOOTSTRAP.md` напрямую; не требуется, чтобы файлы уже находились в GitHub.

## Как работать

1. Открой Codex на компьютере, где корректно настроен SSH alias `de126-2` и GitHub auth. Выбери модель/уровень мышления по `MODEL_AND_LAUNCH_GUIDE.md`.
2. Вставь содержимое **одного** `.md` файла с промптом STAGE_00, выполни его.
3. Убедись, что Codex создал отчёты в `docs/stages/`, обновил `docs/PROGRESS.md` и `docs/HANDOFF.md`, закоммитил изменения в `rustwave-dev` и показал реальный статус.
4. Для следующего этапа открой новый файл с промптом. Кодекс сначала перечитает отчёты и реальный код из RustWave; не полагается на память переписки.
5. При статусе `PARTIAL`, `BLOCKED` или `FAIL` не переходи к следующему этапу без устранения блокера или явной документированной стратегии его разрешения; используй `RESUME_STAGE.md`.
6. По окончании этапа 15 при зелёных gate можно выпускать стабильную RustWave.

## Усиление v2: обязательные parity gates

Добавлены три блокирующих набора требований (общая спецификация: [`GLOBAL_PARITY_GATES.md`](GLOBAL_PARITY_GATES.md)):

1. **Frontend/API-shape parity.** Существующий React/TypeScript frontend — полноценный потребительский контракт. На этапах **02, 08, 11, 13** проверяются точные типы/поля и состояния (`null` vs absent), обработка ошибок, отображение UI и network traces, а не только эндпоинты или OpenAPI. Результаты — `docs/FRONTEND_API_SHAPE_MATRIX.md`, `docs/FRONTEND_API_PARITY.md`.
2. **Determinism и No-skips release gate.** Тесты используют одинаковые fixtures/UTC/clock/test-seed и проверяют реальное исполнение всех обязательных ID. `skipped`, `ignored`, `todo`, `xfail`, `not_run`, flaky → **не PASS**, обязательный CI fail-closed. Для промежуточного этапа это относится к его in-scope тестам, для stable release — ко всему зафиксированному инвентарю.
3. **Static-serving + metrics parity.** Фиксируются Go baseline и Rust сравнение раздачи React/SPA/assets/HEAD/gzip/WASM и Prometheus listener/metric families/labels/auth/health. Главная реализация/закрытие — Stage 11, обязательные CI проверки — Stage 13.

**Stage 00** должен записать правила в `AGENTS.md` и `docs/GATE_POLICY.md` целевого RustWave; при продолжении с уже начатого этапа используйте `RESUME_STAGE.md`. Входные prompts обновлены, **сам GitHub-репозиторий этим комплектом не изменяется**.

## Этапы

| № | Промпт | Главное | Основной MD-результат |
|---|---|---|---|
| 00 | `STAGE_00_BOOTSTRAP.md` | Инициализация RustWave и безопасная проверка SSH | `docs/stages/STAGE_00_*.md` |
| 01 | `STAGE_01_AUDIT.md` | Инвентаризация возможностей GoWave и исходные метрики | `docs/stages/STAGE_01_*.md` |
| 02 | `STAGE_02_API_CONTRACT.md` | Полный API-контракт и эталонное дифференциальное тестирование | `docs/stages/STAGE_02_*.md` |
| 03 | `STAGE_03_DATABASE_DESIGN.md` | SQL-схемы, семантика данных и дизайн dual-DB | `docs/stages/STAGE_03_*.md` |
| 04 | `STAGE_04_RUST_CORE.md` | Rust workspace, конфигурация, Axum и первоначальный CI | `docs/stages/STAGE_04_*.md` |
| 05 | `STAGE_05_SQLITE.md` | SQLite implementation, совместимые миграции и тесты | `docs/stages/STAGE_05_*.md` |
| 06 | `STAGE_06_POSTGRES.md` | PostgreSQL adapter и единая семантика двух баз | `docs/stages/STAGE_06_*.md` |
| 07 | `STAGE_07_AUTH.md` | Авторизация, безопасность, JWT, tokens, cookies, passkey/OAuth | `docs/stages/STAGE_07_*.md` |
| 08 | `STAGE_08_DOMAIN_API.md` | Пользователи, squads, profiles, inbounds, hosts, системные настройки | `docs/stages/STAGE_08_*.md` |
| 09 | `STAGE_09_NODES.md` | Ноды, RPC/TLS, SSH WebSocket, outbox и фоновые задачи | `docs/stages/STAGE_09_*.md` |
| 10 | `STAGE_10_SUBSCRIPTIONS.md` | Подписки, шаблоны, форматтеры, crypto и byte-for-byte parity | `docs/stages/STAGE_10_*.md` |
| 11 | `STAGE_11_REMAINING_FEATURES.md` | Оставшиеся функции, CLI, уведомления, импорт/экспорт, мониторинг | `docs/stages/STAGE_11_*.md` |
| 12 | `STAGE_12_INSTALLER.md` | Интерактивный installer: SQLite/PostgreSQL + native/Docker | `docs/stages/STAGE_12_*.md` |
| 13 | `STAGE_13_CI_E2E.md` | GitHub Actions, matrix CI и полноценная differential E2E | `docs/stages/STAGE_13_*.md` |
| 14 | `STAGE_14_DEBIAN_BENCH.md` | Бенчмарки Go/Rust на Debian 13 de126-2 и оптимизация | `docs/stages/STAGE_14_*.md` |
| 15 | `STAGE_15_RELEASE.md` | Финальный аудит, документация и безопасный релиз | `docs/stages/STAGE_15_*.md` |

## Схема передачи результатов между сессиями

- `docs/UPSTREAM_LOCK.md` — точный эталонный GoWave commit SHA, лицензия, frontend и pin версии контракта.
- `docs/PROGRESS.md` — сводная таблица этапов, критерии gate, progress процент по проверяемому инвентарю.
- `docs/HANDOFF.md` — единая точка продолжения: ветка, commit, блокеры, следующий этап, быстрые тесты.
- `docs/stages/STAGE_XX_*.md` — полный технический отчёт этапа.
- `docs/API_PARITY_MATRIX.md` — все реальные endpoints и edge cases, с доказательствами Go↔Rust.
- `docs/FUNCTIONAL_PARITY_MATRIX.md` — полный функционал, включая фоновые задачи/CLI/ноды.
- `docs/DATABASE_PARITY_MATRIX.md` — тестовое подтверждение каждой операции на SQLite и PostgreSQL.
- `docs/benchmarks/` — методология и реальные измерения, исходные команды и результаты.

**Важно:** `RustWave` при проверке был созданным, но пустым репозиторием. STAGE_00 проверяет это заново и безопасно инициализирует проект. Наличие alias `de126-2` не гарантирует успешный SSH: host key должен пройти проверку, а удалённые тесты выполняются только в изоляции.

**100% совместимость** означает отсутствие известных расхождений и 100% пройденных обязательных сценариев по полному инвентарю, а не математическое доказательство эквивалентности всех возможных входов.
