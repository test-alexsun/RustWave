# RESUME_STAGE — продолжение текущего этапа Codex GPT-6 High

Продолжи работу над `https://github.com/test-alexsun/RustWave`. Исходник: `https://github.com/aaaSaZaN/gowave`; Debian 13 VPS доступен через SSH-алиас `de126-2` (только при успешной проверке host key).

1. Прочитай `AGENTS.md`, `docs/PROGRESS.md`, `docs/HANDOFF.md`, `docs/UPSTREAM_LOCK.md` и отчёт **текущего незавершённого этапа** в `docs/stages/`. Сверь с реальными `git status`, HEAD, удалённой веткой `rustwave-dev` и CI; не полагайся на текст из старой переписки.
2. Определи точный текущий этап и незавершённые критерии PASS; не начинай следующую стадию.
3. Продолжи только недоделанные задачи, исправь найденные ошибки, выполни пропущенные тесты; не повторяй без причины пройденные шаги и не уничтожай изменения.
4. Сохрани проверяемые результаты в `docs/stages/STAGE_NN_*.md`, обнови `docs/PROGRESS.md` и `docs/HANDOFF.md`; commit/push только в RustWave, без force.
5. Если SSH host key изменился, приостанови удалённые операции, не отключай SSH-проверку.
6. Выведи статус PASS/PARTIAL/BLOCKED/FAIL, SHA, список пройденных/непройденных тестов и следующую безопасную задачу.

## Дополнение v2 — обязательные проверки

Прочитай `docs/GATE_POLICY.md` и при необходимости спецификацию из `GLOBAL_PARITY_GATES.md` комплекта промптов. Проверь, что отчёты frontend/API-shape, static-serving, metrics, determinism и no-skips gate перенесены в текущую сессию. При обнаружении skipped/ignored/not_run обязательного теста по текущему gate запрети PASS; для stable заблокируй релиз. Не изменяй эталонные Go fixtures для согласования с Rust.
