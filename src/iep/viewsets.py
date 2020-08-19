import django.db.utils
from core.exceptions import ApplicationValidationError
from core.viewsets import ModelViewSet
from core.permissions import IsAdmin, IsAgencyMember
from core.validation import validate_fields_with_rules
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
        serializer.save(
            created_by=self.request.user,
            status='awaiting_approval',
        )
