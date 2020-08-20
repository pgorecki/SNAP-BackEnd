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
    assert response.status_code == 201
    assert response.data['created_by']['id'] == user.id

    # make sure that new Eligibility Queue has been created as well
    iep = ClientIEP.objects.get(pk=response.data['id'])
    assert iep
    assert iep.eligibility_request.client == iep.client
    assert iep.eligibility_request.status is None


def test_creating_2_ieps_will_result_in_single_eligibility_request():
    agency = AgencyWithEligibilityFactory(users=1, clients=1, num_eligibility=1)
    user = agency.user_profiles.first().user

    url = '/iep/'
    api_client = APIClient()
    api_client.force_authenticate(user)

    response1 = api_client.post(url, {
        'client': Client.objects.first().id,
        'start_date': '2020-01-01',
        'end_date': '2020-01-03',
    }, format='json')
    response2 = api_client.post(url, {
        'client': Client.objects.first().id,
        'start_date': '2020-01-01',
        'end_date': '2020-01-03',
    }, format='json')

    iep1 = ClientIEP.objects.get(pk=response1.data['id'])
    iep2 = ClientIEP.objects.get(pk=response2.data['id'])
    assert iep1.eligibility_request == iep2.eligibility_request


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
    assert response.status_code == 200


def test_list_iep_by_type__new():
    agency = AgencyWithEligibilityFactory(users=1, clients=1, num_eligibility=1)
    user = agency.user_profiles.first().user
    client = Client.objects.first()

    api_client = APIClient()
    api_client.force_authenticate(user)

    # lets create new IEP
    api_client.post('/iep/', {'client': Client.objects.first().id}, format='json')

    response = api_client.get('/iep/?type=new')
    assert response.data == 123

    iep = ClientIEPFactory(client=client)

    url = f'/iep/{iep.id}/'
    api_client = APIClient()
    api_client.force_authenticate(user)

    response = api_client.patch(url, {
        'status': 'in_progress',
    }, format='json')
    print(response.data)
    assert response.status_code == 200
