from django.db.models import Q
from django.utils import timezone

from pages.models import Page
from posts.models import Post


def get_posts(is_owner_posts: bool, owner=None) -> Page:
    if is_owner_posts and owner is None:
        raise Exception('The owner must be specified.')

    if is_owner_posts:
        pages = Page.objects.filter(Q(owner=owner),
                                    Q(is_blocked=False),
                                    Q(unblock_date__isnull=True) |
                                    Q(unblock_date__lt=timezone.now()))
    else:
        pages = Page.objects.filter(Q(is_blocked=False),
                                    Q(unblock_date__isnull=True) |
                                    Q(unblock_date__lt=timezone.now()))

    posts = Post.objects.filter(page__in=pages).order_by('id')

    return posts
