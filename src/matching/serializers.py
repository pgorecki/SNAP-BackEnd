from rest_framework.utils import model_meta
from core.serializers import ObjectSerializer, CreatedByReader
from client.serializers import ClientReader
from program.serializers import ProgramReader
from .models import MatchingConfig, ClientMatching, ClientMatchingNote, ClientMatchingHistory


class MatchingConfigReader(ObjectSerializer):
    created_by = CreatedByReader(read_only=True)

    class Meta:
        model = MatchingConfig
        fields = ('id', 'object', 'name', 'config', 'created_at', 'modified_at', 'created_by')


class MatchingConfigWriter(MatchingConfigReader):
    pass


class ClientMatchingReader(ObjectSerializer):
    class HistoryReader(ObjectSerializer):
        created_by = CreatedByReader(read_only=True)

        class Meta:
            model = ClientMatchingHistory
            fields = ('id', 'object', 'step', 'outcome', 'created_by', 'created_at')

    class NotesReader(ObjectSerializer):
        created_by = CreatedByReader(read_only=True)

        class Meta:
            model = ClientMatchingNote
            fields = ('id', 'object', 'step', 'note', 'created_by', 'created_at')

    config = MatchingConfigReader()
    client = ClientReader()
    program = ProgramReader()
    notes = NotesReader(many=True, read_only=True)
    history = HistoryReader(many=True, read_only=True)
    created_by = CreatedByReader(read_only=True)

    class Meta:
        model = ClientMatching
        fields = ('id', 'object', 'config', 'client', 'program', 'start_date',
                  'end_date', 'history', 'notes', 'created_at', 'modified_at', 'created_by')


class ClientMatchingWriter(ObjectSerializer):
    class ClientMatchingInlineHistoryWriter(ObjectSerializer):
        class Meta:
            model = ClientMatchingHistory
            fields = ('id', 'step', 'outcome')

    class ClientMatchingInlineNoteWriter(ObjectSerializer):
        class Meta:
            model = ClientMatchingNote
            fields = ('id', 'note')

    # def create(self, validated_data):
    #     # TODO: check access permissions to survey, questions, respondent
    #     # TODO: add transaction
    #     response = Response.objects.create(
    #         survey=validated_data['survey'],
    #         respondent=validated_data['respondent'],
    #         created_by=validated_data['created_by'],
    #     )
    #     for ans in validated_data['answers']:
    #         Answer.objects.create(response=response, **ans)

    #     return response

    history = ClientMatchingInlineHistoryWriter(many=True, required=False)
    notes = ClientMatchingInlineNoteWriter(many=True, required=False)

    def update(self, instance, validated_data):
        print(validated_data)
        user = self.context['request'].user
        for note_data in validated_data.get('notes', []):
            if not note_data.get('id', None):
                instance.notes.create(created_by=user, **note_data)
        for history_data in validated_data.get('history', []):
            if not history_data.get('id', None):
                instance.history.create(created_by=user, **history_data)

        info = model_meta.get_field_info(instance)
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                pass
            else:
                setattr(instance, attr, value)

        instance.save()

        return instance

    class Meta:
        model = ClientMatching
        fields = ('config', 'client', 'program', 'start_date', 'end_date', 'notes', 'history')


class ClientMatchingHistoryReader(ObjectSerializer):
    created_by = CreatedByReader(read_only=True)

    class Meta:
        model = ClientMatchingHistory
        fields = ('id', 'object', 'step', 'outcome', 'created_by', 'created_at')


class ClientMatchingHistoryWriter(ObjectSerializer):
    class Meta:
        model = ClientMatchingHistory
        fields = ('step', 'outcome')


class ClientMatchingNoteReader(ObjectSerializer):
    created_by = CreatedByReader(read_only=True)

    class Meta:
        model = ClientMatchingNote
        fields = ('id', 'object', 'note', 'created_by', 'created_at')


class ClientMatchingNoteWriter(ObjectSerializer):
    class Meta:
        model = ClientMatchingNote
        fields = ('note',)
