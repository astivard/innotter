from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from users.models import User
from users.serializers import UserListSerializer, UserDetailSerializer, UserRegistrationSerializer, UserLoginSerializer


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    """Users"""

    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action in ('retrieve', 'update'):
            return UserDetailSerializer
        return UserListSerializer


class UserRegistrationViewSet(viewsets.ModelViewSet):
    """User registration view set (creating new account)"""

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)


class UserLoginViewSet(viewsets.ModelViewSet):
    """User login view set (getting access and refresh token)"""

    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)
