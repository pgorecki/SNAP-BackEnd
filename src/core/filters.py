from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.postgres.fields import JSONField, ArrayField
from django.contrib.postgres.forms import SimpleArrayField
from django_filters import filterset
from django_filters import rest_framework as filters
from django_filters.rest_framework.filters import Filter


class ArrayFilter(Filter):
    """
    Array filter to tell filterset about  base field class for lookups.
    """

    base_field_class = SimpleArrayField


class AllDjangoFilterBackend(DjangoFilterBackend):
    """
    Filters DRF views by any of the objects properties.
    """

    def get_filter_class(self, view, queryset=None):
        """
        Return the django-filters `FilterSet` used to filter the queryset.
        """
        filter_class = getattr(view, "filter_class", None)
        filter_fields = getattr(view, "filter_fields", None)

        if filter_class or filter_fields:
            return super().get_filter_class(self, view, queryset)

        class AutoFilterSet(self.default_filter_set):
            class Meta:
                exclude = ""
                model = queryset.model
                filter_overrides = {
                    ArrayField: {"filter_class": ArrayFilter},
                    JSONField: {
                        "filter_class": filters.CharFilter,
                        "extra": lambda f: {"lookup_expr": "icontains"},
                    },
                }

        return AutoFilterSet
