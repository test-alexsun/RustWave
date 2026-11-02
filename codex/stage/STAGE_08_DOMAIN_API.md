# ПРОМПТ 08 — Пользователи, squads, profiles, inbounds, hosts, системные настройки

> **Рекомендуемая модель Codex для этапа 08:** GPT-6 Astra, Thinking Effort: **Extra High**. Если модель недоступна в меню, выбери доступную GPT-6 с уровнем High/Extra High. Это рекомендация; выбор делается в интерфейсе Codex.

**Инструкция Codex GPT-6 High:** выполни **только этап 08** проекта RustWave. Ниже полный самостоятельный промпт для вставки в новую сессию Codex.

**Предыдущий отчёт:** `docs/stages/STAGE_07_*.md`. Прочитай и используй доказательные результаты, не воссоздавай их с нуля.


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
Перенеси основные административные REST-домены, строго сохранив UI и связь пользователей с Xray конфигурациями.

### Выполнение
1. По API inventory реализуй CRUD и actions для users: create/update/delete/status/traffic/reset/extend/revoke/bulk/tags/lookup/stream, ограничения и очереди синхронизации.
2. Реализуй internal/external squads и membership, config profiles, config profile inbounds, hosts, host templates, routing/response rules, subscription settings и системные настройки, имеющиеся в эталоне.
3. Проверь все поля сложных JSON Xray inbounds и host config: VLESS REALITY Vision, XHTTP REALITY, Hysteria2 и остальные поддержанные типы — не добавляй ограничения, которых нет в GoWave.
4. Операции пользователей, профилей и очередей выполняй с сохранением атомарности GoWave (transactional outbox). Учитывай optimistic/concurrent updates, FK, idempotency, non-null differences.
5. Для каждого эндпоинта: сравни status/headers/JSON/errorCode, DB before/after, downstream queue. Покрой SQLite и PostgreSQL на одинаковых фикстурах, ошибки/валидацию/bulk операций.
6. Пройди UI browser smoke (без изменения frontend) с эталонной авторизацией: логин, таблица пользователей, редактирование профиля, inbound и host, настройки.

### Обязательное усиление: frontend/API-shape (потребительский контракт)

1. Используй `docs/FRONTEND_API_SHAPE_MATRIX.md` из Stage 02. Для **каждого** UI callsite доменов users/squads/profiles/inbounds/hosts/settings, который покрывает Stage 08, обеспечь точную форму ответа Rust без правок React: `response` envelope, nesting, nullable/optional/missing, empty arrays, integer/string booleans, enum casing, sort/order, pagination metadata, error codes/paths, `Content-Type`, cookies, ETag где применимо.
2. Построй реальные end-to-end сценарии React → Rust и React → Go с **одним и тем же неизменённым frontend bundle**, browser trace redaction и snapshot ожидаемого shape. Typecheck и smoke недостаточны: проверь формы submit/mutation, все поля таблиц, фильтры, empty/error/loading states, optimistic updates и повторный fetch.
3. Differential tests запускать на SQLite **и** PostgreSQL с одинаковыми seed data, контролируемыми timestamp, детерминированным порядком списков; тесты с пропущенным или неисполненным обязательным случаем Stage 08 → Gate FAIL/PARTIAL, не PASS. Добавь тест, который ловит несовпадение `field absent` vs `field: null`.
4. Не исправляй несоответствие правкой Zod schema, сменой Axios-декодирования или удалением React-поля. Любые изменения frontend без независимого обоснования отмечай как нарушение parity до проверки на обеих реализациях.

**Приёмка:** все in-scope строки `docs/FRONTEND_API_SHAPE_MATRIX.md` помечены PASS для Go/Rust × SQLite/PG; реальные UI workflows выполняются и проверяют сетевые ответы; ни один обязательный тест текущего этапа не skipped/ignored/xfail/not_run.

### Обязательные MD-результаты
- `docs/stages/STAGE_08_DOMAIN_API.md`
- `docs/DOMAIN_API_PARITY.md`
- `docs/UI_SMOKE_RESULTS.md`
- `docs/FRONTEND_API_PARITY.md` и обновлённая `docs/FRONTEND_API_SHAPE_MATRIX.md`
- Обновлённые матрицы API/функций/DB.

### Gate PASS
Весь инвентарь перечисленных доменов имеет работающие Rust handlers, differential tests для обеих БД, достоверные результаты UI smoke; нет заглушек, выдающих фиктивный success.

## Команда завершения этапа 08

Сначала запиши/обнови все обязательные `.md` отчёты и сводный handoff, затем закоммить изменения и выполни `git push origin rustwave-dev` (без force). В финальном ответе покажи **фактический статус**, commit SHA, тесты с числом PASS/FAIL/SKIPPED, ссылку на CI, названия отчётов и текстовый список блокеров. **Не приступай к этапу 09**: пользователь запустит следующий промпт отдельно.
