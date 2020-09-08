from core.viewsets import ModelViewSet
from core.permissions import AbilityPermission
from .models import Note
from .serializers import NoteReader, NoteWriter
from .filters import NoteFilter


class NoteViewset(ModelViewSet):
    queryset = Note.objects.all()
    read_serializer_class = NoteReader
    write_serializer_class = NoteWriter
    permission_classes = [AbilityPermission]
    filterset_class = NoteFilter

    def get_queryset(self):
        return self.request.ability.queryset_for(self.action, Note)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
