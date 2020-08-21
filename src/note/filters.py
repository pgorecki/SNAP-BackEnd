from django.core import exceptions
import django_filters
from rest_framework.exceptions import ValidationError


class NoteFilter(django_filters.FilterSet):
    source_id = django_filters.CharFilter(method='filter_by_source_id')

    def filter_by_source_id(self, qs, name, value):
        try:
            qs = qs.filter(source_id=value)
        except exceptions.ValidationError as e:
            raise ValidationError({'source_id': e.messages})
        return qs
