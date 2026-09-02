"""CRUD задач: автор ставится сам, удаляет только автор, PROTECT на связях."""

from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User

PASSWORD = "qwerty"


class TaskCrudTest(TestCase):
    """Тесты шага «CRUD задач»."""

    fixtures = ["users.json", "statuses.json", "labels.json", "tasks.json"]

    def setUp(self):
        self.author = User.objects.get(username="hexlet")
        self.other = User.objects.get(username="another")
        self.status = Status.objects.get(name="New")
        self.label = Label.objects.get(name="Important")
        self.task = Task.objects.get(name="Prepare report")

    def test_list_requires_login(self):
        response = self.client.get(reverse("tasks"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_list_for_logged_in_user(self):
        self.client.login(username="hexlet", password=PASSWORD)
        response = self.client.get(reverse("tasks"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Prepare report")
        self.assertContains(response, "Создать задачу")
        self.assertContains(response, "Показать")
        self.assertContains(response, "Изменить")
        self.assertContains(response, "Удалить")

    def test_detail_shows_fields_and_labels(self):
        self.client.login(username="hexlet", password=PASSWORD)
        response = self.client.get(reverse("task_detail", args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Просмотр задачи")
        self.assertContains(response, "Prepare report")
        self.assertContains(response, "Demo task")
        self.assertContains(response, "Important")
        self.assertContains(response, "Автор")
        self.assertContains(response, "Исполнитель")
        self.assertContains(response, "Статус")
        self.assertContains(response, "Метки")

    def test_create_page_has_form_fields(self):
        self.client.login(username="hexlet", password=PASSWORD)
        response = self.client.get(reverse("task_create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="name"')
        self.assertContains(response, 'id="id_name"')
        self.assertContains(response, "Имя")
        self.assertContains(response, "Описание")
        self.assertContains(response, "Статус")
        self.assertContains(response, "Исполнитель")
        self.assertContains(response, "Метки")
        self.assertContains(response, "Создать")
        self.assertContains(response, 'name="labels"')
        self.assertContains(response, 'id="id_labels"')
        self.assertContains(response, "multiple")

    def test_create_task_sets_author(self):
        self.client.login(username="hexlet", password=PASSWORD)
        response = self.client.post(
            reverse("task_create"),
            {
                "name": "Write docs",
                "description": "Need docs",
                "status": self.status.pk,
                "executor": self.other.pk,
                "labels": [self.label.pk],
            },
            follow=True,
        )
        self.assertRedirects(
            response, reverse("tasks"), status_code=302, target_status_code=200
        )
        self.assertContains(response, "Задача успешно создана")
        task = Task.objects.get(name="Write docs")
        self.assertEqual(task.author, self.author)
        self.assertEqual(task.executor, self.other)
        self.assertIn(self.label, task.labels.all())

    def test_create_duplicate_name(self):
        self.client.login(username="hexlet", password=PASSWORD)
        response = self.client.post(
            reverse("task_create"),
            {
                "name": "Prepare report",
                "description": "dup",
                "status": self.status.pk,
            },
        )
        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertTrue("уже существует" in body or "already exists" in body)

    def test_update_task(self):
        self.client.login(username="another", password=PASSWORD)
        response = self.client.post(
            reverse("task_update", args=[self.task.pk]),
            {
                "name": "Prepare report",
                "description": "Updated",
                "status": self.status.pk,
                "executor": "",
            },
            follow=True,
        )
        self.assertRedirects(
            response, reverse("tasks"), status_code=302, target_status_code=200
        )
        self.assertContains(response, "Задача успешно изменена")
        self.task.refresh_from_db()
        self.assertEqual(self.task.description, "Updated")

    def test_update_task_with_multiple_labels(self):
        bug = Label.objects.get(name="Bug")
        self.client.login(username="hexlet", password=PASSWORD)
        response = self.client.post(
            reverse("task_update", args=[self.task.pk]),
            {
                "name": "Prepare report",
                "description": "Demo task",
                "status": self.status.pk,
                "labels": [self.label.pk, bug.pk],
            },
            follow=True,
        )
        self.assertRedirects(
            response, reverse("tasks"), status_code=302, target_status_code=200
        )
        self.task.refresh_from_db()
        self.assertEqual(set(self.task.labels.all()), {self.label, bug})

    def test_author_can_delete_task(self):
        self.client.login(username="hexlet", password=PASSWORD)
        response = self.client.post(
            reverse("task_delete", args=[self.task.pk]),
            follow=True,
        )
        self.assertRedirects(
            response, reverse("tasks"), status_code=302, target_status_code=200
        )
        self.assertContains(response, "Задача успешно удалена")
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_non_author_cannot_delete_task(self):
        self.client.login(username="another", password=PASSWORD)
        response = self.client.post(
            reverse("task_delete", args=[self.task.pk]),
            follow=True,
        )
        self.assertContains(response, "Задачу может удалить только ее автор")
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())

    def test_cannot_delete_status_in_use(self):
        self.client.login(username="hexlet", password=PASSWORD)
        response = self.client.post(
            reverse("status_delete", args=[self.status.pk]),
            follow=True,
        )
        self.assertContains(response, "Невозможно удалить статус")
        self.assertTrue(Status.objects.filter(pk=self.status.pk).exists())

    def test_cannot_delete_user_with_tasks(self):
        self.client.login(username="hexlet", password=PASSWORD)
        response = self.client.post(
            reverse("user_delete", args=[self.author.pk]),
            follow=True,
        )
        self.assertContains(response, "Невозможно удалить пользователя")
        self.assertTrue(User.objects.filter(pk=self.author.pk).exists())

    def test_detail_requires_login(self):
        response = self.client.get(reverse("task_detail", args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_create_requires_login(self):
        response = self.client.get(reverse("task_create"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_update_requires_login(self):
        response = self.client.get(reverse("task_update", args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_delete_requires_login(self):
        response = self.client.get(reverse("task_delete", args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)
