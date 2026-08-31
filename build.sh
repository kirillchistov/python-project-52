#!/usr/bin/env bash
# Сборка на Render: ставит uv, зависимости, статику и миграции.
# Команда сборки в настройках Web Service: make build

set -euo pipefail

curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"

make install && make collectstatic && make migrate
