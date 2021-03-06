from core.viewsets import ModelViewSet
from core.permissions import AbilityPermission
from core.validation import validate_fields_with_abilities
from .filters import (
    ProgramViewsetFilter,
    EnrollmentViewsetFilter,
    EnrollmentServiceViewsetFilter,
    EnrollmentServiceTypeViewsetFilter,
)
from .models import (
    Program,
    Enrollment,
    EnrollmentService,
    EnrollmentServiceType,
)
from .serializers import (
    ProgramReader,
    ProgramWriter,
    EnrollmentReader,
    EnrollmentWriter,
    EnrollmentServiceReader,
    EnrollmentServiceWriter,
    EnrollmentServiceTypeReader,
    EnrollmentServiceTypeWriter,
)


class ProgramViewset(ModelViewSet):
    read_serializer_class = ProgramReader
    write_serializer_class = ProgramWriter
    permission_classes = [AbilityPermission]
    filterset_class = ProgramViewsetFilter

    def get_queryset(self):
        return self.request.ability.queryset_for(self.action, Program)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class EnrollmentViewset(ModelViewSet):
    read_serializer_class = EnrollmentReader
    write_serializer_class = EnrollmentWriter
    permission_classes = [AbilityPermission]
    filterset_class = EnrollmentViewsetFilter

    def get_queryset(self):
        return self.request.ability.queryset_for(self.action, Enrollment).distinct()

    def validate(self, request, data, action):
        validate_fields_with_abilities(
            request.ability, data, client="view", program="view"
        )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class EnrollmentServiceTypeViewset(ModelViewSet):
    read_serializer_class = EnrollmentServiceTypeReader
    write_serializer_class = EnrollmentServiceTypeWriter
    permission_classes = [AbilityPermission]
    filterset_class = EnrollmentServiceTypeViewsetFilter

    def get_queryset(self):
        return self.request.ability.queryset_for(self.action, EnrollmentServiceType)


class EnrollmentServiceViewset(ModelViewSet):
    read_serializer_class = EnrollmentServiceReader
    write_serializer_class = EnrollmentServiceWriter
    permission_classes = [AbilityPermission]
    filterset_class = EnrollmentServiceViewsetFilter

    def get_queryset(self):
        return self.request.ability.queryset_for(
            self.action, EnrollmentService
        ).distinct()
