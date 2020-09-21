from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PageNumberPaginationWithTotalPages(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 1000

    def paginate_queryset(self, queryset, request, view=None):
        self.page_number = request.query_params.get(self.page_query_param, 1)
        self.page_size = self.get_page_size(request)
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("page_number", self.page_number),
                    ("page_size", self.page_size),
                    ("total_pages", self.page.paginator.num_pages),
                    ("results", data),
                ]
            )
        )

    def get_paginated_response_schema(self, schema):
        return {
            "type": "object",
            "properties": {
                "count": {
                    "type": "integer",
                    "example": 1000,
                },
                "next": {
                    "type": "string",
                    "nullable": True,
                },
                "previous": {
                    "type": "string",
                    "nullable": True,
                },
                "page_number": {
                    "type": "integer",
                    "example": 1,
                },
                "page_size": {
                    "type": "integer",
                    "example": 100,
                },
                "total_pages": {
                    "type": "integer",
                    "example": 10,
                },
                "results": schema,
            },
        }
