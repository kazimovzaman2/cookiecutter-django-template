"""Settings for the local development environment with enabled debugging tools."""

from config.settings.base import *  # noqa: F403

DEBUG = True

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["*"]


# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
    }
}


# JWT
# ------------------------------------------------------------------------------
# https://django-rest-framework-simplejwt.readthedocs.io/en/latest
SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"] = timedelta(days=1)  # noqa: F405
SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"] = timedelta(days=7)  # noqa: F405


# EMAIL
# ---------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = "{{ cookiecutter.project_name }} <{{ cookiecutter.email }}>"
# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = "{{ cookiecutter.project_name }} <{{ cookiecutter.email }}>"
