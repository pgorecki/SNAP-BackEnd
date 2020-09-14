import django_filters
from core.exceptions import ApplicationValidationError
from .choices import IEPStatus
from .models import ClientIEP


class ClientIEPViewsetFilter(django_filters.FilterSet):
    type = django_filters.CharFilter(method='filter_by_type')

    def filter_by_type(self, qs, name, value):
        status = [IEPStatus.IN_ORIENTATION, IEPStatus.NOT_ELIGIBLE, IEPStatus.IN_PLANNING, IEPStatus.IN_PROGRESS]
        if value == 'new':
            return qs.filter(status__in=status, client__is_new=True)
        elif value == 'existing':
            return qs.filter(status__in=status, client__is_new=False)
        elif value == 'historical':
            return qs.filter(status__in=[IEPStatus.ENDED, IEPStatus.NOT_ELIGIBLE])
        else:
            raise ApplicationValidationError({'type': ['Allowed values are: [new|existing|historical]']})
        return qs

    class Meta:
        model = ClientIEP
        fields = ['client', 'status', 'type']
