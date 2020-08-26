from django.core import exceptions
import django_filters
from rest_framework.exceptions import ValidationError
from .models import Response


class ResponseFilter(django_filters.FilterSet):
    context = django_filters.CharFilter(method='filter_by_response_context')

    def filter_by_response_context(self, qs, name, value):
        try:
            qs = qs.filter(response_context_id=value)
        except exceptions.ValidationError as e:
            raise ValidationError({'context': e.messages})
        return qs

    class Meta:
        model = Response
        fields = ['client', 'context']
