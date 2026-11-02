# ПРОМПТ 15 — Финальный аудит, документация и безопасный релиз

> **Рекомендуемая модель Codex для этапа 15:** GPT-6 Astra, Thinking Effort: **Extra High**. Если модель недоступна в меню, выбери доступную GPT-6 с уровнем High/Extra High. Это рекомендация; выбор делается в интерфейсе Codex.

**Инструкция Codex GPT-6 High:** выполни **только этап 15** проекта RustWave. Ниже полный самостоятельный промпт для вставки в новую сессию Codex.

**Предыдущий отчёт:** `docs/stages/STAGE_14_*.md`. Прочитай и используй доказательные результаты, не воссоздавай их с нуля.


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
Сделай **независимый финальный аудит** RustWave и выпусти релиз лишь после прохождения всех обязательных критериев. Не объявляй 100% совместимость без доказательной матрицы.

### Выполнение
1. Верифицируй заново все промежуточные `docs/stages/STAGE_00...STAGE_14`, `docs/PROGRESS.md`, `docs/HANDOFF.md`, исходный SHA, README/LICENSE/AGPL атрибуцию, все матрицы API/DB/functions и список незакрытых несоответствий.
2. Выполни полный CI: Rust fmt/clippy/tests, SQLite/PG tests, differential Go↔Rust, subscriptions golden, auth/security, node E2E, CLI, install/update/backup/restore, frontend smoke, amd64/arm64 images, SCA. Все обязательные тесты должны реально исполняться (не skipped).
3. Проверь обратимую миграцию с GoWave на RustWave на **копиях** SQLite и PG, сохранение UUID, пользователей, токенов, нод, subscriptions, обновлений. Рассмотри несовместимые будущие миграции upstream и процедуру синхронизации веток.
4. Подготовь понятную русскую документацию: `README.md`, `docs/INSTALLATION.md`, `docs/CONFIGURATION.md`, `docs/API_COMPATIBILITY.md`, `docs/DATABASE_MIGRATION.md`, `docs/BACKUP_RESTORE.md`, `docs/DOCKER.md`, `docs/SYSTEMD.md`, `docs/SECURITY.md`, `docs/TROUBLESHOOTING.md`, `docs/RELEASE_CHECKLIST.md`. Укажи настоящие benchmark цифры с ограничениями.
5. Если gate PASS: подготовь Github Release (tags, changelog, SHA256SUMS, amd64/arm64 binaries, minimal GHCR images, SBOM/provenance по возможности), проверь установку из релизных артефактов. Ставить RustWave на действующую production-систему НЕ нужно.
6. Если gate НЕ PASS: не публикуй stable и не прячь проблему. Опубликуй подробный blocking report и оставь ветку `rustwave-dev` для исправлений. Опционально pre-release только с честной маркировкой неполной совместимости, без подмены stable.
7. Заверши `docs/HANDOFF.md` с версией, run IDs, SHA, ограничениями и планом обновления upstream. Не применяй force push, не мержи в main при провале gate.

### Дополнительные блокирующие условия stable release

- `docs/FRONTEND_API_SHAPE_MATRIX.md`: полное Go↔Rust consumer-shape покрытие для закреплённого React на SQLite и PG; real browser E2E и negative/error states, без правок frontend для скрытия ошибок.
- `docs/STATIC_SERVING_PARITY.md`: SPA/base path/404/GET/HEAD/gzip/WASM/headers security scenarios PASS; идентичный frontend build.
- `docs/METRICS_PARITY.md`: Prometheus listener/auth/enabled-disabled, metric names/HELP/TYPE/labels/units, health/system stats PASS, нет неподтверждённых отклонений.
- `docs/TEST_DETERMINISM.md` и `docs/RELEASE_GATE.md`: повторяемые тесты, manifest с expected/executed IDs по обеим DB/архитектурам, программа-проверяльщик статусов, **failed/skipped/ignored/xfail/todo/pending/not_run/unknown/flaky = 0** для обязательного набора. Отдельно проверь, что intentional skipped required test приводит к gate fail.
- При любом из этих пробелов нельзя выпускать stable, даже если Go↔Rust API endpoints count = 100% и Docker собирается. Сохрани blocker в отчёте и HANDOFF.

### Обязательные MD-результаты
- `docs/stages/STAGE_15_RELEASE.md`
- `docs/FINAL_AUDIT.md`, `docs/RELEASE_CHECKLIST.md`
- `docs/API_PARITY_FINAL_REVIEW.md`, `docs/DB_PARITY_FINAL_REVIEW.md`
- `docs/UPSTREAM_UPDATE_STRATEGY.md`, полный README.
- `docs/FRONTEND_API_SHAPE_MATRIX.md`, `docs/FRONTEND_API_PARITY.md`, `docs/STATIC_SERVING_PARITY.md`, `docs/METRICS_PARITY.md`, `docs/TEST_DETERMINISM.md`, `docs/RELEASE_GATE.md`.

### Gate PASS
Все P0–P3 критерии выполнены, покрытие 100% по полной объявленной матрице тестов, поддержка SQLite/PG проверена и честно указаны границы доказательства. Иначе — BLOCKED/PARTIAL и никакого заявления об успешном релизе.

## Завершение

Сохрани итоговый audit в Markdown, запушь проверенный результат, перечисли реальные SHA, CI runs и release artifacts. Не создавай stable при неполном gate.
