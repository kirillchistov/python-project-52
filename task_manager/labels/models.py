"""Метка задачи: уникальное имя. verbose_name как в демо (Label с таким Имя…).

M2M с задачами на уровне БД не PROTECT: занятую метку блокируем в delete().
"""

from django.db import models
from django.db.models import ProtectedError
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Name"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Label")

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        if self.pk and self.tasks.exists():
            raise ProtectedError(
                "Cannot delete label because it is used",
                set(self.tasks.all()),
            )
        return super().delete(using=using, keep_parents=keep_parents)
