from rest_framework.test import APIClient
from survey.factories import SurveyFactory
from .factories import AgencyWithProgramsFactory
from .models import Program


def test_retrieve_programs():
    # create test agency
    agency1 = AgencyWithProgramsFactory(users=1, num_programs=3)
    # create another agency
    AgencyWithProgramsFactory(users=1, num_programs=2)

    user = agency1.user_profiles.first().user
    url = "/programs/"
    api_client = APIClient()
    api_client.force_authenticate(user)

    response = api_client.get(url)

    assert Program.objects.count() == 5
    assert response.status_code == 200
    assert len(response.data["results"]) == 3


def test_agency_user_cannot_create_program():
    agency = AgencyWithProgramsFactory(users=1, num_programs=1)

    user = agency.user_profiles.first().user
    url = "/programs/"
    api_client = APIClient()
    api_client.force_authenticate(user)

    response = api_client.post(url, {"name": "new program"})

    assert response.status_code == 403
    assert Program.objects.count() == 1


def test_list_program_surveys():
    agency = AgencyWithProgramsFactory(users=1, num_programs=1)
    AgencyWithProgramsFactory(users=1, num_programs=1)
    user = agency.user_profiles.first().user

    entry_survey = SurveyFactory(name="entry", created_by=user)
    update_survey = SurveyFactory(name="update", created_by=user)
    exit_survey = SurveyFactory(name="exit", created_by=user)

    program = agency.programs.first()
    program.enrollment_entry_survey = entry_survey
    program.enrollment_update_survey = update_survey
    program.enrollment_exit_survey = exit_survey
    program.save()

    url = "/programs/"
    api_client = APIClient()
    api_client.force_authenticate(user)

    response = api_client.get(url)

    assert response.status_code == 200

    result = response.data["results"][0]

    assert result["enrollment_entry_survey"]["name"] == "entry"
    assert result["enrollment_update_survey"]["name"] == "update"
    assert result["enrollment_exit_survey"]["name"] == "exit"
