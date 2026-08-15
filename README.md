# News Portal

Веб-приложение на Django для публикации и чтения новостей и статей.

Пользователи могут регистрироваться, создавать публикации, подписываться на категории и получать уведомления о новых материалах.

## Возможности

* регистрация и авторизация пользователей;
* авторизация через Яндекс;
* публикация, редактирование и удаление статей;
* категории публикаций;
* поиск и фильтрация;
* пагинация;
* подписка на категории;
* разграничение прав пользователей через группы и permissions;
* email-уведомления о новых публикациях;
* периодическая рассылка дайджеста;
* административная панель Django.

## Технологический стек

* Python
* Django
* Django ORM
* PostgreSQL / SQLite
* Celery
* Redis
* Django Allauth
* Yandex OAuth
* HTML / CSS
* Git

## Архитектура

Основная бизнес-логика реализована на Django.

Celery используется для выполнения фоновых задач, связанных с отправкой email-уведомлений. Redis используется в качестве брокера задач.

Права доступа пользователей реализованы средствами Django Groups и Permissions.

## Запуск проекта

### 1. Клонирование

```bash
git clone https://github.com/IlyaPanda13/News_Portal_2.git
cd News_Portal_2
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Переменные окружения

Создайте файл `.env` в корне проекта:

```env
SECRET_KEY=your_secret_key

YANDEX_CLIENT_ID=your_client_id
YANDEX_SECRET=your_secret

EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_email_password
DEFAULT_FROM_EMAIL=your_email
```

### 4. Миграции

```bash
python manage.py migrate
```

### 5. Запуск Django

```bash
python manage.py runserver
```

### 6. Запуск Redis и Celery

Для работы фоновых задач необходимо запустить Redis и Celery worker.

```bash
celery -A newsite worker -l info
```

## Безопасность

Секретные данные не хранятся непосредственно в исходном коде.

Файл `.env` добавлен в `.gitignore` и не должен публиковаться в репозитории.

## Структура проекта

```text
newsite/
├── news/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── tasks.py
│   ├── urls.py
│   ├── templatetags/
│   └── management/
├── templates/
├── static/
├── newsite/
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
└── .env.example
```

## Проект

Учебный backend-проект, созданный для практики разработки веб-приложений на Django, работы с ORM, авторизацией, правами доступа и асинхронными задачами.
