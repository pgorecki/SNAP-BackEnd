from core.serializers import ObjectSerializer
from agency.serializers import AgencyReader
from client.serializers import ClientReader
from survey.serializers import SurveyMiniReader
from .models import Program, Enrollment, ProgramEligibility


class ProgramReader(ObjectSerializer):
    agency = AgencyReader()
    enrollment_entry_survey = SurveyMiniReader()
    enrollment_update_survey = SurveyMiniReader()
    enrollment_exit_survey = SurveyMiniReader()

    class Meta:
        model = Program
        fields = ('id', 'object', 'name', 'agency', 'description', 'created_at', 'modified_at',
                  'enrollment_entry_survey', 'enrollment_update_survey', 'enrollment_exit_survey')


class ProgramWriter(ProgramReader):
    pass


class ProgramEligibilityReader(ObjectSerializer):
    client = ClientReader()
    program = ProgramReader()

    class Meta:
        model = ProgramEligibility
        fields = ('id', 'object', 'status', 'client', 'program', 'created_at', 'modified_at')


class ProgramEligibilityWriter(ObjectSerializer):
    class Meta:
        model = ProgramEligibility
        fields = ('status', 'client', 'program')


class EnrollmentReader(ObjectSerializer):
    client = ClientReader()
    program = ProgramReader()

    class Meta:
        model = Enrollment
        fields = ('id', 'object', 'status', 'client', 'program', 'start_date',
                  'projected_end_date', 'end_date', 'created_at', 'modified_at')


class EnrollmentWriter(ObjectSerializer):
    class Meta:
        model = Enrollment
        fields = ('status', 'client', 'program', 'start_date',
                  'projected_end_date', 'end_date')
