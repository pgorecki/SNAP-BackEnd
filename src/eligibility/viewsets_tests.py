from rest_framework.test import APIClient
from client.models import Client
from .factories import AgencyWithEligibilityFactory, EligibilityQueueFactory
from .models import Eligibility, ClientEligibility


def test_retrieve_eligibility():
    # create test agency
    agency1 = AgencyWithEligibilityFactory(users=1, num_eligibility=3)
    # create another agency
    AgencyWithEligibilityFactory(users=1, num_eligibility=2)

    user = agency1.user_profiles.first().user
    url = '/eligibility/'
    api_client = APIClient()
    api_client.force_authenticate(user)

    response = api_client.get(url)

    assert Eligibility.objects.count() == 5
    assert response.status_code == 200
    assert len(response.data['results']) == 3


def test_agency_user_cannot_create_eligibility():
    agency = AgencyWithEligibilityFactory(users=1, num_eligibility=1)

    user = agency.user_profiles.first().user
    url = '/eligibility/'
    api_client = APIClient()
    api_client.force_authenticate(user)

    response = api_client.post(url, {
        'name': 'new eligibility'
    })

    assert response.status_code == 403
    assert Eligibility.objects.count() == 1


def test_list_eligibility_agency_configs():
    agency = AgencyWithEligibilityFactory(users=1, num_eligibility=1)
    AgencyWithEligibilityFactory(users=1, num_eligibility=1)

    user = agency.user_profiles.first().user
    url = '/eligibility/agency_configs/'
    api_client = APIClient()
    api_client.force_authenticate(user)

    response = api_client.get(url)

    assert response.status_code == 200

    results = response.data['results']

    assert len(results) == 1
    assert results[0]['agency']['id'] == str(agency.id)
    assert results[0]['eligibility']['id'] == str(agency.agencyeligibilityconfig_set.first().eligibility.id)


def test_list_client_eligibility():
    agency = AgencyWithEligibilityFactory(users=1, num_eligibility=1)
    user = agency.user_profiles.first().user

    url = '/eligibility/clients/'
    api_client = APIClient()
    api_client.force_authenticate(user)

    response = api_client.get(url)

    assert response.status_code == 200


def test_create_client_eligibility():
    agency = AgencyWithEligibilityFactory(users=1, clients=1, num_eligibility=1)
    user = agency.user_profiles.first().user

    url = '/eligibility/clients/'
    api_client = APIClient()
    api_client.force_authenticate(user)

    response = api_client.post(url, {
        'client': Client.objects.first().id,
        'eligibility': agency.eligibility.first().id,
        'status': 'ELIGIBLE',
    }, format='json')
    print(response.data)
    assert response.status_code == 201


def test_create_client_eligibility_for_invalid_client():
    AgencyWithEligibilityFactory(users=1, clients=1, num_eligibility=1)
    agency = AgencyWithEligibilityFactory(users=1, clients=1, num_eligibility=1)
    user = agency.user_profiles.first().user

    url = '/eligibility/clients/'
    api_client = APIClient()
    api_client.force_authenticate(user)

    client = Client.objects.exclude(created_by=user).first()

    response = api_client.post(url, {
        'client': client.id,
        'eligibility': agency.eligibility.first().id,
        'status': 'ELIGIBLE',
    }, format='json')
    assert response.status_code == 400


def test_create_client_eligibility_for_invalid_eligibility():
    agency1 = AgencyWithEligibilityFactory(users=1, clients=1, num_eligibility=1)
    agency2 = AgencyWithEligibilityFactory(users=1, num_eligibility=1)
    user = agency1.user_profiles.first().user

    url = '/eligibility/clients/'
    api_client = APIClient()
    api_client.force_authenticate(user)

    client = Client.objects.exclude(created_by=agency2.user_profiles.first().user).first()

    response = api_client.post(url, {
        'eligibility': agency2.eligibility.first().id,
        'client': client.id,
        'status': 'ELIGIBLE',
    }, format='json')
    assert response.status_code == 400


def test_update_client_eligibility_runs_validation():
    agency1 = AgencyWithEligibilityFactory(users=1, clients=1, num_eligibility=1)
    agency2 = AgencyWithEligibilityFactory(users=1, num_eligibility=1)
    user = agency1.user_profiles.first().user

    client = Client.objects.first()

    client_eligibility = ClientEligibility.objects.create(
        eligibility=agency1.eligibility.first(),
        client=client,
    )

    api_client = APIClient()
    api_client.force_authenticate(user)

    url = f'/eligibility/clients/{client_eligibility.id}/'
    response = api_client.patch(url, {
        'eligibility': agency2.eligibility.first().id,
    }, format='json')
    assert response.status_code == 400


def test_add_client_to_eligibility_queue():
    agency = AgencyWithEligibilityFactory(users=1, clients=1, num_eligibility=1)
    user = agency.user_profiles.first().user

    client = Client.objects.first()

    api_client = APIClient()
    api_client.force_authenticate(user)

    response = api_client.post('/eligibility/queue/', {
        'client': client.id,
    })

    assert response.status_code == 201
    assert response.data['client']['id'] == str(client.id)
    assert response.data['requestor']['id'] == str(agency.id)
    assert response.data['status'] is None


def test_update_eligibility_queue():
    agency = AgencyWithEligibilityFactory(users=1, clients=1, num_eligibility=1)
    # TODO: make sure that user is from DFCS
    user = agency.user_profiles.first().user

    client = Client.objects.first()

    queue_item = EligibilityQueueFactory(client=client, requestor=agency)

    api_client = APIClient()
    api_client.force_authenticate(user)

    response = api_client.patch(f'/eligibility/queue/{queue_item.id}/', {
        'status': 'ELIGIBLE',
    })

    assert response.status_code == 200
    assert response.data['client']['id'] == str(client.id)
    assert response.data['requestor']['id'] == str(agency.id)
    assert response.data['status'] == 'ELIGIBLE'


def test_adding_client_twice_to_eligibility_queue_will_throw_400_error():
    agency = AgencyWithEligibilityFactory(users=1, clients=1, num_eligibility=1)
    user = agency.user_profiles.first().user

    client = Client.objects.first()
    client.eligibility_queue.create(requestor=agency)

    api_client = APIClient()
    api_client.force_authenticate(user)

    response = api_client.post('/eligibility/queue/', {
        'client': client.id,
    })

    assert response.status_code == 400


def test_resolving_eligibility_queue_will_set_resolved_by_field():
    agency1 = AgencyWithEligibilityFactory(users=1, clients=1, num_eligibility=1)
    agency2 = AgencyWithEligibilityFactory(users=1)
    user = agency2.user_profiles.first().user

    client = Client.objects.first()
    queue_item = client.eligibility_queue.create(requestor=agency1)

    api_client = APIClient()
    api_client.force_authenticate(user)

    response = api_client.patch(f'/eligibility/queue/{queue_item.id}/', {
        'status': 'NOT_ELIGIBLE',
    })

    assert response.status_code == 200
    assert response.data['resolved_by']['id'] == user.id
