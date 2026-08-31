"""Пользователь системы: ФИО обязательны, в списках показывается полное имя."""

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Стандартный Django User с обязательными именем и фамилией."""

    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self) -> str:
        full_name = self.get_full_name().strip()
        return full_name or self.username
