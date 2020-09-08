from .helpers import setup_agency_data, agency_clients, agency_users, assertScenario
from .test_helpers import create_view
from core.permissions import AbilityPermission
from eligibility.enums import EligibilityStatus
from eligibility.models import Eligibility, ClientEligibility
from eligibility.viewsets import ClientEligibilityViewset, EligibilityQueueViewset
from django.contrib.auth.models import Permission
"""
Eligiblity endpoints

/eligibility/clients/

"""


def test_client_eligibility_is_protected():
    agency1, agency2 = setup_agency_data()
    user1, user2 = agency_users(agency1)

    user = agency1.user_profiles.first().user
    view = create_view(ClientEligibilityViewset, 'view', user)
    assert AbilityPermission in view.permission_classes


def test_client_eligibility_access():
    agency1, agency2 = setup_agency_data()
    client1, client2 = agency_clients(agency1)
    user1, user2 = agency_users(agency1)
    user3, user4 = agency_users(agency2)

    eli1 = client1.eligibility.create(
        status=EligibilityStatus.ELIGIBLE.name,
        eligibility=Eligibility.objects.first(),
        created_by=user1,
    )

    eli2 = client2.eligibility.create(
        status=EligibilityStatus.ELIGIBLE.name,
        eligibility=Eligibility.objects.first(),
        created_by=user2,
    )

    assertScenario('view', ClientEligibility, (
        (None,  eli1,  eli2),
        (user1, False, False, 'view_clienteligibility'),
        (user1, True,  False, ['view_clienteligibility', 'view_client']),
    ))


def test_eligibility_queue_is_protected():
    agency1, agency2 = setup_agency_data()
    user1, user2 = agency_users(agency1)

    user = agency1.user_profiles.first().user
    view = create_view(EligibilityQueueViewset, 'view', user)
    assert AbilityPermission in view.permission_classes
