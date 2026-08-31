"""Представления верхнего уровня.

IndexView — GET / отдаёт приветствие (цель шага 1).
"""

from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Главная страница с приветствием Хекслета."""

    template_name = "index.html"
