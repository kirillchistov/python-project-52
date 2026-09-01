"""Задача: обязательные статус и автор, опциональные исполнитель и метки.

Автор и исполнитель — PROTECT: пользователя с задачами удалить нельзя.
Статус — PROTECT: занятый статус удалить нельзя.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import User


class Task(models.Model):
    """Поля формы: name, description, status, executor, labels."""

    name = models.CharField(max_length=150, unique=True, verbose_name=_("Name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name="tasks",
        verbose_name=_("Status"),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="authored_tasks",
        verbose_name=_("Author"),
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="executed_tasks",
        verbose_name=_("Executor"),
        null=True,
        blank=True,
    )
    labels = models.ManyToManyField(
        Label,
        related_name="tasks",
        verbose_name=_("Labels"),
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Task")

    def __str__(self):
        return self.name
