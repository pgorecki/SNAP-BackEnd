from rest_framework.test import APIClient
from client.models import Client
from agency.factories import AgencyFactory
from eligibility.factories import AgencyWithEligibilityFactory
from .factories import ClientIEPFactory
from .models import ClientIEP


def test_retrieve_client_iep():
    # create test agency
    agency1 = AgencyFactory(users=1, clients=1)
    user = agency1.user_profiles.first().user
    client = Client.objects.first()

    iep = ClientIEPFactory(client=client)

    url = '/iep/'
    api_client = APIClient()
    api_client.force_authenticate(user)

    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data['results']) == 1

    row = response.data['results'][0]
    assert row['client']['id'] == str(client.id)


def test_create_client_iep():
    agency = AgencyWithEligibilityFactory(users=1, clients=1, num_eligibility=1)
    user = agency.user_profiles.first().user

    url = '/iep/'
    api_client = APIClient()
    api_client.force_authenticate(user)

    response = api_client.post(url, {
        'client': Client.objects.first().id,
        'start_date': '2020-01-01',
        'end_date': '2020-01-03',
    }, format='json')
    print(response.data)
    assert response.status_code == 201
    assert response.data['created_by']['id'] == user.id


def test_update_iep_status():
    agency = AgencyWithEligibilityFactory(users=1, clients=1, num_eligibility=1)
    user = agency.user_profiles.first().user
    client = Client.objects.first()
    iep = ClientIEPFactory(client=client)

    url = f'/iep/{iep.id}/'
    api_client = APIClient()
    api_client.force_authenticate(user)

    response = api_client.patch(url, {
        'status': 'in_progress',
    }, format='json')
    print(response.data)
    assert response.status_code == 200
