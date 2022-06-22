from rest_framework import serializers

from users.models import User
from users.utils import UserRegistrationSerializerMethods, UserLoginSerializerMethods, UserRefreshSerializerMethods


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer for list of users
    Methods: list
    Only for admin
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'title', 'email', 'role', 'image', 'is_blocked')


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Seriazizer for separate user
    Methods: retrieve, update (only 'is_blocked' and 'role' fields)
    Only for admin
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'title', 'email', 'role', 'image', 'is_blocked',)
        read_only_fields = ('id', 'username', 'title', 'email', 'image')

    is_blocked = serializers.BooleanField()


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Seriazizer for user profile
    User can check his profile and update it
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'title', 'email', 'role', 'image',)
        read_only_fields = ('role',)


class UserRegistrationSerializer(UserRegistrationSerializerMethods):
    """Serialization of user registration and creation of a new one"""

    class Meta:
        model = User
        fields = ('username', 'title', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class UserLoginSerializer(UserLoginSerializerMethods):
    """Serializer for user getting access and refresh tokens"""

    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)


class UserRefreshSerializer(UserRefreshSerializerMethods):
    """Serializer for getting refresh token"""

    refresh_token = serializers.CharField(required=True, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
