from rest_framework.test import APIClient
from django.contrib.auth.models import Permission
from client.models import Client
from agency.factories import AgencyFactory
from program.factories import EnrollmentFactory
from eligibility.factories import AgencyWithEligibilityFactory
from .choices import IEPStatus
from .factories import ClientIEPFactory
from .models import ClientIEP, JobPlacement


def test_retrieve_client_iep():
    # create test agency
    agency1 = AgencyFactory(users=1, clients=1)
    user = agency1.user_profiles.first().user
    user.user_permissions.add(Permission.objects.get(codename='view_clientiep'))
    user.user_permissions.add(Permission.objects.get(codename='view_client'))
    client = Client.objects.first()

    ClientIEPFactory(client=client)

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
    user.user_permissions.add(Permission.objects.get(codename='add_clientiep'))

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
    user.user_permissions.add(Permission.objects.get(codename='add_clientiep'))

    url = '/iep/'
    api_client = APIClient()
    api_client.force_authenticate(user)

    response1 = api_client.post(url, {
        'client': Client.objects.first().id,
        'start_date': '2020-01-01',
        'end_date': '2020-01-03',
    }, format='json')
    assert response1.status_code == 201
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
    user.user_permissions.add(Permission.objects.get(codename='change_clientiep'))
    user.user_permissions.add(Permission.objects.get(codename='view_client'))

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
    user.user_permissions.add(Permission.objects.get(codename='view_clientiep'))
    user.user_permissions.add(Permission.objects.get(codename='view_client'))

    api_client = APIClient()
    api_client.force_authenticate(user)

    ClientIEPFactory(client=Client.objects.first(), status=IEPStatus.IN_ORIENTATION)

    assert api_client.get('/iep/?type=new').data['count'] == 1
    assert api_client.get('/iep/?type=existing').data['count'] == 0
    assert api_client.get('/iep/?type=historical').data['count'] == 0


def test_list_iep_by_type__existing():
    agency = AgencyWithEligibilityFactory(users=1, clients=1, num_eligibility=1)
    user = agency.user_profiles.first().user
    user.user_permissions.add(Permission.objects.get(codename='view_clientiep'))
    user.user_permissions.add(Permission.objects.get(codename='view_client'))

    client = Client.objects.first()

    api_client = APIClient()
    api_client.force_authenticate(user)

    # lets create IEP which is in progress
    ClientIEPFactory(client=client, status=IEPStatus.IN_PROGRESS)

    # and another one which is new
    ClientIEPFactory(client=client, status=IEPStatus.IN_ORIENTATION)

    assert api_client.get('/iep/?type=new').data['count'] == 0
    print(api_client.get('/iep/?type=existing').data)
    assert api_client.get('/iep/?type=existing').data['count'] == 2
    assert api_client.get('/iep/?type=historical').data['count'] == 0


def test_list_iep_by_type__historical():
    agency = AgencyWithEligibilityFactory(users=1, clients=1, num_eligibility=1)
    user = agency.user_profiles.first().user
    user.user_permissions.add(Permission.objects.get(codename='view_clientiep'))
    user.user_permissions.add(Permission.objects.get(codename='view_client'))

    client = Client.objects.first()

    api_client = APIClient()
    api_client.force_authenticate(user)

    # lets create IEP which is in progress
    ClientIEPFactory(client=client, status=IEPStatus.ENDED)

    assert api_client.get('/iep/?type=new').data['count'] == 0
    assert api_client.get('/iep/?type=existing').data['count'] == 0
    assert api_client.get('/iep/?type=historical').data['count'] == 1


def test_create_iep_enrollment():
    agency = AgencyWithEligibilityFactory(users=1, clients=1, num_eligibility=1)
    program = agency.programs.create()
    user = agency.user_profiles.first().user
    user.user_permissions.add(Permission.objects.get(codename='change_clientiep'))
    user.user_permissions.add(Permission.objects.get(codename='view_client'))

    client = Client.objects.first()
    iep = ClientIEPFactory(client=client)

    url = f'/iep/{iep.id}/'
    api_client = APIClient()
    api_client.force_authenticate(user)

    response = api_client.patch(url, {
        'enrollments': [
            {
                'program': program.id,
                'status': 'PLANNED',
            },
        ],
    }, format='json')
    import json
    assert response.status_code == 200
    assert response.data['enrollments'][0]['id'] == str(iep.iep_enrollments.first().enrollment.id)

    assert iep.iep_enrollments.count() == 1


def test_update_iep_enrollment():
    agency = AgencyWithEligibilityFactory(users=1, clients=1, num_eligibility=1)
    program = agency.programs.create()
    user = agency.user_profiles.first().user
    user.user_permissions.add(Permission.objects.get(codename='change_clientiep'))
    user.user_permissions.add(Permission.objects.get(codename='view_client'))

    client = Client.objects.first()
    iep = ClientIEPFactory(client=client)
    enrollment = EnrollmentFactory(client=client, program=program)
    iep.iep_enrollments.create(enrollment=enrollment)

    url = f'/iep/{iep.id}/'
    api_client = APIClient()
    api_client.force_authenticate(user)

    response = api_client.patch(url, {
        'enrollments': [
            {
                'id': enrollment.id,
                'program': program.id,
                'status': 'PLANNED',
            },
        ],
    }, format='json')
    print('response data', response.data)
    assert response.status_code == 200

    assert iep.iep_enrollments.count() == 1

    updated_enrollment = iep.iep_enrollments.first().enrollment
    assert updated_enrollment.id == enrollment.id
    assert updated_enrollment.program.id == program.id
    assert updated_enrollment.status == 'PLANNED'


def test_delete_iep_enrollment():
    agency = AgencyWithEligibilityFactory(users=1, clients=1, num_eligibility=1)
    program = agency.programs.create()
    user = agency.user_profiles.first().user
    user.user_permissions.add(Permission.objects.get(codename='change_clientiep'))
    user.user_permissions.add(Permission.objects.get(codename='view_client'))

    client = Client.objects.first()
    iep = ClientIEPFactory(client=client)
    enrollment = EnrollmentFactory(client=client, program=program)
    iep.iep_enrollments.create(enrollment=enrollment)

    url = f'/iep/{iep.id}/'
    api_client = APIClient()
    api_client.force_authenticate(user)

    assert iep.iep_enrollments.count() == 1

    response = api_client.patch(url, {
        'enrollments': [],
    }, format='json')
    print('response data', response.data)
    assert response.status_code == 200

    assert iep.iep_enrollments.count() == 0


def test_cannot_remove_iep_enrollment_if_started():
    agency = AgencyWithEligibilityFactory(users=1, clients=1, num_eligibility=1)
    program = agency.programs.create()
    user = agency.user_profiles.first().user
    user.user_permissions.add(Permission.objects.get(codename='change_clientiep'))
    user.user_permissions.add(Permission.objects.get(codename='view_client'))

    client = Client.objects.first()
    iep = ClientIEPFactory(client=client)
    enrollment = EnrollmentFactory(client=client, program=program, status='ENROLLED')
    iep.iep_enrollments.create(enrollment=enrollment)

    url = f'/iep/{iep.id}/'
    api_client = APIClient()
    api_client.force_authenticate(user)

    assert iep.iep_enrollments.count() == 1

    response = api_client.patch(url, {
        'enrollments': [],
    }, format='json')
    assert response.status_code == 400


def test_replace_iep_enrollment_with_new_enrollment():
    agency = AgencyWithEligibilityFactory(users=1, clients=1, num_eligibility=1)
    program = agency.programs.create()
    user = agency.user_profiles.first().user
    user.user_permissions.add(Permission.objects.get(codename='change_clientiep'))
    user.user_permissions.add(Permission.objects.get(codename='view_client'))

    client = Client.objects.first()
    iep = ClientIEPFactory(client=client)
    enrollment = EnrollmentFactory(client=client, program=program, status='PLANNED')
    iep.iep_enrollments.create(enrollment=enrollment)

    url = f'/iep/{iep.id}/'
    api_client = APIClient()
    api_client.force_authenticate(user)

    response = api_client.patch(url, {
        'enrollments': [
            {
                'program': program.id,
                'status': 'ENROLLED',
            },
        ],
    }, format='json')
    assert response.status_code == 200

    assert iep.iep_enrollments.count() == 1

    from iep.models import ClientIEPEnrollment
    from program.models import Enrollment
    assert ClientIEPEnrollment.objects.count() == 1
    # TODO: is it the right case?
    assert Enrollment.objects.count() == 2


def test_add_another_enrollment_to_iep():
    agency = AgencyWithEligibilityFactory(users=1, clients=1, num_eligibility=1)
    program1 = agency.programs.create()
    program2 = agency.programs.create()
    user = agency.user_profiles.first().user
    user.user_permissions.add(Permission.objects.get(codename='view_clientiep'))
    user.user_permissions.add(Permission.objects.get(codename='change_clientiep'))
    user.user_permissions.add(Permission.objects.get(codename='view_client'))

    client = Client.objects.first()
    iep = ClientIEPFactory(client=client)
    enrollment = EnrollmentFactory(client=client, program=program1, status='PLANNED')
    first_iep_enrollment = iep.iep_enrollments.create(enrollment=enrollment)

    url = f'/iep/{iep.id}/'
    api_client = APIClient()
    api_client.force_authenticate(user)

    response = api_client.get(url)
    existing_enrollments = response.data['enrollments']

    response = api_client.patch(url, {
        'enrollments': existing_enrollments + [
            {
                'program': program2.id,
                'status': 'ENROLLED',
            },
        ],
    }, format='json')
    assert response.status_code == 200

    assert iep.iep_enrollments.count() == 2
    assert iep.iep_enrollments.first() == first_iep_enrollment


def test_replace_iep_enrollment_with_existing_enrollment():
    agency = AgencyWithEligibilityFactory(users=1, clients=1, num_eligibility=1)
    program = agency.programs.create()
    user = agency.user_profiles.first().user
    user.user_permissions.add(Permission.objects.get(codename='change_clientiep'))
    user.user_permissions.add(Permission.objects.get(codename='view_client'))

    client = Client.objects.first()
    iep = ClientIEPFactory(client=client)
    old_enrollment = EnrollmentFactory(client=client, program=program, status='PLANNED')
    new_enrollment = EnrollmentFactory(client=client, program=program, status='PLANNED')
    iep.iep_enrollments.create(enrollment=old_enrollment)

    url = f'/iep/{iep.id}/'
    api_client = APIClient()
    api_client.force_authenticate(user)

    response = api_client.patch(url, {
        'enrollments': [
            {
                'id': str(new_enrollment.id),
                'program': program.id,
                'status': 'ENROLLED',
            },
        ],
    }, format='json')
    assert response.status_code == 400
    # assert iep.iep_enrollments.count() == 1
    # assert response.data['enrollments'][0]['id'] == str(new_enrollment.id)


def test_update_iep_job_placement():
    agency = AgencyWithEligibilityFactory(users=1, clients=1, num_eligibility=1)
    user = agency.user_profiles.first().user
    user.user_permissions.add(Permission.objects.get(codename='change_clientiep'))
    user.user_permissions.add(Permission.objects.get(codename='view_client'))

    client = Client.objects.first()
    iep = ClientIEPFactory(client=client)

    url = f'/iep/{iep.id}/'
    api_client = APIClient()
    api_client.force_authenticate(user)

    response = api_client.patch(url, {
        'job_placement': {
            'effective_date': '2020-01-01',
            'Company': 'foobar',
        },
    }, format='json')
    assert response.status_code == 200
    iep.refresh_from_db()
    assert iep.job_placement.Company == 'foobar'
