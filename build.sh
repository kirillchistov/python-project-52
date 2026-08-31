#!/usr/bin/env bash
# Сборка на Render: ставит uv, зависимости, статику и миграции.
# Команда сборки в настройках Web Service: make build

set -euo pipefail

curl -LsSf https://astral.sh/uv/install.sh | sh
# uv ставит бинарник в ~/.local/bin. Файл env есть не на всех системах
# (на Render его нет) — добавляем каталог в PATH сами.
export PATH="$HOME/.local/bin:$PATH"
if [ -f "$HOME/.local/bin/env" ]; then
  source "$HOME/.local/bin/env"
fi

make install && make collectstatic && make migrate
