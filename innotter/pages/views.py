from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from pages.models import Page, Tag
from pages.serializers import PageListSerializer, PageDetailSerializer, TagSerializer
from posts.models import Post


class PageViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    """Pages"""

    queryset = Page.objects.all()
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action in ('retrieve', 'update'):
            return PageDetailSerializer
        return PageListSerializer


class TagViewSet(mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 mixins.ListModelMixin,
                 GenericViewSet):
    """Tags"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
