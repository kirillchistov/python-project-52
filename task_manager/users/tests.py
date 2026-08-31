"""CRUD пользователей: регистрация, список, правка, удаление, вход и выход."""

from django.test import TestCase
from django.urls import reverse

from task_manager.users.models import User

PASSWORD = "qwerty"


class UserCrudTest(TestCase):
    """Тесты шага «Пользователи и аутентификация»."""

    fixtures = ["users.json"]

    def setUp(self):
        self.user = User.objects.get(username="hexlet")
        self.other = User.objects.get(username="another")

    def test_users_list_available_without_login(self):
        response = self.client.get(reverse("users"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "hexlet")
        self.assertContains(response, "another")
        self.assertContains(response, "Изменить")
        self.assertContains(response, "Удалить")

    def test_create_page_has_standard_fields(self):
        response = self.client.get(reverse("user_create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'id="id_username"')
        self.assertContains(response, "Имя")
        self.assertContains(response, "Фамилия")
        self.assertContains(response, "Имя пользователя")
        self.assertContains(response, "Пароль")
        self.assertContains(response, "Подтверждение пароля")
        self.assertContains(response, "Зарегистрировать")

    def test_create_user_redirects_to_login(self):
        response = self.client.post(
            reverse("user_create"),
            {
                "first_name": "Tyrion",
                "last_name": "Lannister",
                "username": "tyrion",
                "password1": PASSWORD,
                "password2": PASSWORD,
            },
            follow=True,
        )
        self.assertRedirects(response, reverse("login"), status_code=302, target_status_code=200)
        self.assertTrue(User.objects.filter(username="tyrion").exists())
        self.assertContains(response, "Пользователь успешно зарегистрирован")

    def test_create_duplicate_username(self):
        response = self.client.post(
            reverse("user_create"),
            {
                "first_name": "Copy",
                "last_name": "Cat",
                "username": "hexlet",
                "password1": PASSWORD,
                "password2": PASSWORD,
            },
        )
        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertTrue("уже существует" in body or "already exists" in body)

    def test_login_redirects_home(self):
        response = self.client.post(
            reverse("login"),
            {"username": "hexlet", "password": PASSWORD},
            follow=True,
        )
        self.assertRedirects(response, reverse("index"), status_code=302, target_status_code=200)
        self.assertContains(response, "Вы залогинены")
        self.assertContains(response, "Выход")

    def test_login_page_fields(self):
        response = self.client.get(reverse("login"))
        self.assertContains(response, "Имя пользователя")
        self.assertContains(response, "Пароль")
        self.assertContains(response, "Войти")
        self.assertContains(response, 'id="id_username"')
        self.assertContains(response, 'id="id_password"')

    def test_logout(self):
        self.client.login(username="hexlet", password=PASSWORD)
        response = self.client.post(reverse("logout"), follow=True)
        self.assertContains(response, "Вы разлогинены")
        self.assertContains(response, "Вход")

    def test_update_own_user(self):
        self.client.login(username="hexlet", password=PASSWORD)
        response = self.client.post(
            reverse("user_update", args=[self.user.pk]),
            {
                "first_name": "New",
                "last_name": "Name",
                "username": "hexlet",
                "password1": PASSWORD,
                "password2": PASSWORD,
            },
            follow=True,
        )
        self.assertRedirects(response, reverse("users"), status_code=302, target_status_code=200)
        self.assertContains(response, "Пользователь успешно изменен")
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "New")

    def test_cannot_update_another_user(self):
        self.client.login(username="hexlet", password=PASSWORD)
        response = self.client.get(
            reverse("user_update", args=[self.other.pk]),
            follow=True,
        )
        self.assertContains(response, "У вас нет прав для изменения")

    def test_cannot_delete_another_user(self):
        self.client.login(username="hexlet", password=PASSWORD)
        response = self.client.post(
            reverse("user_delete", args=[self.other.pk]),
            follow=True,
        )
        self.assertContains(response, "У вас нет прав для изменения")
        self.assertTrue(User.objects.filter(pk=self.other.pk).exists())

    def test_delete_own_user(self):
        self.client.login(username="hexlet", password=PASSWORD)
        response = self.client.post(
            reverse("user_delete", args=[self.user.pk]),
            follow=True,
        )
        self.assertRedirects(response, reverse("users"), status_code=302, target_status_code=200)
        self.assertContains(response, "Пользователь успешно удален")
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_update_requires_login(self):
        response = self.client.get(reverse("user_update", args=[self.user.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)
