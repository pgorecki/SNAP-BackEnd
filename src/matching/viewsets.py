from django.shortcuts import get_object_or_404
from core.viewsets import ModelViewSet
from core.permissions import IsAdmin, IsAgencyMember
from core.validation import validate_fields_with_rules
from .models import MatchingConfig, ClientMatching, ClientMatchingHistory, ClientMatchingNote
from .serializers import (
    MatchingConfigReader, MatchingConfigWriter,
    ClientMatchingReader, ClientMatchingWriter,
    ClientMatchingHistoryReader, ClientMatchingHistoryWriter,
    ClientMatchingNoteReader, ClientMatchingNoteWriter,
)


class MatchingConfigViewset(ModelViewSet):
    queryset = MatchingConfig.objects.all()
    read_serializer_class = MatchingConfigReader
    write_serializer_class = MatchingConfigWriter
    permission_classes = [IsAdmin | IsAgencyMember]
    # filterset_class = ...

    def get_queryset(self):
        return MatchingConfig.objects.for_user(self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ClientMatchingViewset(ModelViewSet):
    queryset = ClientMatching.objects.all()
    read_serializer_class = ClientMatchingReader
    write_serializer_class = ClientMatchingWriter
    permission_classes = [IsAdmin | IsAgencyMember]
    # filterset_class = ...

    # def get_queryset(self):
    #     return MatchingConfig.objects.for_user(self.request.user)

    def validate(self, request, data, action):
        validate_fields_with_rules(request.user, data, client='can_read_client', program='can_read_program')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ClientMatchingHistoryViewset(ModelViewSet):
    read_serializer_class = ClientMatchingHistoryReader
    write_serializer_class = ClientMatchingHistoryWriter

    def get_queryset(self):
        return ClientMatchingHistory.objects.filter(client_matching=self.kwargs.get('client_matching_pk', None))

    def perform_create(self, serializer):
        client_matching = get_object_or_404(ClientMatching, pk=self.kwargs.get('client_matching_pk', None))
        serializer.save(created_by=self.request.user, client_matching=client_matching)


class ClientMatchingNoteViewset(ModelViewSet):
    read_serializer_class = ClientMatchingNoteReader
    write_serializer_class = ClientMatchingNoteWriter

    def get_queryset(self):
        return ClientMatchingNote.objects.filter(client_matching=self.kwargs.get('client_matching_pk', None))

    def perform_create(self, serializer):
        client_matching = get_object_or_404(ClientMatching, pk=self.kwargs.get('client_matching_pk', None))
        serializer.save(created_by=self.request.user, client_matching=client_matching)
