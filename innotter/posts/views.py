from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from posts.models import Post
from posts.serializers import PostListSerializer, PostDetailSerializer, HomeSerializer
from posts.services import get_posts, get_following_pages_posts, get_liked_posts, like_post, unlike_post
from users.permissions import IsAdminRole, IsModerRole, IsBlockedUser


class PostsViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    """
    All posts from all pages
    Only for admins and moderators
    """

    queryset = Post.objects.all().order_by('id')
    permission_classes = (IsAuthenticated, ~IsBlockedUser, IsAdminRole | IsModerRole,)
    serializer_class = PostListSerializer


class UserPostsViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    """Certain user posts"""

    permission_classes = (IsAuthenticated, ~IsBlockedUser,)

    def get_queryset(self):
        return get_posts(is_owner_posts=True, owner=self.request.user)

    def get_serializer_class(self):
        if self.action in ('retrieve', 'update', 'partial_update'):
            return PostDetailSerializer
        return PostListSerializer


class HomeViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    """Feed with posts"""

    serializer_class = HomeSerializer
    permission_classes = (IsAuthenticated, ~IsBlockedUser,)

    @action(detail=True, methods=['post'], url_path='like')
    def like(self, request, pk=None):
        return like_post(self, post_pk=pk)

    @action(detail=True, methods=['post'], url_path='unlike')
    def unlike(self, request, pk=None):
        return unlike_post(self, post_pk=pk)

    @action(detail=False, methods=['get'], url_path='liked')
    def liked(self, request, pk=None):
        return get_liked_posts(self)

    def get_queryset(self):
        return get_following_pages_posts(user=self.request.user)
