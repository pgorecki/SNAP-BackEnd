from django.contrib.auth.models import AnonymousUser
from __tests__.factories import setup_2_agencies
from .models import Client


# manager / query tests

# def test_ClientManager_for_user_returns_clients_from_user_agency():
#     agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()

#     assert list(Client.objects.for_user(user1)) == [client1, client2]
#     assert list(Client.objects.for_user(user2)) == [client2, client2]


def test_ClientManager_for_anonymous_returns_empty_list():
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()

    anonymous = AnonymousUser()

    assert anonymous.is_anonymous is True
    assert list(Client.objects.for_user(anonymous)) == []
