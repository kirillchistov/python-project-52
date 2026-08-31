# Менеджер задач (Python)

[![hexlet-check](https://github.com/kirillchistov/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/kirillchistov/python-project-52/actions)

**Демо на Render:** [https://python-project-52-8j2t.onrender.com/](https://python-project-52-8j2t.onrender.com/)

- Task Manager — система управления задачами, подобная [Redmine](http://www.redmine.org/). В ней можно ставить задачи, назначать исполнителей, менять статусы задач, помечать их метками и фильтровать список по любому из этих признаков. Для работы с системой требуется регистрация и аутентификация: гость видит только главную страницу и список пользователей.
- Проект включает проектирование базы данных, PaaS, мониторинг ошибок, ORM, фреймворк Django, шаблонизацию и Tailwind CSS.

Учебный проект Хекслета: https://ru.hexlet.io/programs/python
Как это должно работать: https://files.hexlet.app/a/0rkpse

## Стек

- Python 3.10+ и пакетный менеджер uv
- Django — ORM, шаблонизатор DjangoTemplates, формы, аутентификация и авторизация
- PostgreSQL в продакшене (psycopg2-binary, dj-database-url), SQLite — для локальной разработки
- Tailwind CSS через django-tailwind-cli и плагин @tailwindcss/forms; раздача статики — WhiteNoise
- django-filter — фильтрация списка задач (следующие шаги)
- WhiteNoise — раздача статики в продакшене
- render.com — PaaS для деплоя, приложение запускается через gunicorn
- python-dotenv — настройки и секреты через переменные окружения
- Ruff — линтер

## Установка (локально)

Нужны Python 3.10+ и [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/kirillchistov/python-project-52.git
cd python-project-52
cp .env.example .env   # затем при желании замените SECRET_KEY
make setup             # зависимости + переводы уже в locale/ + Tailwind + статика + миграции
make dev               # http://127.0.0.1:8000/
```

Секреты хранятся в `.env` (файл не коммитится). На Render те же переменные задаются в дашборде.

## Использование

```bash
make dev          # локальный сервер + watch Tailwind
make tailwind     # разовая сборка CSS (перед collectstatic)
make lint         # проверка кода ruff
make render-start # запуск как на Render (gunicorn)
```

## Деплой на Render (шаг 1)

Один раз: `make build` и `make render-start`.

1. Заведите аккаунт на [render.com](https://render.com). Если вы из РФ, укажите другую страну и «для учебных целей».
2. Закоммитьте и запушьте этот репозиторий на GitHub (когда будете готовы — напишите, закоммитим вместе).
3. **PostgreSQL:** Dashboard → New → PostgreSQL → Create. Скопируйте **Internal Database URL**.
4. **Web Service:** New → Web Service → подключите GitHub-репозиторий.
   - Build Command: `make build`
   - Start Command: `make render-start`
5. **Environment** (Environment Variables):
   - `SECRET_KEY` — длинная случайная строка (Generate)
   - `DEBUG` = `False`
   - `ALLOWED_HOSTS` = `webserver,.onrender.com`
   - `DATABASE_URL` — Internal Database URL из шага 3 (или свяжите базу с сервисом)

---

<details>
<summary>Автоматические тесты Хекслета</summary>

Тесты запускаются на каждый коммит. За запуск отвечает файл `.github/workflows/hexlet-check.yml` — не удаляйте и не переименовывайте ни его, ни репозиторий.

</details>

## Шаг 1: Инициализация

- [x] Посмотрите и разоберитесь в [демонстрации работы проекта](https://files.hexlet.app/a/0rkpse)
- [x] Подготовьте рабочее окружение к разработке: убедитесь, что установлен и настроен редактор кода и окружение готово к работе с проектом.

## Шаг 2: Деплой на Render

- [x] Python 3.10 или выше
- [x] Настройте базовое окружение, которое после старта на (/) выдает приветствие
- [x] Заведите аккаунт на render.com. Укажите страну не РФ «для учебных целей»
- [x] Скрипт `build.sh`, цели Makefile: `build`, `setup`, `render-start`
- [x] Создайте Web Service и PostgreSQL на Render, выполните деплой
- [x] Добавьте в README.md [ссылку на задеплоенное приложение](https://python-project-52-8j2t.onrender.com/)

## Шаг 3: Серверный рендеринг

- [x] Установите пакет django-tailwind-cli в проект
- [x] Соберите стили командой manage.py tailwind build и подключите их в шаблоне тегом {% tailwind_css %}
- [x] Сверстайте макет приложения утилитарными классами Tailwind
- [x] Настройте проект так, чтобы он отдавал шаблон при запросе на главную (роут /)
- [x] Добавьте сборку стилей в скрипт сборки на деплое, перед collectstatic
- [x] Задеплойте результат и убедитесь, что все работает
- [x] Организуйте хранение текстов в i18n и их подстановку в шаблоне

## О Хекслете

[Хекслет](https://ru.hexlet.io/) — школа программирования: авторские программы обучения с практикой, поддержкой наставников и реальными проектами, которые остаются в резюме. Этот репозиторий — один из таких проектов.
