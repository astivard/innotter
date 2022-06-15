from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.response import Response

from pages.models import Page
from posts.models import Post
from users.models import User


def get_posts(is_owner_posts: bool, owner=None) -> Post:
    pages = Page.objects.filter(Q(is_blocked=False),
                                Q(unblock_date__isnull=True) |
                                Q(unblock_date__lt=timezone.now()))

    if is_owner_posts:
        pages = pages.filter(owner=owner)

    return Post.objects.filter(page__in=pages).order_by('id')


def get_following_pages_posts(user: User) -> Post:
    pages = Page.objects.filter(Q(followers=user) | Q(owner=user)).distinct()
    return Post.objects.filter(page__in=pages).order_by('-created_at')


def get_liked_posts(self) -> Response:
    liked_posts = Post.objects.filter(likers=self.request.user).order_by('created_at')
    if liked_posts:
        serializer = self.get_serializer(liked_posts, many=True)
        return Response(data=serializer.data)
    return Response({'detail': 'You didn\'t like any post.'})


def like_post(self, post_pk: int) -> Response:
    user = self.request.user
    post = get_object_or_404(Post, pk=post_pk)
    if not post.likers.contains(user):
        post.likers.add(user)
        return Response({'detail': 'You have successfully liked this post.'})
    return Response({'detail': 'You have already liked this post.'})


def unlike_post(self, post_pk: int) -> Response:
    user = self.request.user
    post = get_object_or_404(Post, pk=post_pk)
    if post.likers.contains(user):
        post.likers.remove(user)
        return Response({'detail': 'You have successfully unliked this post.'})
    return Response({'detail': 'You didn\'t like this post.'})
