from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from posts.models import Post
from posts.serializers import PostListSerializer, PostDetailSerializer


class PostViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    """Posts"""

    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = PostListSerializer

    def get_serializer_class(self):
        if self.action in ('retrieve', 'update'):
            return PostDetailSerializer
        return PostListSerializer
