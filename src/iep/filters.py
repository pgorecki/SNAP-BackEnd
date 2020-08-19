import django_filters
from .models import ClientIEP


class ClientIEPViewsetFilter(django_filters.FilterSet):
    class Meta:
        model = ClientIEP
        fields = ['client', 'status']
