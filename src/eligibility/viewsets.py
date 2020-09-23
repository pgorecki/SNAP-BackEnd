from core.exceptions import ApplicationValidationError
from core.viewsets import ModelViewSet
from core.permissions import AbilityPermission
from core.validation import validate_fields_with_abilities
from .models import (
    Eligibility,
    AgencyEligibilityConfig,
    ClientEligibility,
    EligibilityQueue,
)
from .serializers import (
    EligibilityReader,
    EligibilityWriter,
    AgencyEligibilityConfigReader,
    AgencyEligibilityConfigWriter,
    ClientEligibilityReader,
    ClientEligibilityWriter,
    EligibilityQueueReader,
    EligibilityQueueWriter,
)
from .filters import (
    AgencyEligibilityConfigViewsetFilter,
    ClientEligibilityViewsetFilter,
    EligibilityQueueViewsetFilter,
)


class EligibilityViewset(ModelViewSet):
    read_serializer_class = EligibilityReader
    write_serializer_class = EligibilityWriter
    permission_classes = [AbilityPermission]

    def get_queryset(self):
        return self.request.ability.queryset_for(self.action, Eligibility)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class AgencyEligibilityConfigViewset(ModelViewSet):
    read_serializer_class = AgencyEligibilityConfigReader
    write_serializer_class = AgencyEligibilityConfigWriter
    permission_classes = [AbilityPermission]
    filterset_class = AgencyEligibilityConfigViewsetFilter

    def get_queryset(self):
        return self.request.ability.queryset_for(self.action, AgencyEligibilityConfig)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ClientEligibilityViewset(ModelViewSet):
    read_serializer_class = ClientEligibilityReader
    write_serializer_class = ClientEligibilityWriter
    permission_classes = [AbilityPermission]
    filterset_class = ClientEligibilityViewsetFilter

    def get_queryset(self):
        return self.request.ability.queryset_for(
            self.action, ClientEligibility
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user, eligibility=Eligibility.objects.first()
        )

    def validate(self, request, data, action):
        validate_fields_with_abilities(
            request.ability,
            data,
            client="view",
            eligibility="view",
        )


class EligibilityQueueViewset(ModelViewSet):
    read_serializer_class = EligibilityQueueReader
    write_serializer_class = EligibilityQueueWriter
    permission_classes = [AbilityPermission]
    filterset_class = EligibilityQueueViewsetFilter

    def get_queryset(self):
        return self.request.ability.queryset_for(
            self.action, EligibilityQueue
        ).distinct()

    def validate(self, request, data, action):
        client = data.get("client")
        if action == "create":
            if client.eligibility_queue.filter(status=None).count():
                raise ApplicationValidationError(
                    {"client": ["Client is already in the queue"]}
                )

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            requestor=self.request.user.profile.agency,
            status=None,
        )

    def perform_update(self, serializer):
        status = self.get_object().status
        new_status = serializer.validated_data.get("status")
        if status is None and new_status is not None:
            serializer.save(resolved_by=self.request.user)
        else:
            serializer.save()
