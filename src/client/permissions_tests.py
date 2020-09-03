import pytest
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth.models import AnonymousUser, Permission
from core.permissions import AbilityPermission
from cancan.ability import Ability, AbilityValidator
from cancan.middleware import CanCanMiddleware
from agency.factories import AgencyFactory
from .viewsets import ClientViewset


class FakeRequest():
    def __init__(self):
        self.user = AnonymousUser()


def create_view(view_cls, action, user, user_permission=None):
    if user_permission:
        user.user_permissions.add(Permission.objects.get(codename=user_permission))
    request = FakeRequest()
    request.user = user
    CanCanMiddleware().process_request(request)
    view = view_cls()
    view.action = action
    view.request = request
    return view


def test_is_protected():
    agency = AgencyFactory(users=1, clients=2)

    user = agency.user_profiles.first().user
    view = create_view(ClientViewset, 'view', user)
    assert AbilityPermission in view.permission_classes


@pytest.mark.parametrize("action", ['view', 'change', 'delete'])
def test_client_user_no_permissions(action):
    agency1 = AgencyFactory(users=2, clients=2)

    user1, user2 = [p.user for p in agency1.user_profiles.all()]
    client1, client2 = [ac.client for ac in agency1.agency_clients.all()]

    view1 = create_view(ClientViewset, 'view', user1)

    assert view1.get_queryset().count() == 0


@pytest.mark.parametrize("action,permission",
                         [("view", "view_client"), ("change", "change_client"),
                          ("delete", "delete_client"),
                          ("delete", "delete_client_agency")])
def test_client_user_as_owner(action, permission):
    agency1 = AgencyFactory(users=2, clients=2)

    user1, user2 = [p.user for p in agency1.user_profiles.all()]
    client1, client2 = [ac.client for ac in agency1.agency_clients.all()]

    view1 = create_view(ClientViewset, action, user1, permission)
    view2 = create_view(ClientViewset, action, user2, permission)

    # both members of agency 1 should se same clients
    assert view1.get_queryset().count() == 1
    assert client1 in view1.get_queryset()

    assert view2.get_queryset().count() == 1
    assert client2 in view2.get_queryset()


@pytest.mark.parametrize("action,permission",
                         [("view", "view_client_agency"), ("change", "change_client_agency"), ])
def test_client_user_as_agency_member(action, permission):
    agency1 = AgencyFactory(users=2, clients=2)
    agency2 = AgencyFactory(users=1)

    user1, user2 = [p.user for p in agency1.user_profiles.all()]
    client1, client2 = [ac.client for ac in agency1.agency_clients.all()]

    userA, = [p.user for p in agency2.user_profiles.all()]

    view1 = create_view(ClientViewset, action, user1, permission)
    view2 = create_view(ClientViewset, action, user2, permission)

    viewA = create_view(ClientViewset, action, userA, permission)

    # both members of agency 1 should se same clients
    assert view1.get_queryset().count() == 2
    assert client1 in view1.get_queryset()
    assert client2 in view1.get_queryset()

    assert view2.get_queryset().count() == 2
    assert client1 in view2.get_queryset()
    assert client2 in view2.get_queryset()

    # someone from other agency will not see clients
    assert viewA.get_queryset().count() == 0
