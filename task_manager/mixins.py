"""Общие mixin'ы доступа: логин и «только владелец записи»."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class AuthRequiredMixin(LoginRequiredMixin):
    """Редирект на вход, если пользователь не аутентифицирован."""

    login_url = reverse_lazy("login")


class SelfOnlyMixin(AuthRequiredMixin, UserPassesTestMixin):
    """Править и удалять можно только свою учётную запись."""

    permission_denied_url = reverse_lazy("users")
    permission_denied_message = _("You don't have permission to change")

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.error(self.request, self.permission_denied_message)
        return redirect(self.permission_denied_url)
