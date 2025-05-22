"""Pagination classes for the views and viewsets."""

from typing import Any, Optional

from django.db.models import QuerySet
from rest_framework.pagination import BasePagination, PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class NullPagination(BasePagination):
    """Null pagination class, performs no pagination."""

    def paginate_queryset(
        self,
        queryset: QuerySet[Any],
        request: Request,
        view: Optional[APIView] = None,
    ) -> list[Any]:
        self.count = queryset.count()
        return list(queryset)

    def get_paginated_response(self, data: list[Any]) -> Response:
        return Response({"count": self.count, "results": data})

    def get_paginated_response_schema(self, schema: dict[Any, Any]) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "count": {
                    "type": "integer",
                    "example": 123,
                },
                "results": schema,
            },
        }


class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination class. Sets page size to 10."""

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 1000
