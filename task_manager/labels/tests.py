"""CRUD меток: только для залогиненных, уникальное имя, нельзя удалить занятую."""

from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.users.models import User

PASSWORD = "qwerty"


class LabelCrudTest(TestCase):
    """Тесты шага «CRUD меток»."""

    fixtures = ["users.json", "statuses.json", "labels.json", "tasks.json"]

    def setUp(self):
        self.user = User.objects.get(username="hexlet")
        self.used_label = Label.objects.get(name="Important")
        self.free_label = Label.objects.get(name="Bug")

    def test_list_requires_login(self):
        response = self.client.get(reverse("labels"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_list_for_logged_in_user(self):
        self.client.login(username="hexlet", password=PASSWORD)
        response = self.client.get(reverse("labels"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Important")
        self.assertContains(response, "Bug")
        self.assertContains(response, "Создать метку")
        self.assertContains(response, "Изменить")
        self.assertContains(response, "Удалить")

    def test_create_page_has_name_field(self):
        self.client.login(username="hexlet", password=PASSWORD)
        response = self.client.get(reverse("label_create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="name"')
        self.assertContains(response, 'id="id_name"')
        self.assertContains(response, "Имя")
        self.assertContains(response, "Создать")

    def test_create_label(self):
        self.client.login(username="hexlet", password=PASSWORD)
        response = self.client.post(
            reverse("label_create"),
            {"name": "Feature"},
            follow=True,
        )
        self.assertRedirects(
            response, reverse("labels"), status_code=302, target_status_code=200
        )
        self.assertTrue(Label.objects.filter(name="Feature").exists())
        self.assertContains(response, "Метка успешно создана")

    def test_create_duplicate_name(self):
        self.client.login(username="hexlet", password=PASSWORD)
        response = self.client.post(reverse("label_create"), {"name": "Important"})
        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertTrue("уже существует" in body or "already exists" in body)

    def test_update_label(self):
        self.client.login(username="hexlet", password=PASSWORD)
        response = self.client.post(
            reverse("label_update", args=[self.free_label.pk]),
            {"name": "Hotfix"},
            follow=True,
        )
        self.assertRedirects(
            response, reverse("labels"), status_code=302, target_status_code=200
        )
        self.assertContains(response, "Метка успешно изменена")
        self.free_label.refresh_from_db()
        self.assertEqual(self.free_label.name, "Hotfix")

    def test_delete_unused_label(self):
        self.client.login(username="hexlet", password=PASSWORD)
        response = self.client.post(
            reverse("label_delete", args=[self.free_label.pk]),
            follow=True,
        )
        self.assertRedirects(
            response, reverse("labels"), status_code=302, target_status_code=200
        )
        self.assertContains(response, "Метка успешно удалена")
        self.assertFalse(Label.objects.filter(pk=self.free_label.pk).exists())

    def test_cannot_delete_label_in_use(self):
        self.client.login(username="hexlet", password=PASSWORD)
        response = self.client.post(
            reverse("label_delete", args=[self.used_label.pk]),
            follow=True,
        )
        self.assertContains(response, "Невозможно удалить метку")
        self.assertTrue(Label.objects.filter(pk=self.used_label.pk).exists())

    def test_task_form_allows_multiple_labels(self):
        self.client.login(username="hexlet", password=PASSWORD)
        response = self.client.get(reverse("task_create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="labels"')
        self.assertContains(response, 'id="id_labels"')
        self.assertContains(response, "multiple")

    def test_create_requires_login(self):
        response = self.client.get(reverse("label_create"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_update_requires_login(self):
        response = self.client.get(reverse("label_update", args=[self.free_label.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_delete_requires_login(self):
        response = self.client.post(reverse("label_delete", args=[self.free_label.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)
        self.assertTrue(Label.objects.filter(pk=self.free_label.pk).exists())
