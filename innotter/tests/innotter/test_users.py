import pytest


register_payload = dict(
    username="test_user",
    title="test_user_title",
    email="test_user@gmail.com",
    password="test_user_password",
)


@pytest.mark.django_db
class TestPagesClass:
    def test_register_user(self, client):
        response = client.post(path="/api/v1/registration/", data=register_payload)
        data = response.data

        assert data["username"] == register_payload["username"]
        assert data["title"] == register_payload["title"]
        assert data["email"] == register_payload["email"]
        assert "password" not in data
        assert response.status_code == 201

    def test_login_user(self, register_user, client):
        response = client.post(
            path="/api/v1/login/", data=dict(email="test_user@gmail.com", password="test_user_password")
        )
        data = response.data

        assert "access" in data
        assert "refresh" in data
        assert response.status_code == 201

    def test_login_user_fail(self, register_user, client):
        response_1 = client.post(
            path="/api/v1/login/", data=dict(email="test_user@gmail.com", password="wrong_password")
        )
        data_1 = response_1.data

        response_2 = client.post(path="/api/v1/login/", data=dict(email="wrong_email", password="test_user_password"))
        data_2 = response_2.data

        assert "access" not in data_1
        assert "access" not in data_2
        assert "refresh" not in data_1
        assert "refresh" not in data_2

        assert response_1.status_code == 400
        assert response_2.status_code == 400

    def test_refresh_user_token(self, register_user, client):
        login_response = client.post(
            path="/api/v1/login/", data=dict(email="test_user@gmail.com", password="test_user_password")
        )
        refresh_response = client.post(path="/api/v1/refresh/", data=dict(refresh_token=login_response.data["refresh"]))
        data = refresh_response.data

        assert "access" in data
        assert "refresh" in data
        assert refresh_response.status_code == 201

    def test_getting_user_profile_for_auth_user(self, auth_user):
        response = auth_user.get(path="/api/v1/profile/")
        data = response.data

        assert response.status_code == 200
        assert len(data) == 1
        assert data[0]["username"] == register_payload["username"]
        assert data[0]["title"] == register_payload["title"]
        assert data[0]["email"] == register_payload["email"]
        assert "role" in data[0]
        assert "image_s3_path" in data[0]
