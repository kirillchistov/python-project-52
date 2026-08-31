# Команды сборки, запуска и деплоя.
# setup — цель проверки Хекслета: зависимости, Tailwind, статика, миграции.
# tailwind — собирает CSS до collectstatic, иначе WhiteNoise не найдёт файл.

export PATH := $(PWD)/.venv/bin:$(HOME)/.local/bin:$(PATH)

install:
	uv sync

tailwind:
	uv run python manage.py tailwind build

collectstatic:
	uv run python manage.py collectstatic --no-input

migrate:
	uv run python manage.py migrate --no-input

messages:
	uv run python manage.py compilemessages --ignore .venv

setup: install tailwind collectstatic migrate

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi --bind 0.0.0.0:$${PORT:-8000}

dev:
	uv run python manage.py tailwind runserver

lint:
	uv run ruff check .

.PHONY: install tailwind collectstatic migrate messages setup build render-start dev lint
