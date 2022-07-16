import pytest

from tests.innotter.services import _generate_uuid, get_owner_posts_number


@pytest.mark.django_db
class TestPagesClass:
    def test_post_create(self, mocker, auth_user, register_user):
        mocker.patch("posts.producer.publish", return_value=None)
        mocker.patch("posts.tasks.send_email_to_subscribers", return_value=None)

        auth_user.post(
            path="/api/v1/my-pages/",
            data=dict(owner=register_user, name="test_page_name", uuid=_generate_uuid(), is_blocked=False),
        )

        response = auth_user.post(path="/api/v1/my-posts/", data=dict(page=1, content="test content 1"))

        assert response.status_code == 201
        assert response.data["content"] == "test content 1"
        assert response.data["id"] == 1
        assert len(response.data) == 6

    def test_getting_owner_posts(self, mocker, auth_user, register_user):
        mocker.patch("posts.producer.publish", return_value=None)
        mocker.patch("posts.tasks.send_email_to_subscribers", return_value=None)

        auth_user.post(
            path="/api/v1/my-pages/",
            data=dict(owner=register_user, name="test_page_name", uuid=_generate_uuid(), is_blocked=False),
        )

        auth_user.post(path="/api/v1/my-posts/", data=dict(page=1, content="test content 1"))
        auth_user.post(path="/api/v1/my-posts/", data=dict(page=1, content="test content 2"))

        response = auth_user.get(path="/api/v1/my-posts/")

        owner_posts_number = get_owner_posts_number(owner=register_user)

        assert response.status_code == 200
        assert len(response.data) == owner_posts_number
