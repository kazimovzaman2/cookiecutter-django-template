{% if cookiecutter.use_firebase == "yes" -%}
import firebase_admin
from firebase_admin import credentials
{%- endif %}

from config.settings.base import *  # noqa: F403
from config.settings.base import env

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

DATABASES["default"]["CONN_MAX_AGE"] = env.int(  # noqa: F405
    "DJANGO_CONN_MAX_AGE", default=60
)

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": env.list("DJANGO_CACHE_URLS"),
    }
}

INSTALLED_APPS += ["storages"]  # noqa: F405


# STORAGES
# ------------------------------------------------------------------------------
# https://django-storages.readthedocs.io/en/latest/#installation
STORAGES: dict[str, Any] = {  # noqa: F405
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "default_acl": None,
            "file_overwrite": True,
            "location": "media",  # noqa: F405
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "location": "static",
            "default_acl": None,
        },
    },
}

AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_DEFAULT_ACL = None
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_QUERYSTRING_AUTH = False
# DO NOT change these unless you know what you're doing.
_AWS_EXPIRY = 604800  # 7 days
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": f"max-age={_AWS_EXPIRY}, s-maxage={_AWS_EXPIRY}, must-revalidate",  # noqa: E501
}
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_S3_MAX_MEMORY_SIZE = env.int(
    "DJANGO_AWS_S3_MAX_MEMORY_SIZE",
    default=100_000_000,  # 100MB
)
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME", default=None)
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#cloudfront
AWS_S3_CUSTOM_DOMAIN = env("AWS_S3_CUSTOM_DOMAIN", default=None)
AWS_S3_DOMAIN = AWS_S3_CUSTOM_DOMAIN or f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

# STATIC
# ------------------------
STATIC_URL = f"https://{AWS_S3_DOMAIN}/static/"  # noqa: E231

# MEDIA
# ------------------------------------------------------------------------------
MEDIA_URL = f"https://{AWS_S3_DOMAIN}/media/"  # noqa: E231, E501, F405

# PRIVATE MEDIA
# ------------------------------------------------------------------------------
PRIVATE_MEDIA_LOCATION = "private"
PRIVATE_FILE_STORAGE = (
    "hello_django.storage_backends.PrivateMediaRootS3Boto3Storage"  # noqa: E501
)


# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env("DJANGO_EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("DJANGO_EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)


# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=False)

# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = env.bool("DJANGO_SESSION_COOKIE_SECURE")

# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = env.bool("DJANGO_CSRF_COOKIE_SECURE")

# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-trusted-origins
CSRF_TRUSTED_ORIGINS = env.list(
    "DJANGO_CSRF_TRUSTED_ORIGINS", default=["https://*.{{ cookiecutter.domain_name }}"]
)

# https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
SECURE_HSTS_SECONDS = env.int("DJANGO_SECURE_HSTS_SECONDS", default=0)

# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
)

# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
# https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True
)


# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL regex.
ADMIN_URL = env("DJANGO_ADMIN_URL")


# REST Framework
# ------------------------------------------------------------------------------
# https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = (  # noqa: F405
    "rest_framework.renderers.JSONRenderer",
)


{% if cookiecutter.use_firebase == "yes" -%}
# FIREBASE
# ------------------------------------------------------------------------------
firebase_certificate = credentials.Certificate(
    {
        "type": "service_account",
        "project_id": env("FIREBASE_PROJECT_ID"),
        "private_key_id": env("FIREBASE_PRIVATE_KEY_ID"),
        "private_key": env("FIREBASE_PRIVATE_KEY").replace(r"\n", "\n"),
        "client_email": env("FIREBASE_CLIENT_EMAIL"),
        "client_id": env("FIREBASE_CLIENT_ID"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": env("FIREBASE_CLIENT_X509_CERT_URL"),
        "universe_domain": "googleapis.com",
    }
)
firebase_admin.initialize_app(firebase_certificate)
{%- endif %}
