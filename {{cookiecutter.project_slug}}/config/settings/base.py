"""Base settings to build other settings files upon."""

import os
import re
from pathlib import Path
from typing import Any
from datetime import timedelta

from django.utils.translation import gettext_lazy as _
from environ import Env

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = Env()
env.read_env(os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/
DEBUG = env.bool("DJANGO_DEBUG", False)
DOMAIN = env("DJANGO_DOMAIN", "{{ cookiecutter.domain_name }}")

# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY")

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "django_filters",
    "import_export",
    "drf_spectacular",
    "drf_standardized_errors",
    # Health checkers
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.storage",
    "health_check.contrib.migrations",
    "health_check.contrib.celery",
    "health_check.contrib.celery_ping",
    "health_check.contrib.psutil",
    "health_check.contrib.redis",
]

LOCAL_APPS = [
    "apps.core.apps.CoreConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES: list[dict[str, Any]] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True


# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]


# Password validation
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # noqa: E501
    },
]


# Internationalization
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/5.2/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Baku"
USE_I18N = True
USE_TZ = True
LANGUAGES = (
    ("en", _("English")),
    ("ru", _("Russian")),
    ("az", _("Azerbaijani")),
)
LOCALE_PATHS = (BASE_DIR / "locale/",)


# STATIC
# ------------------------------------------------------------------------------
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/
STATIC_URL = "static/"

# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(BASE_DIR / "staticfiles")

# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(BASE_DIR / "static")]
# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field


# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(BASE_DIR / "media")
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [
    ("{{ cookiecutter.author_name }}", "{{ cookiecutter.email }}"),
]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS


# Django REST Framework
# ------------------------------------------------------------------------------
# DRF - https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",
    "DEFAULT_SCHEMA_CLASS": "drf_standardized_errors.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "apps.core.pagination.StandardResultsSetPagination",
    "PAGE_SIZE": 10,
}


# CORS HEADERS
# ------------------------------------------------------------------------------
# https://github.com/adamchainz/django-cors-headers#setup
CORS_URLS_REGEX = re.compile(r"^/api/.*$")
CORS_ALLOW_ALL_ORIGINS = env.bool("DJANGO_CORS_ALLOW_ALL_ORIGINS", default=False)
CORS_ALLOWED_ORIGINS = env.list("DJANGO_CORS_ALLOWED_ORIGINS", default=[])
CORS_ALLOWED_ORIGIN_REGEXES = env.list("DJANGO_CORS_ALLOWED_ORIGIN_REGEXES", default=[])


# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"


# DRF spectacular
# ------------------------------------------------------------------------------
# https://drf-spectacular.readthedocs.io/en/latest

DISABLE_API_DOC = env.bool("DISABLE_API_DOC", False)

SPECTACULAR_SETTINGS = {
    "TITLE": "{{ cookiecutter.project_name }} API",
    "DESCRIPTION": "{{ cookiecutter.project_description }}",
    "VERSION": "{{ cookiecutter.version }}",
    "SERVE_INCLUDE_SCHEMA": False,
    "POSTPROCESSING_HOOKS": [
        "drf_standardized_errors.openapi_hooks.postprocess_schema_enums"
    ],
    "SWAGGER_UI_SETTINGS": {
        "persistAuthorization": True,
    },
    "ENUM_NAME_OVERRIDES": {
        "ValidationErrorEnum": "drf_standardized_errors.openapi_serializers.ValidationErrorEnum.choices",
        "ClientErrorEnum": "drf_standardized_errors.openapi_serializers.ClientErrorEnum.choices",
        "ServerErrorEnum": "drf_standardized_errors.openapi_serializers.ServerErrorEnum.choices",
        "ErrorCode401Enum": "drf_standardized_errors.openapi_serializers.ErrorCode401Enum.choices",
        "ErrorCode403Enum": "drf_standardized_errors.openapi_serializers.ErrorCode403Enum.choices",
        "ErrorCode404Enum": "drf_standardized_errors.openapi_serializers.ErrorCode404Enum.choices",
        "ErrorCode405Enum": "drf_standardized_errors.openapi_serializers.ErrorCode405Enum.choices",
        "ErrorCode406Enum": "drf_standardized_errors.openapi_serializers.ErrorCode406Enum.choices",
        "ErrorCode415Enum": "drf_standardized_errors.openapi_serializers.ErrorCode415Enum.choices",
        "ErrorCode429Enum": "drf_standardized_errors.openapi_serializers.ErrorCode429Enum.choices",
        "ErrorCode500Enum": "drf_standardized_errors.openapi_serializers.ErrorCode500Enum.choices",
    },
}


# JWT
# ------------------------------------------------------------------------------
# https://django-rest-framework-simplejwt.readthedocs.io/en/latest
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=90),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "SIGNING_KEY": SECRET_KEY,
    "ALGORITHM": "HS256",
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",  # noqa: E501
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=20),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",  # noqa: E501
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",  # noqa: E501
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",  # noqa: E501
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",  # noqa: E501
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",  # noqa: E501
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",  # noqa: E501
}


# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING_LEVEL = env("DJANGO_LOGGING_LEVEL", default="INFO")
LOGGING: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
    },
    "formatters": {
        "simple": {
            "format": "{levelname} {asctime} {message}",
            "style": "{",
        },
        "verbose": {
            "format": "{name} {levelname} {asctime} {module} {process:d} {thread:d} {message}",  # noqa: E501
            "style": "{",
        },
        "json": {
            "()": "apps.logging.formatters.JSONFormatter",
            "fmt_keys": {
                "level": "levelname",
                "message": "message",
                "timestamp": "timestamp",
                "logger": "name",
                "module": "module",
                "function": "funcName",
                "line": "lineno",
                "thread_name": "threadName",
            },
        },
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
            "formatter": "verbose",
            "include_html": True,
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "mail_admins"],
            "level": LOGGING_LEVEL,
        },
        "django": {
            "level": LOGGING_LEVEL,
            "handlers": ["console", "mail_admins"],
            "propagate": False,
        },
    },
}


# Email
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = env(
    "DJANGO_EMAIL_SUBJECT_PREFIX", default="[{{ cookiecutter.project_slug }}]"
)


# CELERY
# ------------------------------------------------------------------------------
CELERY_broker_url = env("CELERY_BROKER_URL")
result_backend = env("CELERY_RESULT_BACKEND")
accept_content = ["application/json"]
task_serializer = "json"
broker_connection_retry = False
broker_connection_retry_on_startup = False

# DJANGO HEALTH CHECK
BROKER_URL = env("DJANGO_BROKER_URL")
REDIS_URL = env("DJANGO_REDIS_URL")


{% if cookiecutter.use_lsim == "yes" -%}
# Sms sender service
SMS_SENDER: dict[str, Any] = {
    "BACKEND": "apps.sms.backends.DummySmsSender",
}
{%- endif %}
