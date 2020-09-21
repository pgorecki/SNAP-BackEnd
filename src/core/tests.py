from django.contrib.auth.models import User
from agency.models import Agency, AgencyClient
from client.models import Client


def test_client_full_name_1():
    client = Client(first_name="A", middle_name="B", last_name="C")

    assert str(client) == "A B C"


def test_client_full_name_2():
    client = Client(first_name="A", last_name="C")

    assert str(client) == "A C"


def test_user_agency_associacion():
    user = User.objects.create(username="John")
    agency = Agency.objects.create(name="Georgia")

    user.profile.agency = agency
    user.save()

    assert agency.user_profiles.first().user == user
    assert list(agency.user_profiles.all()) == [user.profile]


def test_client_agency_associacion():
    agency = Agency.objects.create(name="Georgia")
    client = Client.objects.create(dob="2000-01-01")

    AgencyClient.objects.create(agency=agency, client=client)

    assert agency in [ac.agency for ac in client.agency_clients.all()]
    assert client in [ac.client for ac in agency.agency_clients.all()]
