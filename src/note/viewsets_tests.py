from rest_framework.test import APIClient
from agency.factories import AgencyFactory
from program.factories import EnrollmentFactory, AgencyWithProgramsFactory
from client.models import Client


def test_create_client_note():
    # create test agency
    agency1 = AgencyFactory(users=1, clients=1)
    user = agency1.user_profiles.first().user
    client = Client.objects.first()

    url = '/notes/'
    api_client = APIClient()
    api_client.force_authenticate(user)

    response = api_client.post(url, {
        'source': {'id': client.id, 'type': 'Client'},
        'text': 'a message'
    }, format='json')

    assert response.status_code == 201


def test_create_enrollment_note():
    # create test agency
    agency = AgencyWithProgramsFactory(users=1, clients=1, num_programs=1)
    user = agency.user_profiles.first().user
    client = Client.objects.first()
    enrollment = EnrollmentFactory(client=client, program=agency.programs.first())

    url = '/notes/'
    api_client = APIClient()
    api_client.force_authenticate(user)

    response = api_client.post(url, {
        'source': {'id': enrollment.id, 'type': 'Enrollment'},
        'text': 'a message'
    }, format='json')

    assert response.status_code == 201
