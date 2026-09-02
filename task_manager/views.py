"""Представления верхнего уровня.

IndexView — GET / отдаёт главную через DjangoTemplates (серверный рендер).
"""

from django.views.generic import TemplateView


def trigger_error(request):
    """GET /sentry-debug/ — искусственная ошибка, чтобы проверить коллектор."""
    _ = request.method
    return 1 / 0


class IndexView(TemplateView):
    """Главная страница с приветствием Хекслета."""

    template_name = "index.html"
