"""ASGI-вход (на Render не используется, gunicorn работает через WSGI)."""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_manager.settings")

application = get_asgi_application()
