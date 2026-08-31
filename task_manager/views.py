"""Представления верхнего уровня.

IndexView — GET / отдаёт главную через DjangoTemplates (серверный рендер).
"""

from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Главная страница с приветствием Хекслета."""

    template_name = "index.html"
