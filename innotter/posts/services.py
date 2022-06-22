from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone

from pages.models import Page
from posts.models import Post
from users.models import User


def get_posts(is_owner_posts: bool, owner=None) -> Post:
    pages = Page.objects.filter(Q(is_blocked=False), Q(unblock_date__isnull=True) | Q(unblock_date__lt=timezone.now()))

    if is_owner_posts:
        pages = pages.filter(owner=owner)

    return Post.objects.filter(page__in=pages).order_by("id")


def get_following_pages_posts(user: User) -> Post:
    pages = Page.objects.filter(Q(followers=user) | Q(owner=user)).distinct()
    return Post.objects.filter(page__in=pages).order_by("-created_at")


def get_liked_posts(user: User) -> Post:
    return Post.objects.filter(likers=user).order_by("created_at")


def like_post(user: User, post_pk: int) -> None:
    post = get_object_or_404(Post, pk=post_pk)
    post.likers.add(user)


def unlike_post(user: User, post_pk: int) -> None:
    post = get_object_or_404(Post, pk=post_pk)
    post.likers.remove(user)


def get_page_name_and_followers_email_list(page_pk: int) -> (list, str):
    page = get_object_or_404(Page, pk=page_pk)
    page_followers = page.followers.filter(is_blocked=False)
    return page.name, [follower.email for follower in page_followers]
