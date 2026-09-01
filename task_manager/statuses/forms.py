"""Форма статуса: одно поле name, как в демо."""

from django import forms
from django.utils.translation import gettext_lazy as _

from task_manager.statuses.models import Status


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ("name",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = _("Name")
        css = self.fields["name"].widget.attrs.get("class", "")
        self.fields["name"].widget.attrs["class"] = f"{css} mt-1 block w-full".strip()
