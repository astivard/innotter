from rest_framework.permissions import IsAuthenticated

from pages.permissions import IsPublicPage
from pages.serializers import StaffPageListSerializer, UserPageListSerializer, AdminPageDetailSerializer, \
    ModerPageDetailSerializer, PageDetailSerializer
from users.permissions import IsAdminRole, IsModerRole, IsUserRole


action_permission_classes = {
    'list': (IsAuthenticated,),
    'retrieve': (IsAuthenticated, IsPublicPage | IsAdminRole | IsModerRole,),
    'update': (IsAuthenticated, IsAdminRole | IsModerRole,),
    'partial_update': (IsAuthenticated, IsAdminRole | IsModerRole,),
    'blocked': (IsAuthenticated, IsAdminRole | IsModerRole,),
    'followers': (IsAuthenticated,),
    'follow': (IsAuthenticated,)
}

user_action_permission_classes = {
    'list': (IsAuthenticated,),
    'retrieve': (IsAuthenticated,),
    'update': (IsAuthenticated, ),
    'partial_update': (IsAuthenticated,),
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
