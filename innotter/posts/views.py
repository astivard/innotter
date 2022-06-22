from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from posts.models import Post
from posts.serializers import HomeSerializer, PostDetailSerializer, PostListSerializer
from posts.services import (
    get_following_pages_posts,
    get_liked_posts,
    get_posts,
    like_post,
    unlike_post,
    get_page_name_and_followers_email_list,
)
from posts.tasks import send_email_to_subscribers
from users.permissions import IsAdminRole, IsBlockedUser, IsModerRole


class PostsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    """
    All posts from all pages
    Only for admins and moderators
    """

    queryset = Post.objects.all().order_by("id")
    permission_classes = (
        IsAuthenticated,
        ~IsBlockedUser,
        IsAdminRole | IsModerRole,
    )
    serializer_class = PostListSerializer


class UserPostsViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """Certain user posts"""

    permission_classes = (
        IsAuthenticated,
        ~IsBlockedUser,
    )

    def get_queryset(self):
        return get_posts(is_owner_posts=True, owner=self.request.user)

    def get_serializer_class(self):
        if self.action in ("retrieve", "update", "partial_update"):
            return PostDetailSerializer
        return PostListSerializer

    def perform_create(self, serializer):
        serializer.save()
        page_name_and_follower_emails = get_page_name_and_followers_email_list(page_pk=self.request.data["page"][0])
        send_email_to_subscribers.delay(
            page=page_name_and_follower_emails[0], follower_list=page_name_and_follower_emails[1]
        )


class HomeViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    """Feed with posts"""

    serializer_class = HomeSerializer
    permission_classes = (
        IsAuthenticated,
        ~IsBlockedUser,
    )

    @action(detail=True, methods=["post"], url_path="like")
    def like(self, request, pk=None):
        like_post(user=self.request.user, post_pk=pk)
        return Response({"detail": "You have liked this post."})

    @action(detail=True, methods=["post"], url_path="unlike")
    def unlike(self, request, pk=None):
        unlike_post(user=self.request.user, post_pk=pk)
        return Response({"detail": "You have unliked this post."})

    @action(detail=False, methods=["get"], url_path="liked")
    def liked(self, request, pk=None):
        liked_posts = get_liked_posts(user=self.request.user)
        serializer = self.get_serializer(liked_posts, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        return get_following_pages_posts(user=self.request.user)
