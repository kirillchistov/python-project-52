"""Форма задачи: имя, описание, статус, исполнитель, метки. Автор задаётся во view."""

from django import forms
from django.utils.translation import gettext_lazy as _

from task_manager.tasks.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("name", "description", "status", "executor", "labels")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 6}),
            "labels": forms.SelectMultiple(attrs={"multiple": True, "size": 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = _("Name")
        self.fields["description"].label = _("Description")
        self.fields["status"].label = _("Status")
        self.fields["executor"].label = _("Executor")
        self.fields["labels"].label = _("Labels")
        self.fields["executor"].required = False
        for field in self.fields.values():
            css = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{css} mt-1 block w-full".strip()
