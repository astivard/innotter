from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from users.models import User
from users.permissions import IsAdminRole
from users.serializers import UserListSerializer, UserDetailSerializer, UserRegistrationSerializer, UserLoginSerializer, \
    UserRefreshSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    """
    Users viewset
    Only for admin
    """

    queryset = User.objects.all()
    permission_classes = (IsAdminRole,)

    def get_serializer_class(self):
        if self.action in ('retrieve', 'update'):
            return UserDetailSerializer
        return UserListSerializer


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

    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)


class RefreshLoginViewSet(mixins.CreateModelMixin,
                          GenericViewSet):
    """
    User refresh viewset (refreshing token)
    """

    queryset = User.objects.all()
    serializer_class = UserRefreshSerializer
    permission_classes = (AllowAny,)
