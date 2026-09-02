"""Фильтр списка задач: статус, исполнитель, метка и «только свои»."""

from django import forms
from django.utils.translation import gettext_lazy as _
from django_filters import BooleanFilter, FilterSet, ModelChoiceFilter

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class TaskFilter(FilterSet):
    """Имена полей как в демо: status, executor, labels, self_tasks."""

    status = ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=_("Status"),
    )
    executor = ModelChoiceFilter(
        queryset=User.objects.all(),
        label=_("Executor"),
    )
    labels = ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_("Label"),
    )
    self_tasks = BooleanFilter(
        method="filter_self_tasks",
        widget=forms.CheckboxInput,
        label=_("Only own tasks"),
    )

    class Meta:
        model = Task
        fields = ("status", "executor", "labels")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.form.fields.items():
            if name == "self_tasks":
                continue
            css = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{css} mt-1 block w-full".strip()

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
