from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from posts.models import Post
from posts.permissions import IsAdminOrModeratorRole, IsUserPageOwner
from posts.serializers import PostListSerializer, PostDetailSerializer
from posts.services import get_posts


class PostsViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    """
    All posts from all pages
    Only for admins and moderators
    """

    queryset = Post.objects.all().order_by('id')
    permission_classes = (IsAuthenticated, IsAdminOrModeratorRole,)
    serializer_class = PostListSerializer


class UserPostsViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    """Certain user posts """

    def get_queryset(self):
        return get_posts(is_owner_posts=True, owner=self.request.user)

    def get_serializer_class(self):
        if self.action in ('retrieve', 'update'):
            return PostDetailSerializer
        return PostListSerializer
