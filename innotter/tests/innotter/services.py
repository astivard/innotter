import uuid

from pages.models import Page
from pages.services import get_unblocked_pages
from users.models import User


def get_all_pages_number() -> int:
    return Page.objects.all().count()


def get_unblock_pages_number() -> int:
    return get_unblocked_pages(is_owner_page=False).count()


def get_owner_posts_number(owner: User) -> int:
    pages = Page.objects.filter(owner=owner)
    return pages[0].posts.all().count()


def generate_pages(owner: User, blocked_number: int, unblocked_number: int) -> None:
    for i in range(unblocked_number):
        Page.objects.create(owner=owner, uuid=_generate_uuid(), is_blocked=False)
    for i in range(blocked_number):
        Page.objects.create(owner=owner, uuid=_generate_uuid(), is_blocked=True)


def _generate_uuid() -> str:
    return str(uuid.uuid4())[:30]
