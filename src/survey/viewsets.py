from django_filters import rest_framework
from rest_framework.filters import OrderingFilter
from core.permissions import AbilityPermission
from core.exceptions import ApplicationValidationError
from core.viewsets import ModelViewSet
from core.permissions import IsAdmin, IsAgencyMember
from .models import Survey, Question, Response
from .serializers import SurveyReader, SurveyWriter, QuestionReader, QuestionWriter, ResponseReader, ResponseWriter
from .filters import ResponseFilter


class SurveyViewset(ModelViewSet):
    read_serializer_class = SurveyReader
    write_serializer_class = SurveyWriter
    permission_classes = [AbilityPermission]
    ordering_fields = ['name', 'is_public', 'created_at', 'modified_at']

    def get_queryset(self):
        return self.request.ability.queryset_for(self.action, Survey)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class QuestionViewset(ModelViewSet):
    read_serializer_class = QuestionReader
    write_serializer_class = QuestionWriter
    permission_classes = [AbilityPermission]
    ordering_fields = ['title', 'is_public', 'created_at', 'modified_at']

    def get_queryset(self):
        return self.request.ability.queryset_for(self.action, Question)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ResponseViewset(ModelViewSet):
    read_serializer_class = ResponseReader
    write_serializer_class = ResponseWriter
    permission_classes = [AbilityPermission]
    filterset_class = ResponseFilter
    ordering_fields = ['survey__name', 'created_at', 'modified_at']

    def get_queryset(self):
        return self.request.ability.queryset_for(self.action, Response)

    def perform_create(self, serializer):
        self.validate_response(serializer.validated_data)
        serializer.save(created_by=self.request.user)

    def validate_response(self, data):
        pass
        # if not can_read_survey(self.request.user, data.survey):
        #     raise ApplicationValidationError({'survey': ['Access denied']})
