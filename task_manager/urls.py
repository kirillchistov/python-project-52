"""Корневые URL: главная, админка, пользователи, вход и выход."""

from django.contrib import admin
from django.urls import include, path

from task_manager.users.views import UserLoginView, UserLogoutView
from task_manager.views import IndexView, trigger_error

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("sentry-debug/", trigger_error, name="sentry_debug"),
    path("admin/", admin.site.urls),
    path("users/", include("task_manager.users.urls")),
    path("statuses/", include("task_manager.statuses.urls")),
    path("labels/", include("task_manager.labels.urls")),
    path("tasks/", include("task_manager.tasks.urls")),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
]
