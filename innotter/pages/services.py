from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response

from pages.models import Page, Tag
from pages.tasks import upload_file_to_s3
from users.models import User
from users.services import is_allowed_file_extension, generate_file_name, get_presigned_url


def get_permissions_list(self, permission_classes_dict: dict) -> list:
    permission_classes = permission_classes_dict.get(self.action, list())
    return [permission() for permission in permission_classes]


def get_unblocked_pages(is_owner_page: bool, owner=None) -> Page:
    pages = Page.objects.filter(
        Q(is_blocked=False),
        Q(unblock_date__isnull=True) | Q(unblock_date__lt=timezone.now()),
    ).order_by("id")
    if is_owner_page:
        pages = pages.filter(owner=owner)
    return pages


def get_blocked_pages() -> Page:
    return Page.objects.filter(is_blocked=True).order_by("id")


def get_page_followers(page_pk: int) -> Page:
    return get_object_or_404(Page, pk=page_pk).followers.all().order_by("id")


def get_page_follow_requests(page_pk: int) -> Response:
    return get_object_or_404(Page, pk=page_pk).follow_requests.all().order_by("id")


def follow_page(user: User, page_pk: int) -> bool:
    page = get_object_or_404(Page, pk=page_pk)
    if page.is_private:
        page.follow_requests.add(user)
        return True
    page.followers.add(user)
    return False


def unfollow_page(user: User, page_pk: int) -> None:
    page = get_object_or_404(Page, pk=page_pk)
    page.follow_requests.remove(user)


def accept_follow_request(follower_email: str, page_pk: int) -> None:
    page = get_object_or_404(Page, pk=page_pk)
    potential_follower = get_object_or_404(User, email=follower_email)
    page.followers.add(potential_follower)
    page.follow_requests.remove(potential_follower)


def deny_follow_request(follower_email: str, page_pk: int) -> None:
    page = get_object_or_404(Page, pk=page_pk)
    potential_follower = get_object_or_404(User, email=follower_email)
    page.follow_requests.remove(potential_follower)


def accept_all_follow_requests(page_pk: int) -> None:
    page = get_object_or_404(Page, pk=page_pk)
    follow_requests = page.follow_requests.all()
    if follow_requests:
        for potential_follower in follow_requests:
            page.followers.add(potential_follower)
            page.follow_requests.remove(potential_follower)


def deny_all_follow_requests(page_pk: int) -> None:
    page = get_object_or_404(Page, pk=page_pk)
    follow_requests = page.follow_requests.all()
    if follow_requests:
        for potential_follower in follow_requests:
            page.follow_requests.remove(potential_follower)


def get_page_tags(page_pk: int) -> Tag:
    page = get_object_or_404(Page, pk=page_pk)
    return page.tags.all()


def add_tag_to_page(tag_name: str, page_pk: int) -> None:
    page = get_object_or_404(Page, pk=page_pk)
    tag = get_object_or_404(Tag, name=tag_name)
    page.tags.add(tag)


def remove_tag_from_page(tag_name: str, page_pk: int) -> None:
    page = get_object_or_404(Page, pk=page_pk)
    tag = get_object_or_404(Tag, name=tag_name)
    page.tags.remove(tag)


def upload_page_image_to_s3(file_path: str, page_id: Page) -> str:
    if not is_allowed_file_extension(file_path=file_path):
        error_msg = "Files with this extension are not allowed."
        raise ValidationError(error_msg)

    page = get_object_or_404(Page, pk=page_id)
    key = generate_file_name(file_path=file_path, key=page.uuid, is_user_image=False)

    page.image_s3_path = key
    page.save()

    try:
        upload_file_to_s3.delay(file_path=file_path, key=key)
    except FileNotFoundError:
        error_msg = f"No such file or directory: {file_path}"
        raise NotFound(error_msg)

    presigned_url = get_presigned_url(key=key)

    return presigned_url
