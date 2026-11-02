# ПРОМПТ 02 — Полный API-контракт и эталонное дифференциальное тестирование

> **Рекомендуемая модель Codex для этапа 02:** GPT-6 Astra, Thinking Effort: **Extra High**. Если модель недоступна в меню, выбери доступную GPT-6 с уровнем High/Extra High. Это рекомендация; выбор делается в интерфейсе Codex.

**Инструкция Codex GPT-6 High:** выполни **только этап 02** проекта RustWave. Ниже полный самостоятельный промпт для вставки в новую сессию Codex.

**Предыдущий отчёт:** `docs/stages/STAGE_01_*.md`. Прочитай и используй доказательные результаты, не воссоздавай их с нуля.


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
До переноса backend подготовь эталонную систему доказательства **100% API-совместимости**. Список роутов — недостаточная проверка: должны совпадать тела ответов, ошибки, авторизация и побочные эффекты.

### Выполнение
1. Разбери `backend-go/internal/contracts/commands.json`, `openapi.json`, скрипты `scripts/export-contract.cjs`, `scripts/validate-contract.cjs`, тесты `parity_test.go`, `probe_test.go`, `mutation_probe_test.go` и весь router включая небазовые/публичные/WS/CLI пути. Зафиксируй `@remnawave/backend-contract` и его SHA.
2. Создай полный инвентарь API: method, path, params, query/body, auth, roles/scopes, статус, ответ/errorCode, cookies/headers, DB side effects, события, websocket frame semantics. Не путай «внешний Remnawave контракт» с реальным поведением зафиксированного GoWave; эталон — последний.
3. Создай инструментарий differential tests против реального Go backend на **изолированных** DB. Сценарии: happy path, отсутствующие/невалидные поля, границы, пагинация, ошибки, 401/403, 404, 409, 501, сложные мутации, токены, заголовки, таймзоны, подписки и WS. Снимай ожидаемые результаты **с Go**.
4. Для POST/PUT/PATCH/DELETE фиксируй state before/after, side effects, задания outbox. Для недетерминированных полей реализуй строго документированную нормализацию (время, random UUID); запрещены маскировка реальных ошибок и широкое игнорирование JSON-полей. Подписки/крипто тестируй golden bytes в подходящих сценариях.
5. Сохрани fixtures без секретов/PII, скрипты запуска и автоматическую матрицу `NOT_TESTED | FAIL | PASS` по каждому endpoint × scenario × DB, метрики покрытия как числитель/знаменатель.
6. Сверь проверяемые факты с существующими `subscription-diff`, `golden`, `matrix`, `http.json.gz` fixtures. Не обновляй эталон «по выходу Rust».

### Обязательное усиление: frontend/API-shape baseline

1. Пройди весь `frontend/src/` и существующий React клиент: API hooks, Axios, `@remnawave/backend-contract`, Zod/TypeScript schema, consumers, error handlers, cookies, WS; для каждого callsite укажи UI route/component и используемые поля. Не делай вывод о совместимости из OpenAPI или одного HTTP 200.
2. Создай `docs/FRONTEND_API_SHAPE_MATRIX.md`: `callsite → method/path → response/error/header shape → Go fixture → Rust fixture → test ID → SQLite/PG`. Типы проверять глубоко: **missing/null/empty**, arrays (включая порядок), enum/case, даты, precision чисел, nested optional, errors, pagination, `response` envelope и system health. На текущем этапе Rust поля могут быть `NOT_TESTED`, baseline Go обязан быть собран.
3. Сними HTTP fixtures реального Go (без PII/secrets) и JSON-schema/consumer assertions; добавь browser network traces из эталонного React там, где есть среда. Фиксируй точный frontend commit/build/lock. Проверь не только успешные ответы, но также 400/401/403/404/409/501, сортировку, bulk/actions и mutation side effects.
4. Внеси в API-инвентарь **не-JSON HTTP**: static assets, SPA маршруты, HEAD, gzip и metrics endpoints. Создай базовые `docs/STATIC_SERVING_PARITY.md` и `docs/METRICS_PARITY.md` с Go baseline/status `NOT_TESTED` для Rust; запиши найденные defaults, port 3001/`METRICS_ENABLED`, auth и content-type только после проверки Go.
5. Протокол determinism для differential harness: фиксированный clock/UTC/locale, test-only random injection, сериализованное состояние БД и jobs, контролируемые network receivers; явный allowlist нормализаций. Повтори ключевые baseline сценарии 3 раза, различия → FAIL/flaky, а не ignored. Веди manifest обязательных сценариев и точно считай `expected/executed/skipped/not_run`.

**Приёмка дополнения Stage 02:** все frontend callsites имеют инвентарный ID и Go expected shape/fixture либо обоснованный BLOCKER; отдельные inventories static/metrics существуют; воспроизводимость подтверждена; `skipped/ignored/not_run=0` среди обязательных **baseline тестов текущего этапа**. Остальной Rust parity остаётся `NOT_TESTED`, не PASS.

### Обязательные MD-результаты
- `docs/stages/STAGE_02_API_CONTRACT.md`
- `docs/API_INVENTORY.md`, `docs/API_PARITY_MATRIX.md`
- `docs/CONTRACT_TEST_STRATEGY.md`
- `docs/FRONTEND_API_SHAPE_MATRIX.md`, `docs/FRONTEND_API_PARITY.md` (baseline Go)
- `docs/STATIC_SERVING_PARITY.md`, `docs/METRICS_PARITY.md` (baseline Go)
- `docs/decisions/ADR_001_COMPATIBILITY_BASELINE.md`
- Исполняемый тестовый harness и versioned fixtures в `tests/compatibility/`.

### Gate PASS
Всё, что обслуживает GoWave (HTTP/WS/не контрактные маршруты), инвентаризировано; baseline и сравнения воспроизводимы; есть сценарии ошибок и мутаций; матрица честно отличает «не проверялось» от PASS.

## Команда завершения этапа 02

Сначала запиши/обнови все обязательные `.md` отчёты и сводный handoff, затем закоммить изменения и выполни `git push origin rustwave-dev` (без force). В финальном ответе покажи **фактический статус**, commit SHA, тесты с числом PASS/FAIL/SKIPPED, ссылку на CI, названия отчётов и текстовый список блокеров. **Не приступай к этапу 03**: пользователь запустит следующий промпт отдельно.
