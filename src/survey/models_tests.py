from django.contrib.auth.models import AnonymousUser
from __tests__.factories import setup_2_agencies
from .models import Survey


# manager / query tests


def test_SurveyManager_for_user_returns_surveys_from_user_agency():
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()

    survey1 = Survey.objects.create(name="survey1", definition={}, created_by=user1)
    survey2 = Survey.objects.create(name="survey1", definition={}, created_by=user2)

    assert list(Survey.objects.for_user(user1)) == [survey1]
    assert list(Survey.objects.for_user(user2)) == [survey2]


def test_SurveyManager_for_anonymous_returns_empty_list():
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()

    anonymous = AnonymousUser()

    assert list(Survey.objects.for_user(anonymous)) == []
