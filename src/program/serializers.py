from core.serializers import ObjectSerializer, CreatedByReader
from agency.serializers import AgencyReader
from client.serializers import ClientReader
from survey.serializers import SurveyMiniReader
from .models import (
    Program,
    Enrollment,
    EnrollmentService,
    EnrollmentServiceType,
)


class ProgramReader(ObjectSerializer):
    agency = AgencyReader()
    enrollment_entry_survey = SurveyMiniReader()
    enrollment_update_survey = SurveyMiniReader()
    enrollment_exit_survey = SurveyMiniReader()

    class Meta:
        model = Program
        fields = (
            "id",
            "object",
            "name",
            "agency",
            "description",
            "created_at",
            "modified_at",
            "enrollment_entry_survey",
            "enrollment_update_survey",
            "enrollment_exit_survey",
        )


class ProgramWriter(ObjectSerializer):
    class Meta:
        model = Program
        fields = (
            "name",
            "agency",
            "description",
            "enrollment_entry_survey",
            "enrollment_update_survey",
            "enrollment_exit_survey",
        )


class EnrollmentReader(ObjectSerializer):
    client = ClientReader()
    program = ProgramReader()

    class Meta:
        model = Enrollment
        fields = (
            "id",
            "object",
            "status",
            "client",
            "program",
            "start_date",
            "projected_end_date",
            "end_date",
            "created_at",
            "modified_at",
        )


class EnrollmentWriter(ObjectSerializer):
    class Meta:
        model = Enrollment
        fields = (
            "status",
            "client",
            "program",
            "start_date",
            "projected_end_date",
            "end_date",
        )


class EnrollmentServiceReader(ObjectSerializer):
    class EnrollmentServiceEnrollmentReader(EnrollmentReader):
        client = None
        program = None

    class EnrollmentServiceEnrollmentServiceTypeReader(ObjectSerializer):
        class Meta:
            model = EnrollmentServiceType
            fields = ("id", "object", "name", "category")

    enrollment = EnrollmentServiceEnrollmentReader()
    service_type = EnrollmentServiceEnrollmentServiceTypeReader()
    created_by = CreatedByReader()

    class Meta:
        model = EnrollmentService
        fields = (
            "id",
            "object",
            "enrollment",
            "service_type",
            "effective_date",
            "values",
            "created_by",
            "created_at",
            "modified_at",
        )


class EnrollmentServiceWriter(ObjectSerializer):
    class Meta:
        model = EnrollmentService
        fields = ("id", "enrollment", "service_type", "effective_date", "values")


class EnrollmentServiceTypeReader(ObjectSerializer):
    class Meta:
        model = EnrollmentServiceType
        fields = ("id", "object", "name", "category", "agency")


class EnrollmentServiceTypeWriter(ObjectSerializer):
    class Meta:
        model = EnrollmentServiceType
        fields = ("name", "category", "agency")
