from rest_framework import mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from users.models import User
from users.permissions import IsAdminRole, IsBlockedUser
from users.serializers import UserListSerializer, UserDetailSerializer, UserRegistrationSerializer, UserLoginSerializer, \
    UserRefreshSerializer, UserProfileSerializer
from users.services import block_or_unblock_all_pages, set_access_to_admin_panel


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    """
    Users viewset
    Only for admin
    """

    queryset = User.objects.all().order_by('id')
    permission_classes = (IsAuthenticated, IsAdminRole,)

    def get_serializer_class(self):
        if self.action in ('retrieve', 'update', 'partial_update', 'get_user_profile'):
            return UserDetailSerializer
        return UserListSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if 'is_blocked' in request.data:
            block_or_unblock_all_pages(user=instance)
        elif 'role' in request.data:
            set_access_to_admin_panel(user=instance)
        return Response(serializer.data)


class UserProfileViewSet(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    """
    Users profile viewset
    """

    permission_classes = (IsAuthenticated, ~IsBlockedUser)
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return User.objects.filter(username=self.request.user)


class UserRegistrationViewSet(mixins.CreateModelMixin,
                              GenericViewSet):
    """
    User registration view set (creating new account)
    """

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)


class UserLoginViewSet(mixins.CreateModelMixin,
                       GenericViewSet):
    """
    User login viewset (getting access and refresh token)
    """

    serializer_class = UserLoginSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)


class RefreshLoginViewSet(mixins.CreateModelMixin,
                          GenericViewSet):
    """
    User refresh viewset (refreshing token)
    """

    queryset = User.objects.all()
    serializer_class = UserRefreshSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED, headers=headers)
