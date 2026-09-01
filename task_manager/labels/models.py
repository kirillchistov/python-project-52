"""Метка задачи: уникальное имя. verbose_name как в демо (Label с таким Имя…)."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Name"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Label")

    def __str__(self):
        return self.name
