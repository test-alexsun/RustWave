# STAGE 00 — Bootstrap

- Status: COMPLETE (gate этапа 00: PASS)
- Started / Finished (UTC): 2026-11-02; точное время не записано.
- Source SHA: d709bad01dc0ceacb20012a3afdf528eddfd061f; branch rustwave-dev, базовый HEAD тот же.
- Environment: Windows, Git 2.45.1.windows.1, rustc 1.98.1, cargo 1.98.1; БД не проверены.

## Что сделано
Созданы AGENTS.md, README.md, .gitignore, политика, lock, план, progress, handoff, шаблон, каталоги contracts/decisions/benchmarks и три пустые матрицы. Промпты находятся в codex/stage, а не codex/stages. Upstream инструкции сохранены в docs/UPSTREAM_AGENTS.md, LICENSE сохранён.

## Решения и обоснования
История upstream сохранена, origin направлен на RustWave, upstream push отключён. Пустой origin проверен через ls-remote; main опубликован без force. Правила .gitignore объединены.

## Команды и результаты
- В sandbox `git ls-remote` не подключился к GitHub, SSH alias не разрешился. Повтор вне sandbox: `git ls-remote https://github.com/test-alexsun/RustWave.git HEAD` exit 0, refs отсутствуют; clone upstream и `git cat-file -t d709bad01dc0ceacb20012a3afdf528eddfd061f` exit 0, тип commit. `git push -u origin main` exit 0.
- `gh auth status` и `gh repo view test-alexsun/RustWave`: exit 1, gh отсутствует. Права push подтверждены публикацией main.
- `git --version`, `rustc --version`, `cargo --version`: exit 0; версии выше. `go version`, `bun --version`, `docker --version`: exit 1, команды отсутствуют.
- `ssh -o BatchMode=yes -o ConnectTimeout=10 de126-2 'cat /etc/os-release; uname -a; id; free -h; df -h; command -v docker || true; command -v cargo || true'` вне sandbox: exit 0, Debian 13.7, x86_64, 967 MiB RAM, root filesystem 9.8G; docker и cargo не найдены. Только чтение, сервисы не изменялись.

## Совместимость API/БД
NOT_TESTED; fixtures отсутствуют. Обязательные тестовые ID ещё не определены: executed 0, PASS 0, FAIL 0, SKIPPED 0; это не означает успешный gate.

## Безопасность и сохранность данных
Production не изменён. Секреты не записаны.

## Результаты CI / ссылки
CI не запускался; ссылка отсутствует.

## Остаточные проблемы, риски, BLOCKER
Обязательных блокеров этапа 00 нет. Ранее daemon не отвечал и запуск завершался по тайм-ауту; последующая проверка ниже подтвердила доступность. Глобальная Git identity не настроена. Совместимость и CI не проверены: это задачи будущих этапов.

## Завершающая проверка

- Перед изменениями `git status --short --branch` показал чистую `rustwave-dev`; HEAD и `refs/heads/rustwave-dev` origin совпали на `4bd576c96d56d061628ab4634f84ffe82b94a547`.
- `docker version` exit 0: клиент и Engine 29.9.2, сервер Docker Desktop 4.97.0, linux/amd64; `docker info --format 'ServerVersion={{.ServerVersion}} OS={{.OperatingSystem}} CPUs={{.NCPU}} Containers={{.Containers}}'` exit 0: ServerVersion=29.9.2, OS=Docker Desktop, CPUs=4, Containers=0. `docker compose version` exit 0: v5.6.1.
- Пользователь сообщил об успешном `docker run --rm hello-world`, включая скачивание и запуск контейнера. Самостоятельно этот smoke test в завершающей сессии не повторялся; exit code и вывод не наблюдались.
- `git --version`, `gh --version`, `go version`, `bun --version`, `rustc --version`, `cargo --version`, `gh auth status` — exit 0; версии соответствуют записи ниже. `gh auth status` подтверждает активный аккаунт test-alexsun.
- SSH preflight выполнен ранее и зафиксирован ниже. В завершающей сессии VPS не изменялся и не проверялся повторно. API parity tests не запускались по указанию пользователя; CI не запускался.

## Повторная проверка 2026-11-02

- Windows 10 Pro 22H2, 10.0.19045 x64. `git --version`: 2.45.1.windows.1; `rustc --version`: 1.98.1; `cargo --version`: 1.98.1; `ssh -V`: OpenSSH_for_Windows_9.5p1. Все exit 0.
- Установлены в пользовательской области через winget с проверкой хеша `gh` 2.103.3 и Bun 1.4.2; пользовательский Go 1.27.3 из официального ZIP проверен по SHA-256 и добавлен в пользовательский PATH. Проверка команд в обновлённом PATH exit 0.
- С разрешения пользователя установлен Docker Desktop 4.97.0 через winget с проверкой хеша. `docker --version` 29.9.2 и `docker compose version` v5.6.1 exit 0; клиент доступен, daemon не проверен успешно. `wsl --update --web-download` exit 0, `wsl --version` показывает WSL 3.0.3 и ядро 6.18.54.1-1.
- `gh auth status` и `gh repo view test-alexsun/RustWave` exit 0: test-alexsun, публичный репозиторий, default main. `git status`, `git remote -v`, `git branch --show-current`, `git ls-remote origin HEAD refs/heads/rustwave-dev`, `git ls-remote upstream HEAD`, `git push --dry-run origin rustwave-dev` успешны. Проверенный remote rustwave-dev: c80a418ac81ab5530d870672fdf923d847ebd652; upstream HEAD изменился до 4a4bdb9a5f2d2a356fc16e55174e6c508cfa0d55, закреплённый d709bad остаётся эталоном. Upstream push отключён.
- SSH preflight из промпта exit 0; Debian 13.7, 1 vCPU AMD EPYC 7642, 967 MiB RAM, диск 9.8 GiB, свободно 8.1 GiB. На VPS ничего не устанавливалось, сервисы не менялись.
- Проверены все Markdown в codex/stage: неверные `codex/stages/` заменены на `codex/stage/`, `docs/stages/` сохранён. `rg -n 'codex/stages/' codex/stage` exit 1 (совпадений нет). `git diff --check` exit 0. API compatibility tests не запускались по заданию; CI не запускался.

## Следующий этап
Этап 01 — только после отдельного запуска пользователем; см. [handoff](../HANDOFF.md).
