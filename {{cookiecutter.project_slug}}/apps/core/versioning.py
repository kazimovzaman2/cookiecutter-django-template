"""Custom versioning classes for the API."""

from rest_framework.versioning import URLPathVersioning


class Versioning(URLPathVersioning):
    """Custom versioning class for the API. Allows api to be used only v1."""

    default_version = 1
    allowed_versions = (1, 2)
    version_param = "v"
