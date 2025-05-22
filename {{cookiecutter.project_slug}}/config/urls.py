from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenRefreshView,
    TokenVerifyView,
    TokenObtainPairView,
)

urlpatterns = [
    path(
        "api/",
        include(
            [
                # Simple jwt
                path(
                    "jwt/create/",
                    TokenObtainPairView.as_view(),
                    name="token_create",
                ),
                path(
                    "jwt/refresh/",
                    TokenRefreshView.as_view(),
                    name="token_refresh",
                ),
                path(
                    "jwt/blacklist/",
                    TokenBlacklistView.as_view(),
                    name="token_blacklist",
                ),
                path(
                    "jwt/verify/",
                    TokenVerifyView.as_view(),
                    name="token_verify",
                ),
            ]
        ),
    ),
    # Health check endpoint
    path("ht/", include("health_check.urls")),
    path(settings.ADMIN_URL, admin.site.urls),
]

if not settings.DISABLE_API_DOC:
    urlpatterns += [
        # DRF Spectacular (API schema)
        path(
            "api/schema/",
            SpectacularAPIView.as_view(),
            name="schema",
        ),
        # DRF Spectacular UIs:
        path(
            "api/schema/swagger-ui/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path(
            "api/schema/redoc/",
            SpectacularRedocView.as_view(url_name="schema"),
            name="redoc",
        ),
        # Django REST Framework browsable API.
        path("api-auth/", include("rest_framework.urls")),
    ]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
