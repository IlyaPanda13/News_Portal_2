from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-l3op9tl*stqt=j9v@eq-*a))i(*jzsml4vdg=%9gujl4=%w!0r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_apscheduler',

    # allauth apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex',

    'news.apps.NewsConfig',
]

SOCIALACCOUNT_PROVIDERS = {
    'yandex': {
        'APP': {
            'client_id': '848039503f5a4d8d88da699898bd9def',
            'secret': '0af5d92a52e741dab5ce9117b978308c',
            'key': ''
        },
        'SCOPE': ['login:email', 'login:info'],
    }
}

SOCIALACCOUNT_URL_PREFIX = 'social/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'newsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Важно для allauth
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'newsite.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'ru-ru'  # Изменил на русский
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Для production

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки для разработки
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
]

# Если используете HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Настройки allauth
SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Стандартные настройки
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/news'
LOGOUT_REDIRECT_URL = '/news'
ACCOUNT_LOGOUT_REDIRECT_URL = '/news'
ACCOUNT_LOGOUT_ON_GET = False
ACCOUNT_EMAIL_VERIFICATION = 'none'

# Настройки аккаунта
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_VERIFICATION = 'none'  # Временно отключаем подтверждение email
ACCOUNT_CONFIRM_EMAIL_ON_GET = False
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_LOGOUT_ON_GET = False
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
ACCOUNT_LOGIN_ON_PASSWORD_RESET = False

# Разрешить регистрацию через социальные сети
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_EMAIL_REQUIRED = False

LOGIN_URL = '/accounts/login/'

# Настройки групп и прав
AUTHOR_GROUP_NAME = 'authors'
COMMON_GROUP_NAME = 'common'

# Автоматическое добавление в группу при регистрации
ACCOUNT_SIGNUP_GROUP_ASSIGNMENT = {
    'default': COMMON_GROUP_NAME,
}

# Права для групп
GROUP_PERMISSIONS = {
    'common': [
        'news.view_post',
        'news.add_comment',  # если будут комментарии
    ],
    'authors': [
        'news.view_post',
        'news.add_post',
        'news.change_post',
        'news.delete_post',
        'news.add_comment',
        'news.change_comment',
        'news.delete_comment',
    ]
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'IlyaPandatest'
EMAIL_HOST_PASSWORD = 'ucpfdjtlggwvmgba'
DEFAULT_FROM_EMAIL = 'IlyaPandatest@yandex.ru'


ADMINS = [
    ('Admin, admin@example.com'),
]

SERVER_EMAIL = 'ilya.samoilov777@yandex.ru'

# Настройка APScheduler
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
APSCHEDULER_RUN_NOW_TIMEOUT = 25