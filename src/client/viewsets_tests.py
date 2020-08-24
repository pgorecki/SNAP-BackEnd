from rest_framework.test import APIClient
from __tests__.factories import setup_2_agencies
from client.models import Client
from agency.factories import AgencyFactory

# e2e tests


def test_get_clients_by_anonymous():
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()

    url = '/clients/'
    api_client = APIClient()

    # self.client.credentials(
    #     HTTP_X_HMIS_TRUSTEDAPP_ID='appid',
    #     HTTP_AUTHORIZATION='HMISUserAuth session_token=abcd',
    # )
    # client.login(username='user1', password='pass')

    response = api_client.get(url)
    assert response.status_code == 401


def test_get_client_public_list_data_by_logged_in_user():
    # create test agency
    AgencyFactory(users=1, clients=1)
    agency2 = AgencyFactory(users=1, clients=0)
    user2 = agency2.user_profiles.first().user

    api_client = APIClient()
    api_client.force_authenticate(user2)

    response = api_client.get('/clients/')
    assert response.status_code == 200
    assert len(response.data['results']) == 1
    client = response.data['results'][0]
    assert client['dob'] is None
    assert client['ssn'] is None
    assert client['address'] is None


def test_get_client_public_single_data_by_logged_in_user():
    # create test agency
    AgencyFactory(users=1, clients=1)
    agency2 = AgencyFactory(users=1, clients=0)
    user2 = agency2.user_profiles.first().user

    api_client = APIClient()
    api_client.force_authenticate(user2)

    client = Client.objects.first()
    response = api_client.get(f'/clients/{client.id}/')
    assert response.status_code == 200
    client = response.data
    assert client['dob'] is None
    assert client['ssn'] is None
    assert client['address'] is None


def test_get_client_private_data_due_via_agency_owner_rights(client):
    agency1 = AgencyFactory(users=1, clients=1)
    user1 = agency1.user_profiles.first().user

    url = '/clients/'
    api_client = APIClient()
    api_client.force_authenticate(user1)

    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data['results']) == 1
    client = response.data['results'][0]
    assert client['object'] == 'Client'
    assert client['created_by']['id'] == user1.id
    assert client['dob'] is not None


def test_create_client_by_user1():
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()
    url = '/clients/'
    api_client = APIClient()
    api_client.force_authenticate(user1)
    response = api_client.post(url, {
        'first_name': 'John',
        'last_name': 'Doe',
        'dob': '2000-01-01',
        'address': {
            'city': 'Boston'
        }
    }, format='json')
    assert response.status_code == 201
    assert response.data['first_name'] == 'John'
    assert response.data['created_by']['id'] == user1.id
    assert response.data['address']['city'] == 'Boston'


def test_update_own_client_by_user1():
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()
    client = Client.objects.create(first_name='John', last_name='Doe', dob='2000-01-01', created_by=user1)

    api_client = APIClient()
    api_client.force_authenticate(user1)
    response = api_client.put(f'/clients/{client.id}/', {
        'first_name': 'Jane',
        'last_name': 'Doe',
        'dob': '2000-01-01'
    }, format='json')
    assert response.status_code == 200
    assert response.data['first_name'] == 'Jane'
