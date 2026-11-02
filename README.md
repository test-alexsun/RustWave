# RustWave

RustWave — планируемый Rust backend, совместимый с GoWave и его существующим React/TypeScript frontend. Цель — 100% совместимости по полному проверяемому инвентарю API и функций, включая форму данных frontend, static serving и метрики. Совместимость пока не проверена.

Планируемая архитектура: Axum, Tokio, SQLx и Serde; SQLite или PostgreSQL на выбор, native systemd либо Docker Compose на Debian 13. Приоритет — сохранность данных и совместимость, затем снижение RAM и CPU. Реализация и установщик ещё не подготовлены; инструкции установки появятся после соответствующих этапов. Не используйте проект как готовую замену GoWave.

Эталон и его статус указаны в [docs/UPSTREAM_LOCK.md](docs/UPSTREAM_LOCK.md), ход разработки — в [docs/PROGRESS.md](docs/PROGRESS.md), политика проверок — в [docs/GATE_POLICY.md](docs/GATE_POLICY.md). Исходная лицензия GoWave AGPL-3.0 и атрибуция должны быть сохранены после проверки оригинала.
