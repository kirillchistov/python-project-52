"""CBV статусов: CRUD только для залогиненных."""

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import AuthRequiredMixin, DeleteProtectionMixin
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


class StatusListView(AuthRequiredMixin, ListView):
    """GET /statuses/ — таблица статусов."""

    model = Status
    template_name = "statuses/list.html"
    context_object_name = "statuses"


class StatusCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/form.html"
    success_url = reverse_lazy("statuses")
    success_message = _("Status successfully created")
    extra_context = {
        "title": _("Create status"),
        "button_text": _("Create"),
    }


class StatusUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/form.html"
    success_url = reverse_lazy("statuses")
    success_message = _("Status successfully updated")
    extra_context = {
        "title": _("Edit status"),
        "button_text": _("Change"),
    }


class StatusDeleteView(
    AuthRequiredMixin,
    DeleteProtectionMixin,
    SuccessMessageMixin,
    DeleteView,
):
    model = Status
    template_name = "statuses/delete.html"
    success_url = reverse_lazy("statuses")
    success_message = _("Status successfully deleted")
    protected_message = _("Cannot delete status")
    extra_context = {
        "title": _("Delete status"),
        "button_text": _("Yes, delete"),
    }
