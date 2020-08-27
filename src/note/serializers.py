from core.serializers import ContentObjectRelatedField, ObjectSerializer, CreatedByReader
from .models import Note


class NoteReader(ObjectSerializer):
    created_by = CreatedByReader(read_only=True)
    source = ContentObjectRelatedField(read_only=True)

    class Meta:
        model = Note
        fields = ('id', 'object', 'text', 'source', 'created_at', 'modified_at', 'created_by')


class NoteWriter(ObjectSerializer):

    class SourceWriter(ContentObjectRelatedField):
        def get_queryset(self):
            return None
    source = SourceWriter()

    class Meta:
        model = Note
        fields = ('text', 'source')
