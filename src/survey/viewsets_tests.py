from django.contrib.auth.models import Permission
from rest_framework.test import APIClient
from __tests__.factories import setup_2_agencies
from survey.models import Survey, Question, Response, Answer
from client.models import Client

# e2e tests


def test_get_surveys_by_anonymous():
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()

    url = "/surveys/"
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
    Survey.objects.create(name="survey1", definition={}, created_by=user1)

    url = "/surveys/"
    api_client = APIClient()
    api_client.force_authenticate(user1)

    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["object"] == "Survey"
    assert response.data["results"][0]["name"] == "survey1"
    assert response.data["results"][0]["created_by"]["id"] == user1.id


def test_get_questions_by_anonymous():
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()
    url = "/questions/"
    api_client = APIClient()
    response = api_client.get(url)
    assert response.status_code == 401


def test_get_questions_by_agency_user(client):
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()
    Question.objects.create(title="question1", created_by=user1)
    url = "/questions/"
    api_client = APIClient()
    api_client.force_authenticate(user1)
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["object"] == "Question"
    assert response.data["results"][0]["title"] == "question1"
    assert response.data["results"][0]["created_by"]["id"] == user1.id


def test_create_survey_by_user1():
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()
    user1.user_permissions.add(Permission.objects.get(codename="add_survey"))
    url = "/surveys/"
    api_client = APIClient()
    api_client.force_authenticate(user1)
    response = api_client.post(
        url,
        {
            "name": "Survey",
            "definition": {"items": []},
        },
        format="json",
    )
    assert response.status_code == 201
    assert response.data["name"] == "Survey"
    assert response.data["created_by"]["id"] == user1.id


def test_create_survey_issue_1891238373():
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()
    user1.user_permissions.add(Permission.objects.get(codename="add_survey"))
    url = "/surveys/"
    api_client = APIClient()
    api_client.force_authenticate(user1)
    q1 = Question.objects.create()
    response = api_client.post(
        url,
        {
            "definition": {
                "items": [
                    {
                        "id": "question1",
                        "questionId": str(q1.id),
                        "title": "Questions 1",
                        "type": "question",
                    },
                    # {
                    #     "id": "question2",
                    #     "questionId": "71fe2baa-6033-488c-8f8a-c510a164e1f7"
                    # },
                    # {
                    #     "id": "question3",
                    #     "questionId": "eb3c5cba-348e-4440-a75e-bc4bc7437a5c"
                    # },
                    # {
                    #     "id": "question4",
                    #     "questionId": "77c52f87-301b-4fc7-aa0e-6d3b5941cd40"
                    # }
                ]
            },
            "name": "Orientation & Assessment",
        },
        format="json",
    )
    assert response.status_code == 201
    survey = Survey.objects.first()
    assert survey.questions.count() == 1
    assert survey.questions.first() == q1


def test_create_survey_with_invalid_definition_by_user1():
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()
    user1.user_permissions.add(Permission.objects.get(codename="add_survey"))
    url = "/surveys/"
    api_client = APIClient()
    api_client.force_authenticate(user1)
    response = api_client.post(
        url,
        {
            "name": "Survey",
            "definition": {
                "items": [
                    {
                        "type": "question",
                        "title": "question without id",
                    }
                ]
            },
        },
        format="json",
    )
    assert response.status_code == 400


def test_update_own_survey_by_user1():
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()
    user1.user_permissions.add(Permission.objects.get(codename="change_survey"))
    survey = Survey.objects.create(
        name="Survey A", definition={"items": []}, created_by=user1
    )

    api_client = APIClient()
    api_client.force_authenticate(user1)
    response = api_client.put(
        f"/surveys/{survey.id}/",
        {
            "name": "Survey B",
            "definition": {"items": []},
        },
        format="json",
    )
    assert response.status_code == 200
    assert response.data["name"] == "Survey B"


def test_delete_own_survey():
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()
    user1.user_permissions.add(Permission.objects.get(codename="delete_survey"))
    survey = Survey.objects.create(
        name="Survey A", definition={"items": []}, created_by=user1
    )

    api_client = APIClient()
    api_client.force_authenticate(user1)
    assert Survey.objects.count() == 1
    response = api_client.delete(f"/surveys/{survey.id}/")
    assert response.status_code == 204
    assert Survey.objects.count() == 0


def test_delete_other_survey():
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()
    user2.user_permissions.add(Permission.objects.get(codename="delete_survey"))
    survey = Survey.objects.create(
        name="Survey A", definition={"items": []}, created_by=user1
    )

    api_client = APIClient()
    api_client.force_authenticate(user2)
    response = api_client.delete(f"/surveys/{survey.id}/")
    assert response.status_code == 404


def test_create_question_by_user1():
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()
    user1.user_permissions.add(Permission.objects.get(codename="add_question"))
    url = "/questions/"
    api_client = APIClient()
    api_client.force_authenticate(user1)
    response = api_client.post(url, {"title": "Question"})
    assert response.status_code == 201
    assert response.data["title"] == "Question"
    assert response.data["created_by"]["id"] == user1.id


def test_update_own_question_by_user1():
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()
    user1.user_permissions.add(Permission.objects.get(codename="change_question"))
    question = Question.objects.create(title="Question A", created_by=user1)

    api_client = APIClient()
    api_client.force_authenticate(user1)
    response = api_client.put(
        f"/questions/{question.id}/", {"title": "Question B"}, format="json"
    )
    assert response.status_code == 200
    assert response.data["title"] == "Question B"


def test_save_question_to_database():
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()
    user1.user_permissions.add(Permission.objects.get(codename="add_question"))
    url = "/questions/"
    api_client = APIClient()
    api_client.force_authenticate(user1)
    api_client.post(
        url,
        {
            "title": "Question",
            "category": "choice",
            "options": ["yes", "no"],
            "other": True,
            "refusable": True,
            "is_public": True,
        },
    )
    q = Question.objects.first()
    assert q.title == "Question"
    assert q.category == "choice"
    assert q.options == ["yes", "no"]
    assert q.other is True
    assert q.refusable is True
    assert q.is_public is True


def test_get_responses_by_anonymous():
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()
    url = "/responses/"
    api_client = APIClient()
    response = api_client.get(url)
    assert response.status_code == 401


def test_get_responses_by_agency_user(client):
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()
    user1.user_permissions.add(Permission.objects.get(codename="view_response"))
    user1.user_permissions.add(Permission.objects.get(codename="view_client"))
    survey1 = Survey.objects.create(name="survey1", definition={}, created_by=user1)
    question1 = Question.objects.create(title="question1", created_by=user1)
    response1 = Response.objects.create(
        survey=survey1, client=client1, created_by=user1
    )
    Answer.objects.create(response=response1, question=question1, value="yes")
    url = "/responses/"
    api_client = APIClient()
    api_client.force_authenticate(user1)
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["object"] == "Response"
    assert response.data["results"][0]["client"]["id"] == str(client1.id)
    assert response.data["results"][0]["client"]["object"] == "Client"
    assert response.data["results"][0]["created_by"]["id"] == user1.id


def test_create_response(client):
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()
    user1.user_permissions.add(Permission.objects.get(codename="add_response"))
    survey1 = Survey.objects.create(name="survey1", definition={}, created_by=user1)
    question1 = Question.objects.create(title="question1", created_by=user1)
    # client = Client.objects.create(first_name='John', last_name='Doe', dob='2000-01-01', created_by=user1)

    url = "/responses/"
    api_client = APIClient()
    api_client.force_authenticate(user1)
    data = {
        "survey": survey1.id,
        "client": client1.id,
        "answers": [
            {
                "question": question1.id,
                "value": "yes",
            },
        ],
    }
    # check api response
    response = api_client.post(url, data, format="json")
    assert response.status_code == 201

    # check model
    r = Response.objects.first()
    ans = Answer.objects.first()
    assert Response.objects.count() == 1
    assert r.survey == survey1
    assert r.client == client1
    assert Answer.objects.count() == 1
    assert ans.response == r
    assert ans.question == question1
    assert ans.value == "yes"


def test_create_response_with_context(client):
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()
    user1.user_permissions.add(Permission.objects.get(codename="add_response"))
    survey1 = Survey.objects.create(name="survey1", definition={}, created_by=user1)
    question1 = Question.objects.create(title="question1", created_by=user1)
    # client = Client.objects.create(first_name='John', last_name='Doe', dob='2000-01-01', created_by=user1)

    url = "/responses/"
    api_client = APIClient()
    api_client.force_authenticate(user1)
    data = {
        "survey": survey1.id,
        "client": client1.id,
        "response_context": {
            "id": survey1.id,
            "type": "Survey",
        },
        "answers": [
            {
                "question": question1.id,
                "value": "yes",
            },
        ],
    }
    # check api response
    response = api_client.post(url, data, format="json")
    assert response.status_code == 201
    # check model
    r = Response.objects.first()
    assert r.response_context == survey1


def test_create_response_invalid_survey(client):
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()
    user1.user_permissions.add(Permission.objects.get(codename="add_response"))
    survey2 = Survey.objects.create(name="survey2", definition={}, created_by=user2)
    question1 = Question.objects.create(title="question1", created_by=user1)
    client = Client.objects.create(
        first_name="John", last_name="Doe", dob="2000-01-01", created_by=user1
    )

    url = "/responses/"
    api_client = APIClient()
    api_client.force_authenticate(user1)
    data = {
        "survey": 9999,  # non-existing survey
        "client": client1.id,
        "answers": [
            {
                "question": question1.id,
                "value": "yes",
            },
        ],
    }
    # check api response
    response = api_client.post(url, data, format="json")
    assert response.status_code == 400


def test_update_response(client):
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()
    user1.user_permissions.add(Permission.objects.get(codename="change_response"))
    user1.user_permissions.add(Permission.objects.get(codename="view_client"))
    survey1 = Survey.objects.create(name="survey1", definition={}, created_by=user1)
    question1 = Question.objects.create(title="question1", created_by=user1)
    question2 = Question.objects.create(title="question2", created_by=user1)
    client = Client.objects.create(
        first_name="John", last_name="Doe", dob="2000-01-01", created_by=user1
    )
    response = Response.objects.create(survey=survey1, client=client, created_by=user1)
    response.answers.create(question=question1, value="no")

    url = f"/responses/{response.id}/"
    api_client = APIClient()
    api_client.force_authenticate(user1)
    data = {
        "survey": survey1.id,
        "client": client1.id,
        "answers": [
            {
                "question": question1.id,
                "value": "yes",
            },
        ],
    }
    # check api response
    r = api_client.put(url, data, format="json")
    assert r.status_code == 200
    response.refresh_from_db()
    assert len(response.answers.all()) == 1
    assert response.answers.all()[0].value == "yes"


def test_create_response_with_invalid_context_data(client):
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()
    user1.user_permissions.add(Permission.objects.get(codename="add_response"))
    survey1 = Survey.objects.create(name="survey1", definition={}, created_by=user1)
    question1 = Question.objects.create(title="question1", created_by=user1)
    client = Client.objects.create(
        first_name="John", last_name="Doe", dob="2000-01-01", created_by=user1
    )

    url = "/responses/"
    api_client = APIClient()
    api_client.force_authenticate(user1)
    data = {
        "survey": survey1.id,
        "client": client1.id,
        "response_context": {
            # 'id': survey1.id,
            # 'type': 'Survey',
        },
        "answers": [
            {
                "question": question1.id,
                "value": "yes",
            },
        ],
    }
    # check api response
    response = api_client.post(url, data, format="json")
    assert response.status_code == 400


def test_create_response_with_invalid_context_data2(client):
    agency1, agency2, user1, user2, client1, client2 = setup_2_agencies()
    user1.user_permissions.add(Permission.objects.get(codename="add_response"))
    survey1 = Survey.objects.create(name="survey1", definition={}, created_by=user1)
    question1 = Question.objects.create(title="question1", created_by=user1)
    client = Client.objects.create(
        first_name="John", last_name="Doe", dob="2000-01-01", created_by=user1
    )

    url = "/responses/"
    api_client = APIClient()
    api_client.force_authenticate(user1)
    data = {
        "survey": survey1.id,
        "client": client1.id,
        "response_context": {
            # 'id': survey1.id,
            "type": "FoobarFoobarFoobarFoobarFoobar",
        },
        "answers": [
            {
                "question": question1.id,
                "value": "yes",
            },
        ],
    }
    # check api response
    response = api_client.post(url, data, format="json")
    assert response.status_code == 400
