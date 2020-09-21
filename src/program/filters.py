import django_filters
from .models import (
    Program,
    ProgramEligibility,
    Enrollment,
    EnrollmentService,
    EnrollmentServiceType,
)


class ProgramViewsetFilter(django_filters.FilterSet):
    class Meta:
        model = Program
        fields = ["agency"]


class ProgramEligibilityViewsetFilter(django_filters.FilterSet):
    class Meta:
        model = ProgramEligibility
        fields = ["client"]


class EnrollmentViewsetFilter(django_filters.FilterSet):
    class Meta:
        model = Enrollment
        fields = ["client", "program"]


class EnrollmentServiceViewsetFilter(django_filters.FilterSet):
    class Meta:
        model = EnrollmentService
        fields = ["enrollment"]


class EnrollmentServiceTypeViewsetFilter(django_filters.FilterSet):
    class Meta:
        model = EnrollmentServiceType
        fields = ["agency"]
