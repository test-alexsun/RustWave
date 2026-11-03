# Решение о принятии Browser V1 — 2026-11-03

Владелец проекта явно утвердил `RUSTWAVE-BROWSER-PATCH-V1` как новую обязательную TEST-ONLY версию browser smoke для RustWave. Формальная проверка: **PASS**. Регистрация baseline: **ACCEPTED**. Исполнение обязательного CI пока **NOT_RUN**, browser gate **BLOCKED**, STAGE_01 **PARTIAL** до получения результатов.

- Upstream: `d709bad01dc0ceacb20012a3afdf528eddfd061f`.
- Patch SHA256: `0cae2b9c7a6800a6b1c9be9645d438a8beecbce62003f978b4ccbf333c4abf88`.
- Точные байты проверенного TSX: `0abb393e052f4cd0720aa42fb18586f9fae2d216afe2960fb119f839c8759fe3`.
- Runner: `RUSTWAVE-BROWSER-CDP-RUNNER-V1`; SHA256 исполненных CRLF-байтов: `8afefe1d65962ebc9878cb952c9819e5221f909cd3d957dab723e430785255d5`.
- Git LF-версия runner: `513ceeb9cc15ff497ce4b4bab71eeddd2000d971050aeaa88c2b951230561122`. CI явно восстанавливает точные CRLF-байты ранее исполненного runner и TSX, сверяет hash. Это не изменение логики или production-файлов.

Версионированный [manifest](../../tools/audit-stage01/browser-v1.manifest.json) закрепляет все 59 ID, порядок, сообщения assertions, hashes артефактов, версии окружения, ожидаемые CI ID и критерии. [Формальная проверка](browser-v1-formal-review.json) содержит все исходные выражения assertions: аргументы, значения и порядок совпадают. Заново применён опубликованный zero-context patch; результат побайтно совпал с тестом из 20 успешных запусков. Исходные 1772 файла проверены по upstream Git blobs. Изменён только тест во временной копии.

## Проверенный функциональный контракт

JSON viewer: ожидание открытого видимого modal с реальным дочерним `.jer-editor-container .jer-value-string` подтверждает React DOM commit перед исходными проверками значений, read-only режима и отсутствия mutation controls. Это не ожидание одного контейнера без содержимого.

Session clock: wrapper наблюдает регистрацию настоящего 20ms setInterval, делегирует его callback без замены Date.now, затем ждёт реального увеличения текста DOM. Сохранено исходное сравнение `Number(container.textContent) > firstTime`. Записи регистрации, начального DOM, callback и DOM commit проверяются в порядке до assertion. Наличие элемента само по себе недостаточно.

Временная семантика пересмотрена явно: фиксированные 100/60ms sleeps заменены ограниченным ожиданием необходимого состояния. Это не утверждение прежней точной временной эквивалентности и не SLA приложения. Внешний timeout остаётся 20000ms, внутренний readiness bound — 19000ms. Production API, React/Go, fixtures и GATE_POLICY неизменны. Никакие assertions не удалены и ожидаемые значения не ослаблены.

## Обязательная проверка

CI выполняет четыре самостоятельных запуска: normal 2CPU/2000MiB, CPU-only 1CPU/2000MiB, RAM-only 2CPU/1400MiB и contention 1CPU/1400MiB с контролируемым CPU loop. Каждый контейнер получает свежий профиль браузера; сеть при smoke отключена. Подготовка зависимостей отдельная. Пакеты Bun 1.4.2 и Chromium 156.0.8078.73 закреплены; базовые образы закреплены digest. Новая сборка CI image не выдаётся за прежний локальный image digest; её фактический inspect сохраняется.

Это отдельная CI-матрица 4×59, дополнительно к сохранённой квалификации 20×59; локальные результаты не являются CI PASS. Любой пропуск, лишний/переставленный ID, FLAKY, неизвестный статус, nonzero exit, неверный hash, несоответствие версии, timeout, неожиданное CDP исключение или network failure блокирует gate. Отрицательная проверка содержит 21 испорченный результат и положительный контроль. При ошибке исполнения CI сохраняет диагностику и завершает job с ошибкой. Никакого continue-on-error или автоматического повторения failed assertions.

Workflow [browser-v1.yml](../../.github/workflows/browser-v1.yml) запускается при каждом push в rustwave-dev и PR в эту ветку без path-фильтров. Обязательный status context: `Browser V1 mandatory gate`. Настройка защиты ветки и реальный run должны быть подтверждены отдельно; наличие YAML не означает исполнение CI.

## История и границы решения

`ORIGINAL_BROWSER = HISTORICAL_FLAKY`; исходный ID `GOWAVE-BROWSER-ORIGINAL-d709bad01dc0ceacb20012a3afdf528eddfd061f` сохраняется отдельно. `PATCHED_BROWSER_V1 = NEW_MANDATORY_TEST`. Исходный 20-секундный timeout остаётся необъяснённым историческим FAIL; найденные races не объявлены его доказанной причиной. Все исходные FAIL/FLAKY/SKIPPED/NOT_RUN и ошибки инструментов остаются в прежних секциях ledger и [диагностике](BROWSER_DIAGNOSTICS.md).

Это утверждённая владельцем замена версии теста, а не исключение из no-skips/no-flaky для новой версии. Прежний flaky тест не переименован в PASS. Go↔Rust parity остаётся NOT_TESTED, Rust backend отсутствует. STAGE_02 автоматически не начинается.

## CI provisioning history

Первый run [41658971199](https://github.com/test-alexsun/RustWave/actions/runs/41658971199), commit `5ec1e6a0ef282cd178b436eb2ef0742a34224d38`: FAIL на сборке окружения (apt exit 100: закреплённая версия отсутствует в текущем индексе). Browser: 4 NOT_RUN, 0 assertions. Upload также FAIL, поскольку evidence directory ещё не создан; полный build log доступен в job. Исправление provisioning: официальные архивные .deb той же версии, SHA256 закреплены, SHA1 сверены с Debian Snapshot. Build log теперь сохраняется независимо от browser evidence. Тест, patch, runner и timeout не менялись.
