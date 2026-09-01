"""Настройки Django.

Секреты — из окружения. Локально SQLite, на Render — PostgreSQL.
ALLOWED_HOSTS всегда содержит webserver. Интерфейс — Tailwind + i18n.
"""

import os
import sys
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "insecure-dev-key-change-in-production")

DEBUG = os.getenv("DEBUG", "True").lower() in {"true", "1", "yes"}


def _allowed_hosts() -> list[str]:
    """Собирает ALLOWED_HOSTS: .env + webserver + хост Render."""
    raw = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,webserver,testserver")
    hosts = [item.strip() for item in raw.split(",") if item.strip()]
    if "webserver" not in hosts:
        hosts.append("webserver")
    if "testserver" not in hosts:
        hosts.append("testserver")
    if ".onrender.com" not in hosts:
        hosts.append(".onrender.com")
    render_host = os.getenv("RENDER_EXTERNAL_HOSTNAME")
    if render_host and render_host not in hosts:
        hosts.append(render_host)
    return hosts


ALLOWED_HOSTS = _allowed_hosts()

CSRF_TRUSTED_ORIGINS = ["https://*.onrender.com"]
render_hostname = os.getenv("RENDER_EXTERNAL_HOSTNAME")
if render_hostname:
    origin = f"https://{render_hostname}"
    if origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(origin)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django_tailwind_cli",
    "task_manager.users",
    "task_manager.statuses",
    "task_manager.labels",
    "task_manager.tasks",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "task_manager.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "task_manager" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "task_manager.wsgi.application"

# Render передаёт DATABASE_URL; без неё — локальный SQLite.
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 3},
    },
]

AUTH_USER_MODEL = "users.User"
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "index"
LOGOUT_REDIRECT_URL = "index"

LANGUAGE_CODE = "ru"
LANGUAGES = [("ru", "Русский")]
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
LOCALE_PATHS = [BASE_DIR / "locale"]

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "assets"]

# Исходный CSS вне STATICFILES_DIRS — иначе WhiteNoise ломает @import "tailwindcss".
TAILWIND_CLI_SRC_CSS = "src/styles.css"
TAILWIND_CLI_DIST_CSS = "css/tailwind.css"
TAILWIND_CLI_VERSION = "4.1.16"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

if "test" in sys.argv:
    STORAGES["staticfiles"] = {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    }

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Логи в stdout — так их забирает Render (Twelve-Factor).
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "[{levelname}] {asctime} {name}: {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
