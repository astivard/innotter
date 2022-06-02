from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Users serializer"""

    class Meta:
        model = User
        fields = '__all__'
