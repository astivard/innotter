from rest_framework import serializers

from users.models import User
from users.utils import UserRegistrationSerializerMethods


class UserListSerializer(serializers.ModelSerializer):
    """Serializer for list of users"""

    class Meta:
        model = User
        fields = ['id', 'username', 'title', 'email', 'role', 'is_blocked']


class UserDetailSerializer(serializers.ModelSerializer):
    """Seriazizer for separate user"""

    class Meta:
        model = User
        fields = ['id', 'username', 'title', 'email', 'role', 'image_s3_path', 'is_blocked']


class UserRegistrationSerializer(serializers.ModelSerializer, UserRegistrationSerializerMethods):
    """Serializer for user registration"""

    class Meta:
        model = User
        fields = ['username', 'title', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    email = serializers.EmailField(required=True)


class UserLoginSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""

    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}
