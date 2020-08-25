from rest_framework.test import APIClient
from agency.factories import AgencyFactory
from program.factories import EnrollmentFactory, AgencyWithProgramsFactory
from note.models import Note
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


def test_create_non_existing_enrollment_note():
    # create test agency
    agency = AgencyWithProgramsFactory(users=1, clients=1, num_programs=1)
    user = agency.user_profiles.first().user
    client = Client.objects.first()
    EnrollmentFactory(client=client, program=agency.programs.first())

    url = '/notes/'
    api_client = APIClient()
    api_client.force_authenticate(user)

    response = api_client.post(url, {
        # we are deliberately using client id instead of enrollment id
        'source': {'id': client.id, 'type': 'Enrollment'},
        'text': 'a message'
    }, format='json')

    assert response.status_code == 400


def test_list_notes_by_type():
    # create test agency
    agency = AgencyWithProgramsFactory(users=1, clients=1, num_programs=1)
    user = agency.user_profiles.first().user
    client = Client.objects.first()
    enrollment = EnrollmentFactory(client=client, program=agency.programs.first())
    Note.objects.create(source=client, text='client note')
    Note.objects.create(source=enrollment, text='enrollment note')

    api_client = APIClient()
    api_client.force_authenticate(user)

    response = api_client.get('/notes/')
    assert response.status_code == 200
    assert len(response.data['results']) == 2

    response = api_client.get(f'/notes/?source_id={client.id}')
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['source']['id'] == str(client.id)
    assert response.data['results'][0]['source']['object'] == 'Client'

    response = api_client.get(f'/notes/?source_id={enrollment.id}')
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['source']['id'] == str(enrollment.id)
    assert response.data['results'][0]['source']['object'] == 'Enrollment'


def test_update_note_field():
    # create test agency
    agency = AgencyWithProgramsFactory(users=1, clients=1, num_programs=1)
    user = agency.user_profiles.first().user
    client = Client.objects.first()
    note = Note.objects.create(source=client, text='client note')

    api_client = APIClient()
    api_client.force_authenticate(user)

    response = api_client.patch(f'/notes/{note.id}/', {'text': 'updated text'}, format='json')
    assert response.status_code == 200
    assert response.data['text'] == 'updated text'
