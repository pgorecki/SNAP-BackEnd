from core.exceptions import ApplicationValidationError
from core.viewsets import ModelViewSet
from core.permissions import IsAdmin, IsAgencyMember, IsAgencyMemberReadOnly
from core.validation import validate_fields_with_rules
from .models import Eligibility, AgencyEligibilityConfig, ClientEligibility, EligibilityQueue
from .serializers import (
    EligibilityReader, EligibilityWriter,
    AgencyEligibilityConfigReader, AgencyEligibilityConfigWriter,
    ClientEligibilityReader, ClientEligibilityWriter,
    EligibilityQueueReader, EligibilityQueueWriter,
)
from .filters import (
    AgencyEligibilityConfigViewsetFilter,
    ClientEligibilityViewsetFilter,
    EligibilityQueueViewsetFilter
)


class EligibilityViewset(ModelViewSet):
    queryset = Eligibility.objects.all()
    read_serializer_class = EligibilityReader
    write_serializer_class = EligibilityWriter
    permission_classes = [IsAdmin | IsAgencyMemberReadOnly]

    def get_queryset(self):
        return Eligibility.objects.for_user(self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class AgencyEligibilityConfigViewset(ModelViewSet):
    queryset = AgencyEligibilityConfig.objects.all()
    read_serializer_class = AgencyEligibilityConfigReader
    write_serializer_class = AgencyEligibilityConfigWriter
    permission_classes = [IsAdmin | IsAgencyMemberReadOnly]
    filterset_class = AgencyEligibilityConfigViewsetFilter

    def get_queryset(self):
        return AgencyEligibilityConfig.objects.for_user(self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ClientEligibilityViewset(ModelViewSet):
    queryset = ClientEligibility.objects.all()
    read_serializer_class = ClientEligibilityReader
    write_serializer_class = ClientEligibilityWriter
    permission_classes = [IsAdmin | IsAgencyMember]
    filterset_class = ClientEligibilityViewsetFilter

    def get_queryset(self):
        print(('qs', list(ClientEligibility.objects.for_user(self.request.user).all())))
        return ClientEligibility.objects.for_user(self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def validate(self, request, data, action):
        validate_fields_with_rules(request.user, data, client='can_read_client', eligibility='can_read_eligibility')


class EligibilityQueueViewset(ModelViewSet):
    queryset = EligibilityQueue.objects.all()
    read_serializer_class = EligibilityQueueReader
    write_serializer_class = EligibilityQueueWriter
    permission_classes = [IsAdmin | IsAgencyMember]
    filterset_class = EligibilityQueueViewsetFilter

    def validate(self, request, data, action):
        client = data.get('client')
        if action == 'create':
            if client.eligibility_queue.filter(status=None).count():
                raise ApplicationValidationError({'client': ['Client is already in the queue']})

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            requestor=self.request.user.profile.agency,
            status=None,
        )

    def perform_update(self, serializer):
        status = self.get_object().status
        new_status = serializer.validated_data.get('status')
        if status is None and new_status is not None:
            serializer.save(resolved_by=self.request.user)
        else:
            serializer.save()
