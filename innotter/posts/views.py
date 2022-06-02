from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from posts.models import Post
from posts.serializers import PostSerializer


class PostViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    """Posts"""

    serializer_class = PostSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Post.objects.all()
