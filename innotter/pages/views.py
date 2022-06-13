from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from pages.models import Page, Tag
from pages.serializers import TagSerializer, UserPageDetailSerializer, FollowersListSerializer
from pages.services import get_unblocked_pages, get_blocked_pages, get_permissions_list, get_page_followers, \
    follow_page, get_page_follow_requests
from pages.utils import list_serializer_classes, detail_serializer_classes, action_permission_classes, \
    user_action_permission_classes


class PagesViewSet(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """
    All pages by all users
    List, retrieve (for all users)
    Update is_blocked and (only for admins and moders)
    Non-blocked pages display only for admins and moders
    """

    filter_backends = (SearchFilter,)
    search_fields = ('name', 'uuid', 'tags__name',)

    @action(detail=False)
    def blocked(self, request):
        return get_blocked_pages(self)

    @action(detail=True)
    def followers(self, request, pk=None):
        return get_page_followers(self, page_pk=pk)

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        return follow_page(self, page_pk=pk)

    def get_queryset(self):
        if self.request.user.role in ('admin', 'moderator'):
            return Page.objects.all().order_by('id')
        return get_unblocked_pages(is_owner_page=False)

    def get_serializer_class(self):
        user_role = self.request.user.role
        if self.action in ('list', 'blocked'):
            return list_serializer_classes.get(user_role)
        elif self.action == 'followers':
            return FollowersListSerializer
        return detail_serializer_classes.get(user_role)

    def get_permissions(self):
        return get_permissions_list(self, permission_classes_dict=action_permission_classes)


class CurrentUserPagesViewSet(mixins.CreateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.DestroyModelMixin,
                              mixins.ListModelMixin,
                              GenericViewSet):
    """
    Current user pages
    Retrieve, create, update, delete page
    """

    @action(detail=True)
    def followers(self, request, pk=None):
        return get_page_followers(self, page_pk=pk)

    @action(detail=True, url_path='follow-requests')
    def follow_requests(self, request, pk=None):
        return get_page_follow_requests(self, page_pk=pk)

    def get_queryset(self):
        return get_unblocked_pages(is_owner_page=True, owner=self.request.user)

    def get_serializer_class(self):
        user_role = self.request.user.role
        if self.action == 'list':
            return list_serializer_classes.get(user_role)
        elif self.action == 'follow_requests':
            return FollowersListSerializer
        return detail_serializer_classes.get(user_role) if user_role in ('admin', 'moderator') \
            else UserPageDetailSerializer

    def get_permissions(self):
        return get_permissions_list(self, permission_classes_dict=user_action_permission_classes)


class TagsViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    """Tags"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
