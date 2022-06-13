from django.db.models import Q
from django.utils import timezone
from rest_framework import mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from pages.models import Page, Tag
from pages.serializers import PageListSerializer, TagSerializer, UserPageDetailSerializer
from pages.utils import user_role_serializers_dict


class PagesViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   mixins.UpdateModelMixin,
                   GenericViewSet):
    """
    Pages
    List, retrieve, update (only for admins and moders)
    Non-blocked pages displayed only for admins
    """

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Page.objects.all()
        return Page.objects.filter(
            Q(is_blocked=False),
            Q(unblock_date__isnull=True) | Q(unblock_date__lt=timezone.now())
        )

    def get_serializer_class(self):
        if self.action in ('retrieve', 'update'):
            return user_role_serializers_dict.get(self.request.user.role)
        return PageListSerializer


class CurrentUserPagesViewSet(mixins.CreateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.DestroyModelMixin,
                              mixins.ListModelMixin,
                              GenericViewSet):
    """Current user pages"""

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Page.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action in ('retrieve', 'update'):
            return UserPageDetailSerializer
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
