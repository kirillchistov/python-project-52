"""CBV меток: CRUD только для залогиненных."""

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label
from task_manager.mixins import AuthRequiredMixin, DeleteProtectionMixin


class LabelListView(AuthRequiredMixin, ListView):
    """GET /labels/ — таблица меток."""

    model = Label
    template_name = "labels/list.html"
    context_object_name = "labels"


class LabelCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/form.html"
    success_url = reverse_lazy("labels")
    success_message = _("Label successfully created")
    extra_context = {
        "title": _("Create label"),
        "button_text": _("Create"),
    }


class LabelUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/form.html"
    success_url = reverse_lazy("labels")
    success_message = _("Label successfully updated")
    extra_context = {
        "title": _("Edit label"),
        "button_text": _("Change"),
    }


class LabelDeleteView(
    AuthRequiredMixin,
    DeleteProtectionMixin,
    SuccessMessageMixin,
    DeleteView,
):
    model = Label
    template_name = "labels/delete.html"
    success_url = reverse_lazy("labels")
    success_message = _("Label successfully deleted")
    protected_message = _("Cannot delete label")
    extra_context = {
        "title": _("Delete label"),
        "button_text": _("Yes, delete"),
    }
