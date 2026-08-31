#!/usr/bin/env python
"""Точка входа Django CLI: runserver, migrate, collectstatic и остальные команды."""

import os
import sys


def main():
    """Запускает выбранную management-команду Django."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_manager.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Не удалось импортировать Django. Проверьте, что зависимости "
            "установлены: uv sync"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
