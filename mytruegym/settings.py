import os
import dj_database_url
from constants import *


DEBUG = os.environ.get(DEBUG_VALUE) == DEBUG_TRUE

SECRET_KEY = os.environ.get(SECRET_KEY_VALUE)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROOT_URLCONF = "mytruegym.urls"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "django_db",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "db",
        "PORT": "5432"
    }
}

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "sportsmen.apps.SportsmenConfig",
    "calories.apps.CaloriesConfig",
    "ratings.apps.RatingsConfig",
    "storages"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

LANGUAGE_CODE = os.environ.get(LANGUAGE_CODE_VALUE)

LANGUAGES = (
    ("ru", "Russian"),
    ("en", "English")
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)

USE_I18N = True

USE_L10N = True

USE_TZ = True

TIME_ZONE = "UTC"

ALLOWED_HOSTS = ["mytruegym.herokuapp.com", "127.0.0.1", "0.0.0.0", "www.mytruegym.ru"]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.media",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        }
    },
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": [
            "/home/html/jinja2",
        ]
    }
]

WSGI_APPLICATION = "mytruegym.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AWS_ACCESS_KEY_ID = os.environ.get(AWS_ACCESS_KEY_ID_VALUE)
AWS_SECRET_ACCESS_KEY = os.environ.get(AWS_SECRET_ACCESS_KEY_VALUE)
AWS_STORAGE_BUCKET_NAME = os.environ.get(AWS_STORAGE_BUCKET_NAME_VALUE)
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
AWS_LOCATION = "static"
AWS_LOCATION_MEDIA = "media"
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION_MEDIA)
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
DEFAULT_FILE_STORAGE = "mytruegym.storage.MediaStorage"
AWS_DEFAULT_ACL = "public-read"

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get(EMAIL_HOST_USER_VALUE)
EMAIL_HOST_PASSWORD = os.environ.get(EMAIL_HOST_PASSWORD_VALUE)
EMAIL_USE_TLS = True

CELERY_BROKER_URL = os.environ.get(CELERY_BROKER_URL_VALUE)
CELERY_RESULT_BACKEND = os.environ.get(CELERY_RESULT_BACKEND_VALUE)
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"

prod_database = dj_database_url.config(conn_max_age=500)
DATABASES["default"].update(prod_database)
