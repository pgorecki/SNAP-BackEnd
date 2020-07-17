from rest_framework import serializers
from core.serializers import ContentObjectRelatedField, ObjectSerializer, CreatedByReader
from .models import Survey, Question, Response, Answer
from .validators import SurveySerializerValidator


class QuestionReader(ObjectSerializer):
    created_by = CreatedByReader(read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'object', 'title', 'description', 'category', 'options', 'other', 'refusable', 'is_public',
                  'created_by', 'usage_count', 'created_at', 'modified_at')


class QuestionWriter(ObjectSerializer):
    class Meta:
        model = Question
        fields = ('title', 'description', 'category', 'options', 'other', 'refusable', 'is_public')


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
    created_by = CreatedByReader(read_only=True)
    respondent = ContentObjectRelatedField(read_only=True)
    survey = SurveyReader(read_only=True)
    answers = AnswerReader(many=True)

    class Meta:
        model = Response
        fields = ('id', 'object', 'survey', 'respondent', 'answers', 'created_by', 'created_at', 'modified_at')


class ResponseWriter(ObjectSerializer):
    class RespondentWriter(ContentObjectRelatedField):
        def get_queryset(self):
            # TODO: .....
            print(('get_qs'))
            return None

    answers = AnswerWriter(many=True)
    respondent = RespondentWriter()

    class Meta:
        model = Response
        fields = ('survey', 'respondent', 'answers')

    def create(self, validated_data):
        # TODO: check access permissions to survey, questions, respondent
        # TODO: add transaction
        response = Response.objects.create(
            survey=validated_data['survey'],
            respondent=validated_data['respondent'],
            created_by=validated_data['created_by'],
        )
        for ans in validated_data['answers']:
            Answer.objects.create(response=response, **ans)

        return response

    def update(self, instance, validated_data):
        instance.answers.all().delete()
        for ans in validated_data['answers']:
            instance.answers.create(**ans)
        return instance
