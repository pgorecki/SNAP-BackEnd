from collections import deque
from agency.factories import AgencyFactory
from eligibility.factories import AgencyWithEligibilityFactory
from django.contrib.auth.models import Permission
from __tests__.permissions.test_helpers import create_fake_request


def agency_clients(agency):
    return [ac.client for ac in agency.agency_clients.all()]


def agency_users(agency):
    return [p.user for p in agency.user_profiles.all()]


def setup_agency_data():
    """
    We have 2 agencies here
    Agency1 has 2 clients: first one created by user1, second one created by user2

    Agency2 has 2 clients: first one created by user1, second one created by user2
    """
    agency1 = AgencyWithEligibilityFactory(name="Agency1", users=2, clients=2, num_eligibility=1)

    user1, user2 = [p.user for p in agency1.user_profiles.all()]
    client1, client2 = [ac.client for ac in agency1.agency_clients.all()]

    agency2 = AgencyFactory(name="Agency2", users=2, clients=2)

    user3, user4 = [p.user for p in agency2.user_profiles.all()]
    client3, client4 = [ac.client for ac in agency2.agency_clients.all()]

    return agency1, agency2


def setup_agency_data_for_survey_permissions():
    agency1, agency2 = setup_agency_data()
    return agency1, agency2


def assertScenario(scenario):
    scenario = deque(scenario)
    header = deque(scenario.popleft())
    action = header.popleft()
    model = header.popleft()
    objects_to_check = header

    print(action, model)

    for row in scenario:
        row = deque(row)
        user = row.popleft()
        permission = row.popleft()
        expected_results = row

        assert user.user_permissions.count() == 0
        if permission:
            try:
                perm = Permission.objects.get(codename=permission)
                user.user_permissions.add(perm)
            except:
                assert False, f"permission {permission} not found"

        request = create_fake_request(user)
        for obj, true_access in zip(objects_to_check, expected_results):
            user_access = request.ability.can(action, obj)

            to_text = {
                True: 'can',
                False: "can't"
            }

            assert user_access == true_access, f"{user} {to_text[user_access]} access {obj}, expected {to_text[true_access]}"
