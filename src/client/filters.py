import django_filters
from django.core import exceptions
from rest_framework.exceptions import ValidationError
from django.contrib.postgres.search import SearchVector, SearchQuery


class ClientSearchFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='search_client')

    def search_client(self, qs, name, value):
        value = '&'.join(value.split()) + ':*'
        search_query = SearchQuery(value, search_type='raw')
        if value:
            qs = qs.annotate(
                search=SearchVector('first_name', 'middle_name', 'last_name'),
            ).filter(search=search_query)
        return qs


class ClientFilter(django_filters.FilterSet):
    client = django_filters.CharFilter(method='filter_by_client')

    def filter_by_client(self, qs, name, value):
        try:
            qs = qs.filter(client_id=value)
        except exceptions.ValidationError as e:
            raise ValidationError({'client': e.messages})
        return qs
