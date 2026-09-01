"""CRUD статусов: только для залогиненных, уникальное имя."""

from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.users.models import User

PASSWORD = "qwerty"


class StatusCrudTest(TestCase):
    """Тесты шага «CRUD статусов»."""

    fixtures = ["users.json", "statuses.json"]

    def setUp(self):
        self.user = User.objects.get(username="hexlet")
        self.status = Status.objects.get(name="New")

    def test_list_requires_login(self):
        response = self.client.get(reverse("statuses"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_list_for_logged_in_user(self):
        self.client.login(username="hexlet", password=PASSWORD)
        response = self.client.get(reverse("statuses"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "New")
        self.assertContains(response, "In progress")
        self.assertContains(response, "Создать статус")
        self.assertContains(response, "Изменить")
        self.assertContains(response, "Удалить")

    def test_create_page_has_name_field(self):
        self.client.login(username="hexlet", password=PASSWORD)
        response = self.client.get(reverse("status_create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="name"')
        self.assertContains(response, 'id="id_name"')
        self.assertContains(response, "Имя")
        self.assertContains(response, "Создать")

    def test_create_status(self):
        self.client.login(username="hexlet", password=PASSWORD)
        response = self.client.post(
            reverse("status_create"),
            {"name": "On review"},
            follow=True,
        )
        self.assertRedirects(
            response, reverse("statuses"), status_code=302, target_status_code=200
        )
        self.assertTrue(Status.objects.filter(name="On review").exists())
        self.assertContains(response, "Статус успешно создан")

    def test_create_duplicate_name(self):
        self.client.login(username="hexlet", password=PASSWORD)
        response = self.client.post(reverse("status_create"), {"name": "New"})
        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertTrue("уже существует" in body or "already exists" in body)

    def test_update_status(self):
        self.client.login(username="hexlet", password=PASSWORD)
        response = self.client.post(
            reverse("status_update", args=[self.status.pk]),
            {"name": "Open"},
            follow=True,
        )
        self.assertRedirects(
            response, reverse("statuses"), status_code=302, target_status_code=200
        )
        self.assertContains(response, "Статус успешно изменен")
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, "Open")

    def test_delete_status(self):
        self.client.login(username="hexlet", password=PASSWORD)
        response = self.client.post(
            reverse("status_delete", args=[self.status.pk]),
            follow=True,
        )
        self.assertRedirects(
            response, reverse("statuses"), status_code=302, target_status_code=200
        )
        self.assertContains(response, "Статус успешно удален")
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())

    def test_create_requires_login(self):
        response = self.client.get(reverse("status_create"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_update_requires_login(self):
        response = self.client.get(reverse("status_update", args=[self.status.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_delete_requires_login(self):
        response = self.client.post(reverse("status_delete", args=[self.status.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)
        self.assertTrue(Status.objects.filter(pk=self.status.pk).exists())
