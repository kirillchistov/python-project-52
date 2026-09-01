"""CBV задач: список, просмотр, CRUD. Удаляет только автор."""

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from task_manager.mixins import AuthorOnlyMixin, AuthRequiredMixin
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task


class TaskListView(AuthRequiredMixin, ListView):
    """GET /tasks/ — таблица задач."""

    model = Task
    template_name = "tasks/list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.select_related("status", "author", "executor")


class TaskDetailView(AuthRequiredMixin, DetailView):
    """GET /tasks/<pk>/ — карточка задачи, включая метки."""

    model = Task
    template_name = "tasks/detail.html"
    context_object_name = "task"

    def get_queryset(self):
        return Task.objects.select_related(
            "status", "author", "executor"
        ).prefetch_related("labels")


class TaskCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/form.html"
    success_url = reverse_lazy("tasks")
    success_message = _("Task successfully created")
    extra_context = {
        "title": _("Create task"),
        "button_text": _("Create"),
    }

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/form.html"
    success_url = reverse_lazy("tasks")
    success_message = _("Task successfully updated")
    extra_context = {
        "title": _("Edit task"),
        "button_text": _("Change"),
    }


class TaskDeleteView(AuthorOnlyMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = "tasks/delete.html"
    success_url = reverse_lazy("tasks")
    success_message = _("Task successfully deleted")
    extra_context = {
        "title": _("Delete task"),
        "button_text": _("Yes, delete"),
    }
