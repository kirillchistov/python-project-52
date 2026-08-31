"""Формы регистрации и правки: стандартные name/id полей Django (id_username)."""

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from task_manager.users.models import User


class UserForm(UserCreationForm):
    """Имя, фамилия, логин и пара паролей — как в демо."""

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["first_name"].label = _("First name")
        self.fields["last_name"].label = _("Last name")
        self.fields["username"].label = _("Username")
        self.fields["password1"].label = _("Password")
        self.fields["password2"].label = _("Password confirmation")
        for field in self.fields.values():
            css = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{css} mt-1 block w-full".strip()

    def clean_username(self):
        """Уникальность без ложного срабатывания при правке своего логина."""
        username = self.cleaned_data.get("username")
        users = User.objects.filter(username__iexact=username)
        if self.instance.pk:
            users = users.exclude(pk=self.instance.pk)
        if username and users.exists():
            self._update_errors(
                ValidationError(
                    {
                        "username": self.instance.unique_error_message(
                            self._meta.model, ["username"]
                        )
                    }
                )
            )
        else:
            return username


class LoginForm(AuthenticationForm):
    """Поля входа: Имя пользователя и Пароль."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = _("Username")
        self.fields["password"].label = _("Password")
        for field in self.fields.values():
            css = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{css} mt-1 block w-full".strip()

