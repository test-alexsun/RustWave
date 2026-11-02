# ПРОМПТ 00 — Инициализация RustWave и безопасная проверка SSH

> **Рекомендуемая модель Codex для этапа 00:** GPT-6.1 Terra, Thinking Effort: **Medium**. Если модель недоступна в меню, выбери доступную GPT-6 с уровнем High/Extra High. Это рекомендация; выбор делается в интерфейсе Codex.

**Инструкция Codex GPT-6 High:** выполни **только этап 00** проекта RustWave. Ниже полный самостоятельный промпт для вставки в новую сессию Codex.

**Первый этап:** отчетов пока может не быть. Создай исходную структуру отчётности.


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
Инициализируй УЖЕ СУЩЕСТВУЮЩИЙ пустой GitHub-репозиторий `test-alexsun/RustWave`. На момент подготовки он был пуст: проверь состояние заново и не перезаписывай появившиеся файлы. Исторический исходник GoWave нужно сохранить как эталон, чтобы сравнивать Rust с Go и переиспользовать frontend.

### Выполнение
1. Проверь доступ GitHub (`gh auth status`, `gh repo view test-alexsun/RustWave`), `git`, Rust, Go, Bun, Docker, локальные версии. При отсутствии прав на push — не пытайся обходить ограничения, отрази BLOCKED.
2. Если RustWave действительно пуст: клонируй `aaaSaZaN/gowave`, переключись на **точный ref** `d709bad01dc0ceacb20012a3afdf528eddfd061f`, сохрани upstream history и LICENSE; переназначь remotes: `upstream` → оригинал, `origin` → `test-alexsun/RustWave`; сформируй `main` из выбранного commit и push **без force**, затем создай `rustwave-dev`. Если RustWave уже инициализирован, изучи его историю и согласуй безопасный способ добавить upstream как read-only reference без замены данных.
3. Создай/обнови `AGENTS.md` с политикой staged development, защитой API, обеими БД и обязательным handoff; не теряй исходные инструкции GoWave — перенеси/объедини их корректно.
4. Создай каталог `docs/stages/`, `docs/contracts/`, `docs/decisions/`, `docs/benchmarks/`. Создай файлы `docs/UPSTREAM_LOCK.md`, `docs/PROGRESS.md`, `docs/HANDOFF.md`, `docs/PLAN.md` и шаблон отчёта `docs/stages/TEMPLATE.md`.
5. Проведи **только read-only SSH preflight**: `ssh -o BatchMode=yes -o ConnectTimeout=10 de126-2 'cat /etc/os-release; uname -a; id; free -h; df -h; command -v docker || true; command -v cargo || true'`. Проверь exit status. Не открывай порты, не устанавливай пакеты, не запускай нагрузку и не отключай службы.
6. Если работаешь из Windows, учти, что SSH-алиас берётся из пользовательского `~/.ssh/config` (Windows OpenSSH). Не копируй приватные ключи на сервер. Host key изменился? Выполни процедуру из общих правил.
7. Проверь `.gitignore`: секреты, базы, дампы, ключи, benchmark raw output с персональными данными не должны попадать в Git. Сохрани сводку окружения без секретов.

8. В `AGENTS.md` и `docs/GATE_POLICY.md` внеси глобальные требования из `GLOBAL_PARITY_GATES.md` комплекта промптов (если файл недоступен, полностью сформулируй политику из нижеследующих требований, не останавливая работу): frontend API consumer-shape, test determinism, no-skips fail-closed, static-serving и metrics parity. Не сокращай их до «все API вернули HTTP 200». Обязательно включи 1) карту React callsite→API method/path/shape и строгую проверку missing/null/empty, headers/errors/UI consumers; 2) детерминированные UTC/clock/test-only PRNG/DB fixtures и повторяемость; 3) подсчёт expected/executed test IDs и запрет skipped/ignored/xfail/todo/pending/not_run для обязательного gate; 4) static roots/SPA/HEAD/404/gzip/WASM; 5) Prometheus families/HELP/TYPE/labels, auth, metrics enabled/disabled и system stats. Запретите выпуск stable при любом обязательном пробеле. Подготовь пустые, честно отмеченные как `NOT_TESTED`, матрицы `docs/FRONTEND_API_SHAPE_MATRIX.md`, `docs/STATIC_SERVING_PARITY.md`, `docs/METRICS_PARITY.md` и ссылки в `docs/PLAN.md`.

### Обязательные MD-результаты
- `docs/stages/STAGE_00_BOOTSTRAP.md`
- `docs/UPSTREAM_LOCK.md` — SHA, ссылка, дата фиксации, контракт и лицензия.
- `docs/PROGRESS.md`, `docs/HANDOFF.md`, `docs/PLAN.md`, `AGENTS.md`.
- `docs/GATE_POLICY.md`, `docs/FRONTEND_API_SHAPE_MATRIX.md`, `docs/STATIC_SERVING_PARITY.md`, `docs/METRICS_PARITY.md`.

### Gate PASS
GitHub RustWave и remotes проверены; зафиксирован upstream SHA; ветка `rustwave-dev` существует либо документирован блокер; необходимые MD созданы; VPS read-only preflight реально выполнен или явно BLOCKED. Ни один production-сервис не изменён.

## Команда завершения этапа 00

Сначала запиши/обнови все обязательные `.md` отчёты и сводный handoff, затем закоммить изменения и выполни `git push origin rustwave-dev` (без force). В финальном ответе покажи **фактический статус**, commit SHA, тесты с числом PASS/FAIL/SKIPPED, ссылку на CI, названия отчётов и текстовый список блокеров. **Не приступай к этапу 01**: пользователь запустит следующий промпт отдельно.
