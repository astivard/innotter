import pytest

from tests.innotter.services import get_all_pages_number, get_unblock_pages_number, generate_pages


@pytest.mark.django_db
class TestPagesClass:
    def test_getting_unblocked_pages_for_user(self, auth_user, register_user):
        generate_pages(owner=register_user, blocked_number=2, unblocked_number=3)
        unblocked_pages_number = get_unblock_pages_number()

        response = auth_user.get(path="/api/v1/pages/")
        data = response.data

        assert response.status_code == 200
        assert len(data) == unblocked_pages_number
        assert len(data) == 3

    @pytest.mark.user_role("moderator")
    def test_getting_all_pages_for_moderator(self, auth_user, register_user):
        generate_pages(owner=register_user, blocked_number=2, unblocked_number=3)
        all_pages_number = get_all_pages_number()

        response = auth_user.get(path="/api/v1/pages/")
        data = response.data

        assert response.status_code == 200
        assert len(data) == all_pages_number
        assert len(data) == 5

    @pytest.mark.user_role("admin")
    def test_getting_all_pages_for_admin(self, auth_user, register_user):
        generate_pages(owner=register_user, blocked_number=2, unblocked_number=3)
        all_pages_number = get_all_pages_number()

        response = auth_user.get(path="/api/v1/pages/")
        data = response.data

        assert response.status_code == 200
        assert len(data) == all_pages_number
        assert len(data) == 5
