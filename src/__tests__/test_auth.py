import pytest
from django.contrib.auth.models import User


def test_user_auth_happy_path(client):
    user = User.objects.create_user(
        username="user1@example.com", email="user1@example.com", password="pass"
    )

    response = client.post(
        "/users/auth/", {"username": "user1@example.com", "password": "pass"}
    )
    assert response.status_code == 200
    assert "token" in response.json()
