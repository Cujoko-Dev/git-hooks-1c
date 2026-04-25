---
name: pdm-dev-workflow
description: >-
  PDM и вложенный проект `.dev`: установка зависимостей, запуск pytest и скриптов через
  `pdm run -p .dev` без активации venv. Используй в этом репозитории при правках Python,
  зависимостей и тестов.
---

# PDM и каталог `.dev`

## Структура

В корне — основной `pyproject.toml` пакета. Разработческое окружение (pytest, инструменты) задаётся во **вложенном** проекте **`.dev/pyproject.toml`**. Его скрипты и команды запускают через **`pdm run -p .dev …`** (`-p` — путь к каталогу с dev-`pyproject.toml`).

## Команды

- Зависимости из корня: `pdm install` или `pdm sync` (см. правило `pdm-package-manager.mdc`).
- Тесты и скрипты из `[tool.pdm.scripts]` dev-проекта: например `pdm run -p .dev test`, `pdm run -p .dev pytest …`.
- Не рассчитывать на ручную активацию виртуального окружения: используй `pdm run -p .dev …`.

## Терминал

В этом репозитории **нет** `scripts/run.ps1` — команды выполняй из корня напрямую. В репозиториях с обёрткой (например ctl-1c, codemask-1c) смотри их `terminal-test-execution-policy.mdc`.

## Ограничения

Не подменять управление зависимостями на `uv`, произвольный `pip install` для lockfile проекта или Poetry — см. `pdm-package-manager.mdc`.
