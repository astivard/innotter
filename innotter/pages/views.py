from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from pages.models import Page, Tag
from pages.serializers import StaffPageListSerializer, UserPageListSerializer, AdminPageDetailSerializer, \
    ModerPageDetailSerializer, PageDetailSerializer, TagSerializer, UserPageDetailSerializer, FollowersListSerializer
from pages.services import get_unblocked_pages, get_blocked_pages, get_permissions_list, get_page_followers, \
    follow_page, get_page_follow_requests, accept_all_follow_requests, get_all_follow_requests, \
    deny_all_follow_requests, accept_follow_request, deny_follow_request, get_page_tags, add_tag_to_page, \
    remove_tag_from_page
from users.permissions import IsAdminRole, IsModerRole, IsBlockedUser


class PagesViewSet(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """
    All pages by all users
    List, retrieve (for all users)
    Update (only for admins and moders)
    Non-blocked pages display only for admins and moders
    """

    action_permission_classes = {
        'list': (IsAuthenticated, ~IsBlockedUser,),
        'retrieve': (IsAuthenticated, ~IsBlockedUser,),
        'update': (IsAuthenticated, IsAdminRole | IsModerRole,),
        'partial_update': (IsAuthenticated, IsAdminRole | IsModerRole,),
        'blocked': (IsAuthenticated, IsAdminRole | IsModerRole,),
        'followers': (IsAuthenticated, ~IsBlockedUser),
        'follow': (IsAuthenticated, ~IsBlockedUser)
    }

    list_serializer_classes = {
        'admin': StaffPageListSerializer,
        'moderator': StaffPageListSerializer,
        'user': UserPageListSerializer,
    }

    detail_serializer_classes = {
        'admin': AdminPageDetailSerializer,
        'moderator': ModerPageDetailSerializer,
        'user': PageDetailSerializer,
    }

    filter_backends = (SearchFilter,)
    search_fields = ('name', 'uuid', 'tags__name',)

    @action(detail=False, methods=['get'], url_path='blocked')
    def blocked(self, request):
        return get_blocked_pages(self)

    @action(detail=True, methods=['get'], url_path='followers')
    def followers(self, request, pk=None):
        return get_page_followers(self, page_pk=pk)

    @action(detail=True, methods=['post'], url_path='follow')
    def follow(self, request, pk=None):
        return follow_page(self, page_pk=pk)

    def get_queryset(self):
        if self.request.user.role in ('admin', 'moderator'):
            return Page.objects.all().order_by('id')
        return get_unblocked_pages(is_owner_page=False)

    def get_serializer_class(self):
        user_role = self.request.user.role
        if self.action in ('list', 'blocked'):
            return self.list_serializer_classes.get(user_role)
        elif self.action == 'followers':
            return FollowersListSerializer
        return self.detail_serializer_classes.get(user_role)

    def get_permissions(self):
        return get_permissions_list(self, permission_classes_dict=self.action_permission_classes)


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

    permission_classes = (IsAuthenticated, ~IsBlockedUser,)

    @action(detail=True, methods=['get'], url_path='followers')
    def followers(self, request, pk=None):
        return get_page_followers(self, page_pk=pk)

    @action(detail=True, methods=['get'], url_path='follow-requests')
    def page_follow_requests(self, request, pk=None):
        return get_page_follow_requests(self, page_pk=pk)

    @action(detail=False, methods=['get'], url_path='follow-requests')
    def all_follow_requests(self, request):
        return get_all_follow_requests(self)

    @action(detail=True, methods=['post'], url_path='accept')
    def accept_follow_request(self, request, pk=None):
        return accept_follow_request(request=request, page_pk=pk)

    @action(detail=True, methods=['post'], url_path='deny')
    def deny_follow_request(self, request, pk=None):
        return deny_follow_request(request=request, page_pk=pk)

    @action(detail=True, methods=['post'], url_path='accept-all')
    def accept_all_follow_requests(self, request, pk=None):
        return accept_all_follow_requests(page_pk=pk)

    @action(detail=True, methods=['post'], url_path='deny-all')
    def deny_all_follow_requests(self, request, pk=None):
        return deny_all_follow_requests(page_pk=pk)

    @action(detail=True, methods=['get'], url_path='tags')
    def tags(self, request, pk=None):
        return get_page_tags(self, page_pk=pk)

    @action(detail=True, methods=['post'], url_path='add-tag')
    def add_tag_to_page(self, request, pk=None):
        return add_tag_to_page(request=request, page_pk=pk)

    @action(detail=True, methods=['post'], url_path='remove-tag')
    def remove_tag_from_page(self, request, pk=None):
        return remove_tag_from_page(request=request, page_pk=pk)

    def get_queryset(self):
        return get_unblocked_pages(is_owner_page=True, owner=self.request.user)

    def get_serializer_class(self):
        if self.action in ('list', 'create'):
            return UserPageListSerializer
        elif self.action in ('page_follow_requests', 'all_follow_requests', 'followers',):
            return FollowersListSerializer
        elif self.action == 'tags':
            return TagSerializer
        return UserPageDetailSerializer


class TagsViewSet(mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    """Tags"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated, ~IsBlockedUser)

    action_permission_classes = {
        'list': (IsAuthenticated, ~IsBlockedUser,),
        'create': (IsAuthenticated, ~IsBlockedUser,),
        'destroy': (IsAuthenticated, ~IsBlockedUser, IsAdminRole | IsModerRole,),
    }

    def get_permissions(self):
        return get_permissions_list(self, permission_classes_dict=self.action_permission_classes)
