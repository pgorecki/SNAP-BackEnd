from rest_framework.test import APIClient
from agency.factories import AgencyFactory


def test_users_me():
    agency = AgencyFactory(users=1)
    # TODO: make sure that user is from DFCS
    user = agency.user_profiles.first().user

    api_client = APIClient()
    api_client.force_authenticate(user)

    response = api_client.get('/users/me/')
    assert response.status_code == 200
