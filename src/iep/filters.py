import django_filters
from core.exceptions import ApplicationValidationError
from .models import ClientIEP


class ClientIEPViewsetFilter(django_filters.FilterSet):
    type = django_filters.CharFilter(method='filter_by_type')

    def filter_by_type(self, qs, name, value):
        if value == 'new':
            return qs.filter(eligibility_request__status=None, client__is_new=True)
        elif value == 'existing':
            return qs.filter(eligibility_request__status=None, client__is_new=False)
        elif value == 'historical':
            return qs.exclude(eligibility_request__status=None)
        else:
            raise ApplicationValidationError({'type': ['Allowed values are: [new|existing|historical]']})
        return qs

    class Meta:
        model = ClientIEP
        fields = ['client', 'status', 'type']
