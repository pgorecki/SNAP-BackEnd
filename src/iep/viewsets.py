import django.db.utils
from core.exceptions import ApplicationValidationError
from core.viewsets import ModelViewSet
from core.permissions import AbilityPermission
from core.validation import validate_fields_with_rules
from eligibility.models import EligibilityQueue
from .models import ClientIEP
from .serializers import (
    ClientIEPReader, ClientIEPWriter,
)
from .filters import ClientIEPViewsetFilter


class ClientIEPViewset(ModelViewSet):
    read_serializer_class = ClientIEPReader
    write_serializer_class = ClientIEPWriter
    permission_classes = [AbilityPermission]
    filterset_class = ClientIEPViewsetFilter

    def get_queryset(self):
        return self.request.ability.queryset_for(self.action, ClientIEP).distinct()

    def perform_create(self, serializer):
        """
        when new IEP is created, eligibility request is created  (if needed)
        or associated (if already exists) with this iep
        """
        client = serializer.validated_data['client']
        agency = self.request.user.profile.agency
        if agency is None:
            ApplicationValidationError({'user': 'Agency is not set in your user profile'})
        existing_request = EligibilityQueue.objects.filter(client=client, requestor=agency, status=None).first()

        serializer.save(
            created_by=self.request.user,
            status='awaiting_approval',
            eligibility_request=existing_request or EligibilityQueue.objects.create(client=client, requestor=agency)
        )
