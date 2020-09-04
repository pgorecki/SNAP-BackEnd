from .helpers import setup_agency_data, agency_clients, agency_users, assertScenario
from eligibility.enums import EligibilityStatus
from eligibility.models import Eligibility, ClientEligibility
"""
Eligiblity endpoints

/eligibility/clients/

"""


def test_foo():
    agency1, agency2 = setup_agency_data()
    client1, client2 = agency_clients(agency1)
    user1, user2 = agency_users(agency1)
    user3, user4 = agency_users(agency2)

    eli1 = client1.eligibility.create(
        status=EligibilityStatus.ELIGIBLE.name,
        eligibility=Eligibility.objects.first(),
        created_by=user1,
    )

    eli2 = client1.eligibility.create(
        status=EligibilityStatus.ELIGIBLE.name,
        eligibility=Eligibility.objects.first(),
        created_by=user2,
    )

    assertScenario((
        ('view', ClientEligibility,                 eli1, eli2),
        (user1, None,                               True, False),
        (user1, 'view_clienteligibility',           True, False),
        (user1, 'view_clienteligibility_agency',    True, True),
    ))
