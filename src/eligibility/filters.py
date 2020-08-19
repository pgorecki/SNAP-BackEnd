import django_filters
from core.exceptions import ApplicationValidationError
from .models import AgencyEligibilityConfig, ClientEligibility, EligibilityQueue


class AgencyEligibilityConfigViewsetFilter(django_filters.FilterSet):
    class Meta:
        model = AgencyEligibilityConfig
        fields = ['agency']


class ClientEligibilityViewsetFilter(django_filters.FilterSet):
    class Meta:
        model = ClientEligibility
        fields = ['client']


class EligibilityQueueViewsetFilter(django_filters.FilterSet):
    type = django_filters.CharFilter(method='filter_by_type')

    def filter_by_type(self, qs, name, value):
        if value == 'new':
            return qs.filter(status=None, client__is_new=True)
        elif value == 'existing':
            return qs.filter(status=None, client__is_new=False)
        elif value == 'historical':
            return qs.exclude(status=None)
        else:
            raise ApplicationValidationError({'type': ['Allowed values are: [new|existing|historical]']})
        return qs

    class Meta:
        model = EligibilityQueue
        fields = ['client', 'requestor', 'resolved_by', 'status', 'type']
