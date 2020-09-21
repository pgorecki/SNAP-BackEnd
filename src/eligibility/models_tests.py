from django.db import transaction
import django.db.utils
from client.models import Client
from .factories import AgencyWithEligibilityFactory
from .models import ClientEligibility, EligibilityQueue
from .enums import EligibilityStatus


def test_eligibility_request_is_unresolved_with_status_is_none():
    agency = AgencyWithEligibilityFactory(users=1, clients=1, num_eligibility=1)
    client = Client.objects.first()

    request = EligibilityQueue(client=client, requestor=agency)

    assert request.is_resolved is False


def test_can_have_multiple_resolved_requests_for_same_client():
    agency = AgencyWithEligibilityFactory(users=1, clients=1, num_eligibility=1)
    client = Client.objects.first()

    EligibilityQueue.objects.create(
        client=client, requestor=agency, status=EligibilityStatus.ELIGIBLE
    )
    EligibilityQueue.objects.create(
        client=client, requestor=agency, status=EligibilityStatus.ELIGIBLE
    )
    assert EligibilityQueue.objects.count() == 2


def test_adding_second_unresolved_eq_will_fail_for_same_client():
    agency = AgencyWithEligibilityFactory(users=1, clients=1, num_eligibility=1)
    client = Client.objects.first()

    EligibilityQueue.objects.create(client=client, requestor=agency, status=None)
    try:
        with transaction.atomic():
            EligibilityQueue.objects.create(
                client=client, requestor=agency, status=None
            )
        # adding another EQ should not be possible, because there is one with status=None
        assert False
    except django.db.utils.IntegrityError:
        pass
    assert EligibilityQueue.objects.count() == 1


def test_changing_newest_eq_will_update_client_eligibility():
    agency = AgencyWithEligibilityFactory(users=1, clients=1, num_eligibility=1)
    client = Client.objects.first()
    user = agency.user_profiles.first().user

    assert ClientEligibility.is_eligible(client=client) is False

    eq = EligibilityQueue.objects.create(client=client, requestor=agency, status=None)
    eq.status = EligibilityStatus.ELIGIBLE.name
    eq.resolved_by = user
    eq.save()

    assert ClientEligibility.objects.count() == 1
    assert ClientEligibility.is_eligible(client=client)
    assert client.eligibility.first().created_by == user
