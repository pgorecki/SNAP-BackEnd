from core.serializers import ContentObjectRelatedField, ObjectSerializer, CreatedByReader
from client.serializers import ClientReader
from .models import Survey, Question, Response, Answer
from .validators import SurveySerializerValidator


class QuestionReader(ObjectSerializer):
    created_by = CreatedByReader(read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'object', 'title', 'description', 'category', 'options', 'other', 'refusable', 'is_public',
                  'rows', 'columns', 'created_by', 'usage_count', 'created_at', 'modified_at')


class QuestionWriter(ObjectSerializer):
    class Meta:
        model = Question
        fields = ('title', 'description', 'category', 'options', 'other', 'refusable', 'is_public', 'rows', 'columns')


class AnswerReader(ObjectSerializer):
    class AnswerQuestionReader(ObjectSerializer):
        created_by = CreatedByReader(read_only=True)

        class Meta:
            model = Question
            fields = ('id', 'object', 'title', 'description', 'category', 'options', 'other', 'refusable', 'is_public',
                      'created_by', 'created_at', 'modified_at')

    question = AnswerQuestionReader()

    class Meta:
        model = Answer
        fields = ('question', 'value')


class AnswerWriter(ObjectSerializer):
    class Meta:
        model = Answer
        fields = ('question', 'value')


class SurveyReader(ObjectSerializer):
    created_by = CreatedByReader(read_only=True)
    questions = QuestionReader(many=True)

    class Meta:
        model = Survey
        fields = ('id', 'object', 'name', 'definition', 'questions', 'is_public',
                  'created_by', 'created_at', 'modified_at')


class SurveyMiniReader(ObjectSerializer):
    class Meta:
        model = Survey
        fields = ('id', 'object', 'name', 'is_public')


class SurveyWriter(ObjectSerializer):
    class Meta:
        model = Survey
        fields = ('name', 'definition', 'is_public')
        validators = (SurveySerializerValidator, )


class ResponseReader(ObjectSerializer):
    created_by = CreatedByReader()
    response_context = ContentObjectRelatedField(read_only=True)
    client = ClientReader()
    survey = SurveyReader()
    answers = AnswerReader(many=True)

    class Meta:
        model = Response
        fields = ('id', 'object', 'client', 'survey', 'answers',
                  'response_context', 'created_by', 'created_at', 'modified_at')


class ResponseWriter(ObjectSerializer):
    class ResponseContextWriter(ContentObjectRelatedField):
        def get_queryset(self):
            # TODO: .....
            print(('get_qs'))
            return None

    answers = AnswerWriter(many=True)
    response_context = ResponseContextWriter(required=False)

    class Meta:
        model = Response
        fields = ('client', 'survey', 'response_context', 'answers')

    def create(self, validated_data):
        # TODO: check access permissions to survey, questions, respondent
        # TODO: add transaction
        response = Response.objects.create(
            survey=validated_data['survey'],
            client=validated_data['client'],
            created_by=validated_data['created_by'],
            response_context=validated_data.get('response_context', None)
        )
        for ans in validated_data['answers']:
            Answer.objects.create(response=response, **ans)

        return response

    def update(self, instance, validated_data):
        instance.answers.all().delete()
        for ans in validated_data['answers']:
            instance.answers.create(**ans)
        return instance
