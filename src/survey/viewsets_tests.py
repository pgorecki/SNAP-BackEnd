from rest_framework.test import APIClient
from __tests__.factories import setup_2_agencies
from survey.models import Survey, Question, Response, Answer

# e2e tests


def test_get_surveys_by_anonymous():
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()

    url = '/surveys/'
    api_client = APIClient()

    # self.client.credentials(
    #     HTTP_X_HMIS_TRUSTEDAPP_ID='appid',
    #     HTTP_AUTHORIZATION='HMISUserAuth session_token=abcd',
    # )
    # client.login(username='user1', password='pass')

    response = api_client.get(url)
    assert response.status_code == 401


def test_get_surveys_by_agency_user(client):
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()
    Survey.objects.create(name='survey1', definition={}, created_by=user1)

    url = '/surveys/'
    api_client = APIClient()
    api_client.force_authenticate(user1)

    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['object'] == 'Survey'
    assert response.data['results'][0]['name'] == 'survey1'
    assert response.data['results'][0]['created_by']['id'] == user1.id


def test_get_questions_by_anonymous():
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()
    url = '/questions/'
    api_client = APIClient()
    response = api_client.get(url)
    assert response.status_code == 401


def test_get_questions_by_agency_user(client):
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()
    Question.objects.create(title='question1', created_by=user1)
    url = '/questions/'
    api_client = APIClient()
    api_client.force_authenticate(user1)
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['object'] == 'Question'
    assert response.data['results'][0]['title'] == 'question1'
    assert response.data['results'][0]['created_by']['id'] == user1.id


def test_create_survey_by_user1():
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()
    url = '/surveys/'
    api_client = APIClient()
    api_client.force_authenticate(user1)
    response = api_client.post(url, {
        'name': 'Survey',
        'definition': {'items': []},
    }, format='json')
    assert response.status_code == 201
    assert response.data['name'] == 'Survey'
    assert response.data['created_by']['id'] == user1.id


def test_update_own_survey_by_user1():
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()
    survey = Survey.objects.create(name='Survey A', definition={'items': []}, created_by=user1)

    api_client = APIClient()
    api_client.force_authenticate(user1)
    response = api_client.put(f'/surveys/{survey.id}/', {
        'name': 'Survey B',
        'definition': {'items': []},
    }, format='json')
    assert response.status_code == 200
    assert response.data['name'] == 'Survey B'


def test_create_question_by_user1():
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()
    url = '/questions/'
    api_client = APIClient()
    api_client.force_authenticate(user1)
    response = api_client.post(url, {
        'title': 'Question'
    })
    assert response.status_code == 201
    assert response.data['title'] == 'Question'
    assert response.data['created_by']['id'] == user1.id


def test_update_own_question_by_user1():
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()
    question = Question.objects.create(title='Question A', created_by=user1)

    api_client = APIClient()
    api_client.force_authenticate(user1)
    response = api_client.put(f'/questions/{question.id}/', {
        'title': 'Question B'
    }, format='json')
    assert response.status_code == 200
    assert response.data['title'] == 'Question B'


def test_save_question_to_database():
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()
    url = '/questions/'
    api_client = APIClient()
    api_client.force_authenticate(user1)
    api_client.post(url, {
        'title': 'Question',
        'category': 'choice',
        'options': ['yes', 'no'],
        'other': True,
        'refusable': True,
        'is_public': True,
    })
    q = Question.objects.first()
    assert q.title == 'Question'
    assert q.category == 'choice'
    assert q.options == ['yes', 'no']
    assert q.other is True
    assert q.refusable is True
    assert q.is_public is True


def test_get_responses_by_anonymous():
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()
    url = '/responses/'
    api_client = APIClient()
    response = api_client.get(url)
    assert response.status_code == 401


def test_get_responses_by_agency_user(client):
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()
    survey1 = Survey.objects.create(name='survey1', definition={}, created_by=user1)
    question1 = Question.objects.create(title='question1', created_by=user1)
    response1 = Response.objects.create(survey=survey1, respondent=client1, created_by=user1)
    Answer.objects.create(response=response1, question=question1, value='yes')
    url = '/responses/'
    api_client = APIClient()
    api_client.force_authenticate(user1)
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['object'] == 'Response'
    assert response.data['results'][0]['respondent']['id'] == str(client1.id)
    assert response.data['results'][0]['respondent']['object'] == 'Client'
    assert response.data['results'][0]['created_by']['id'] == user1.id
