# from rest_framework.test import APIClient
# from .factories import AgencyWithProgramsFactory
# from client.models import Client
# from .models import ProgramEligibility


# def test_list_eligibility():
#     agency = AgencyWithProgramsFactory(users=1, num_programs=1)
#     user = agency.user_profiles.first().user

#     url = '/programs/eligibility/'
#     api_client = APIClient()
#     api_client.force_authenticate(user)

#     response = api_client.get(url)

#     assert response.status_code == 200


# def test_create_eligibility():
#     agency = AgencyWithProgramsFactory(users=1, clients=1, num_programs=1)
#     user = agency.user_profiles.first().user

#     url = '/programs/eligibility/'
#     api_client = APIClient()
#     api_client.force_authenticate(user)

#     response = api_client.post(url, {
#         'program': agency.programs.first().id,
#         'client': Client.objects.first().id,
#         'status': 'ELIGIBLE',
#     }, format='json')
#     assert response.status_code == 201


# def test_create_eligibility_for_invalid_client():
#     AgencyWithProgramsFactory(users=1, clients=1, num_programs=1)
#     agency = AgencyWithProgramsFactory(users=1, clients=1, num_programs=1)
#     user = agency.user_profiles.first().user

#     url = '/programs/eligibility/'
#     api_client = APIClient()
#     api_client.force_authenticate(user)

#     client = Client.objects.exclude(created_by=user).first()

#     response = api_client.post(url, {
#         'program': agency.programs.first().id,
#         'client': client.id,
#         'status': 'ELIGIBLE',
#     }, format='json')
#     assert response.status_code == 400


# def test_create_eligibility_for_invalid_program():
#     agency1 = AgencyWithProgramsFactory(users=1, clients=1, num_programs=1)
#     agency2 = AgencyWithProgramsFactory(users=1, num_programs=1)
#     user = agency1.user_profiles.first().user

#     url = '/programs/eligibility/'
#     api_client = APIClient()
#     api_client.force_authenticate(user)

#     client = Client.objects.exclude(created_by=agency2.user_profiles.first().user).first()

#     response = api_client.post(url, {
#         'program': agency2.programs.first().id,
#         'client': client.id,
#         'status': 'ELIGIBLE',
#     }, format='json')
#     assert response.status_code == 400


# def test_update_eligibility_runs_validation():
#     agency1 = AgencyWithProgramsFactory(users=1, clients=1, num_programs=1)
#     agency2 = AgencyWithProgramsFactory(users=1, num_programs=1)
#     user = agency1.user_profiles.first().user

#     client = Client.objects.first()

#     eligibility = ProgramEligibility.objects.create(
#         program=agency1.programs.first(),
#         client=client,
#     )

#     api_client = APIClient()
#     api_client.force_authenticate(user)

#     url = f'/programs/eligibility/{eligibility.id}/'
#     response = api_client.patch(url, {
#         'program': agency2.programs.first().id,
#     }, format='json')
#     assert response.status_code == 400
