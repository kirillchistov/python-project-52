"""Статус задачи: уникальное имя, дата создания. Удаление с PROTECT у связанных задач."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    """Имя совпадает с полем формы name / id_name в демо."""

    name = models.CharField(max_length=100, unique=True, verbose_name=_("Name"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Task status")

    def __str__(self):
        return self.name
