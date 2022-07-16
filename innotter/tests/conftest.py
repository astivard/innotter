import pytest
from rest_framework.test import APIClient

from users.models import User


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def register_user(request):
    marker = request.node.get_closest_marker("user_role")
    role = marker.args[0] if marker else "user"
    return User.objects.create_user(
        username="test_user",
        title="test_user_title",
        email="test_user@gmail.com",
        password="test_user_password",
        role=role,
    )


@pytest.fixture
def auth_user(register_user, client):
    response = client.post(path="/api/v1/login/", data=dict(email="test_user@gmail.com", password="test_user_password"))
    access_token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return client
