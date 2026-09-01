"""CBV пользователей и аутентификации: список, CRUD, вход и выход."""

from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import DeleteProtectionMixin, SelfOnlyMixin
from task_manager.users.forms import LoginForm, UserForm
from task_manager.users.models import User


class UserListView(ListView):
    """GET /users/ — список доступен без входа."""

    model = User
    template_name = "users/list.html"
    context_object_name = "users"


class UserCreateView(SuccessMessageMixin, CreateView):
    """Регистрация: после успеха — редирект на страницу входа."""

    model = User
    form_class = UserForm
    template_name = "users/form.html"
    success_url = reverse_lazy("login")
    success_message = _("User successfully registered")
    extra_context = {
        "title": _("Sign up"),
        "button_text": _("Register"),
    }


class UserUpdateView(SelfOnlyMixin, SuccessMessageMixin, UpdateView):
    """Править можно только себя; после успеха — список пользователей."""

    model = User
    form_class = UserForm
    template_name = "users/form.html"
    success_url = reverse_lazy("users")
    success_message = _("User successfully updated")
    extra_context = {
        "title": _("Edit user"),
        "button_text": _("Change"),
    }


class UserDeleteView(SelfOnlyMixin, DeleteProtectionMixin, SuccessMessageMixin, DeleteView):
    """Удалять можно только себя и только если нет связанных задач."""

    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users")
    success_message = _("User successfully deleted")
    protected_message = _("Cannot delete user")
    extra_context = {
        "title": _("Delete user"),
        "button_text": _("Yes, delete"),
    }


class UserLoginView(SuccessMessageMixin, LoginView):
    """Вход: после успеха — главная (LOGIN_REDIRECT_URL)."""

    template_name = "users/login.html"
    authentication_form = LoginForm
    success_message = _("You are logged in")


class UserLogoutView(LogoutView):
    """POST /logout/: сообщение после сброса сессии, иначе flash пропадёт."""

    next_page = reverse_lazy("index")

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.info(request, _("You are logged out"))
        return response
