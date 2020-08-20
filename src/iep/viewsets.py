import django.db.utils
from core.exceptions import ApplicationValidationError
from core.viewsets import ModelViewSet
from core.permissions import IsAdmin, IsAgencyMember
from core.validation import validate_fields_with_rules
from eligibility.models import EligibilityQueue
from .models import ClientIEP
from .serializers import (
    ClientIEPReader, ClientIEPWriter,
)
from .filters import ClientIEPViewsetFilter


class ClientIEPViewset(ModelViewSet):
    queryset = ClientIEP.objects.all()
    read_serializer_class = ClientIEPReader
    write_serializer_class = ClientIEPWriter
    permission_classes = [IsAdmin | IsAgencyMember]
    filterset_class = ClientIEPViewsetFilter

    def perform_create(self, serializer):
        """
        when new IEP is created, eligibility request is created  (if needed)
        or associated (if already exists) with this iep
        """
        client = serializer.validated_data['client']
        agency = self.request.user.profile.agency
        existing_request = EligibilityQueue.objects.filter(client=client, requestor=agency, status=None).first()

        serializer.save(
            created_by=self.request.user,
            status='awaiting_approval',
            eligibility_request=existing_request or EligibilityQueue.objects.create(client=client, requestor=agency)
        )
