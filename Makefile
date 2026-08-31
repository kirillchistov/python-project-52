# Команды сборки, запуска и деплоя.
# setup — цель проверки Хекслета: ставит зависимости, собирает статику, применяет миграции.
# render-start — команда запуска на Render; gunicorn берётся из .venv после uv sync.

export PATH := $(PWD)/.venv/bin:$(HOME)/.local/bin:$(PATH)

install:
	uv sync

collectstatic:
	uv run python manage.py collectstatic --no-input

migrate:
	uv run python manage.py migrate --no-input

setup: install collectstatic migrate

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi --bind 0.0.0.0:$${PORT:-8000}

dev:
	uv run python manage.py runserver

lint:
	uv run ruff check .

.PHONY: install collectstatic migrate setup build render-start dev lint
