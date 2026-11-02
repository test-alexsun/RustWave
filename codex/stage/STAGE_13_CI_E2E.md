# ПРОМПТ 13 — GitHub Actions, matrix CI и полноценная differential E2E

> **Рекомендуемая модель Codex для этапа 13:** GPT-6 Astra, Thinking Effort: **Extra High**. Если модель недоступна в меню, выбери доступную GPT-6 с уровнем High/Extra High. Это рекомендация; выбор делается в интерфейсе Codex.

**Инструкция Codex GPT-6 High:** выполни **только этап 13** проекта RustWave. Ниже полный самостоятельный промпт для вставки в новую сессию Codex.

**Предыдущий отчёт:** `docs/stages/STAGE_12_*.md`. Прочитай и используй доказательные результаты, не воссоздавай их с нуля.


## Неизменяемый контекст проекта

- **Исходник (эталон):** `https://github.com/aaaSaZaN/gowave`.
- **Целевой GitHub:** `https://github.com/test-alexsun/RustWave` (уже создан; НЕ создавать новый репозиторий и НЕ менять оригинальный GoWave).
- **Тестовый VPS:** Debian 13, SSH-алиас **`de126-2`** из SSH-конфигурации машины, где запущен Codex. Использовать именно `ssh de126-2`, не выдумывать IP, логин или ключи.
- **Референсный commit GoWave, обнаруженный при подготовке:** `d709bad01dc0ceacb20012a3afdf528eddfd061f` (2026-11-01). Зафиксировать его в `docs/UPSTREAM_LOCK.md`; если он недоступен — описать причину, не подменять незаметно на `main`.
- **Конечный стек:** backend Rust (Axum/Tokio/SQLx/Serde), существующий React/TypeScript frontend; обе БД **SQLite и PostgreSQL** с выбором при установке; native systemd и Docker Compose на Debian 13.
- **P0:** не потерять данные и не повредить существующие установки. **P1:** максимальная доказанная эквивалентность API/функций; цель — 100% по полному проверяемому инвентарю. **P2:** одинаковая функциональность на обеих БД. **P3:** тесты/безопасность. Затем RAM, CPU, размер бинарника и образа.
- Сохранять исходную лицензию AGPL-3.0 и атрибуцию; проверить оригинальные LICENSE/NOTICE. Не считать успешно скомпилированный код доказательством 100% совместимости.

## Строгий протокол работы в КАЖДОЙ сессии

1. Прочитай `AGENTS.md` (сначала локальный, затем соответствующие upstream-инструкции), `docs/PROGRESS.md`, `docs/HANDOFF.md`, `docs/UPSTREAM_LOCK.md`, все относящиеся к этапу `docs/stages/STAGE_*.md` и матрицы в `docs/`. Если файлов нет только при первичной инициализации этапа 00 — создай их. Если отсутствуют позднее — выясни причину, не выдумывай содержимое.
2. Сверь `git remote -v`, `git status`, `git branch --show-current`, последние commits и актуальный remote HEAD. Рабочая интеграционная ветка — `rustwave-dev`; не перезаписывай чужие изменения и не применяй `push --force`. Не пушь в исходный GoWave. Все изменения коммитить и публиковать только в RustWave.
3. Исполняй **только текущий этап**; НЕ переходи к следующему самостоятельно. При необходимости разбей текущий этап на небольшие проверяемые подшаги с commits.
4. Записывай точные команды, exit codes, результаты тестов, commit SHA, ссылки на workflow runs, созданные/изменённые файлы и обнаруженные расхождения. Не помечай тест PASS, если он не был запущен.
5. В конце ОБЯЗАТЕЛЬНО обнови `docs/PROGRESS.md` (сводка по всем этапам), `docs/HANDOFF.md` (контекст следующей сессии) и `docs/stages/STAGE_NN_*.md` (полный отчёт именно этого этапа). Сделай commit и push в `rustwave-dev`, если доступ разрешён и пуш технически возможен. Если нет — запиши конкретный blocker и команды возобновления.
6. Для каждого действия на VPS сначала проверяй, что оно не затрагивает production. Тестируй в отдельном каталоге/контейнерах/сетях/портах и с ограниченными ресурсами. Не останавливай чужие сервисы. Секреты, токены, ключи, `.env` и содержимое БД НЕ коммить и НЕ вставляй в отчёты.
7. Если SSH сообщает **REMOTE HOST IDENTIFICATION HAS CHANGED**, не отключай проверку ключа и не удаляй `known_hosts` автоматически. Останови удалённые операции и потребуй независимой проверки нового ED25519 fingerprint; локальные задачи продолжай без VPS.
8. Не делай destructive DB-миграций, in-place изменений действующей установки или нагрузочных тестов на загруженном VPS без безопасной изоляции и актуального backup. Если нужен внешний доступ/согласие — пометь блокировку, не выдавай имитацию за результат.
9. Для статусов используй `PASS`, `PARTIAL`, `BLOCKED`, `FAIL`; `PASS` разрешён лишь при исполнении всех критериев этапа. Незавершённые задачи переносить в HANDOFF, не скрывая.

10. **Единая политика parity/gate:** прочитай `docs/GATE_POLICY.md` (если Stage 00 ещё не создал его — создай, прежде чем двигаться дальше) и поддерживай `docs/FRONTEND_API_SHAPE_MATRIX.md`, `docs/STATIC_SERVING_PARITY.md`, `docs/METRICS_PARITY.md` по мере охвата функций. Контракт определяется совместно реальным Go backend, закреплённым frontend и внешними schema/fixtures, а не только числом URL. Доказательства: точные команды + вывод + fixture IDs + источник ожидаемого результата.
11. **Determinism:** фиксируй время/UTC, locale, seeds в тестовой среде, состояние БД, порядок данных и контролируемые mock-сервисы; production CSPRNG/внешнее окружение не подменять. Любую нормализацию Go↔Rust перечислить явно по полям и обосновать; нельзя скрывать реальные различия. Недетерминированный/флакующий обязательный тест — не PASS.
12. **Fail-closed gate:** `skipped`, `ignored`, `xfail`, `todo`, `pending`, `filtered-out`, disabled и «not executed» **обязательных для текущего gate тестов** должны приводить к `PARTIAL/FAIL/BLOCKED`, не к PASS. Проанализируй результаты test runner программно, сверяй manifest запланированных тестов с фактически исполненными; запрещено уменьшать знаменатель покрытия или отключать тесты ради зелёного CI. До финального релиза полный gate без пропусков для всех обязательных сценариев.


## Общий формат отчёта STAGE_NN_*.md

```markdown
# STAGE NN — <название>
- Status: PASS | PARTIAL | BLOCKED | FAIL
- Started / Finished (UTC):
- Source SHA / RustWave HEAD SHA / Branch:
- Environment (OS, versions, DB):
## Что сделано (пути к файлам)
## Решения и обоснования
## Команды и результаты (PASS/FAIL/SKIPPED + объяснение)
## Совместимость API/БД (покрытие, расхождения, ссылки на fixtures)
## Безопасность и сохранность данных
## Результаты CI / ссылки
## Остаточные проблемы, риски, BLOCKER
## Что прочитать и выполнить на следующем этапе
```

В `docs/HANDOFF.md` обязательно: **какой этап выполнять далее**, последние реальные commits, branch, upstream SHA, несмерженные изменения, точные ссылки на отчёты/fixtures, команды быстрого повторного запуска тестов и риски. Никогда не подменять отчёт «всё работает» неподтверждённым заявлением.

## Задания этого этапа

### Задача
Построй CI как независимый строгий gate: нельзя выпускать RustWave при провале совместимости API, БД или безопасности.

### Выполнение
1. Настрой `rust.yml`: fmt/clippy/test/build/audit/deny (с объяснением лицензий), `frontend.yml`: Bun frozen lock/typecheck/format/test/build, `database-matrix.yml`: SQLite+PostgreSQL, `parity.yml`: pinned GoWave Go vs Rust с зафиксированными fixtures и реальным состоянием DB, `docker.yml`: image build + smoke для amd64/arm64, `installer.yml`: безопасный native/Docker test.
2. Используй pinned versions либо SHA для важных GitHub Actions и Rust/Bun/Go toolchains; минимальные permissions GitHub token; никакие секреты и тестовые дампы с PII в artifacts.
3. Настрой матрицу API методов: status/JSON/headers/auth/errors и state side effects, WebSocket/node/subscription/CLI E2E, обе БД, cold start, restarts, upgrades. Считай покрытие от **полного фактического инвентаря** GoWave, не только от имеющихся тестов. Zero fake success/stubs.
4. Обязательное правило release gate: все `P0/P1/P2/P3` tests зелёные и нет незакрытых блокеров. `SKIPPED` обязательного сценария = нельзя маркировать 100% parity. Отдельно учти объективно невозможные exhaustive доказательства: статус VERIFIED означает 100% из явно определённой проверяемой матрицы, а не математическую гарантию всех возможных входов.
5. Запусти CI на RustWave, изучи run/job logs и исправь дефекты; прикрепи точные ссылки на run URL и SHA, не просто зелёную галочку.
6. Проверь зависимости и секреты, differential harness против случайного изменения fixtures, reproducibility при разных DB/timezones/architecture.

### Обязательное усиление: strict release gate + determinism

1. Введи **manifest обязательных тестов** с точным набором ID: endpoint × scenario × DB, frontend consumer callsite × response shape × DB, static-serving route/headers/gzip × DB, metrics family/listener/auth × DB, subscriptions bytes, WS, CLI, jobs/outbox, install/update/migration. Сопоставляй expected IDs с actual executed IDs; `not_run`/`unknown_status` считаются провалом, а не отсутствием ошибки.
2. Для машинного анализа используй подходящие event reporters: `go test -json`, JSON/JUnit вывод Rust тестового runner, Bun frontend/browser test reporters. Парсер обязан детектировать `skipped`, `ignored`, `todo`, `pending`, `xfail`, `filtered-out`, `not_run` и незнакомые статусы; по умолчанию fail closed. Нельзя полагаться только на суммарный exit code (он может быть 0 при skipped).
3. В required GitHub Actions jobs **запрети** маскирующие конструкции `continue-on-error`, `|| true`, выключенные suites, пустую матрицу, обход блокирующей проверки. Проверь gate negative control: искусственно skipped обязательный тест в отдельном безопасном CI сценарии обязан привести к exit != 0. Не объединяй необязательные exploratory тесты с обязательным gate.
4. Запускай определённые наборы минимум повторно на чистом и одинаковом seed: фиксируй UTC/locale/clock/PRNG(test-only)/DB snapshots и эмулируй внешние RPC/Telegram/webhook responses. Для real concurrency добавь stress/repeat на обеих DB, записывай flaky ratio; flakiness FAIL до устранения. Не перезаписывай expected Go fixtures Rust-ответами.
5. Запусти frontend build/typecheck + consumer-contract tests + реальный browser E2E с одинаковым frontend против Go и Rust; сравни типы/поля/порядок/nullable/error envelope и после действий перезагрузку UI. Проходящие API route parity или TypeScript check **не** заменяют frontend/API-shape parity.
6. Добавь отдельные CI jobs для static-serving и metrics: mount/base path, SPA/404, GET/HEAD, gzip/precompressed WASM и schemas, HTTP headers, negative security; Prometheus family/HELP/TYPE/labels/units, auth, enabled/disabled, health и runtime stats. Обе БД в матрице там, где функциональность от них зависит; если не зависит — доказать и всё равно проверить не регрессирует на обеих.
7. Публикуй `docs/FRONTEND_API_PARITY.md`, `docs/STATIC_SERVING_PARITY.md`, `docs/METRICS_PARITY.md`, `docs/TEST_DETERMINISM.md` и `docs/RELEASE_GATE.md` с таблицей **expected / executed / passed / failed / skipped / ignored / not_run / flaky** по каждому required job. Подкрепи конкретными CI URLs, проверяй, что jobs required через branch protection/status checks там, где это доступно.

**Непреодолимое правило:** Gate PASS / stable release допускается только при `failed=0`, `skipped=0`, `ignored=0`, `xfail=0`, `todo=0`, `pending=0`, `not_run=0`, `unknown_status=0` для **всех обязательных сценариев**. Матрица покрытия должна быть 100% по полному зафиксированному инвентарю GoWave. Исключения не «whitelist skipped», а явно неполная совместимость и BLOCKED/PARTIAL без stable release.

### Обязательные MD-результаты
- `docs/stages/STAGE_13_CI_E2E.md`
- `docs/CI_CD.md`
- `docs/API_PARITY_FINAL_REVIEW.md`
- `docs/SECURITY_REVIEW.md`
- `docs/RELEASE_GATE.md`
- `docs/TEST_DETERMINISM.md`, `docs/FRONTEND_API_PARITY.md`, `docs/STATIC_SERVING_PARITY.md`, `docs/METRICS_PARITY.md`

### Gate PASS
Работает CI matrix, обе БД+frontend+API parity+security+installer протестированы; есть фактические URLs зелёных запусков и точная матрица coverage; при skipped/failed обязательных тестах — PARTIAL/FAIL.

## Команда завершения этапа 13

Сначала запиши/обнови все обязательные `.md` отчёты и сводный handoff, затем закоммить изменения и выполни `git push origin rustwave-dev` (без force). В финальном ответе покажи **фактический статус**, commit SHA, тесты с числом PASS/FAIL/SKIPPED, ссылку на CI, названия отчётов и текстовый список блокеров. **Не приступай к этапу 14**: пользователь запустит следующий промпт отдельно.
