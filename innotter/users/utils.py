import django.contrib.auth.password_validation as validators
import jwt
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from innotter.settings import JWT_SECRET
from users.models import User
from users.services import create_jwt_token_dict


class UserRegistrationSerializerMethods(serializers.ModelSerializer):
    """Registration serializer methods"""

    def validate_password(self, value):
        try:
            validators.validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return make_password(value)


class UserLoginSerializerMethods(serializers.Serializer):
    """Login serializer methods"""

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        email = validated_data.get("email")
        password = validated_data.get("password")

        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise serializers.ValidationError("Incorrect password")
            validated_data["user"] = user
        except User.DoesNotExist:
            raise serializers.ValidationError("No such user")

        return validated_data

    def create(self, validated_data):
        return create_jwt_token_dict(to_refresh=False, validated_data=validated_data)


class UserRefreshSerializerMethods(serializers.Serializer):
    """Refresh serializer methods"""

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        refresh_token = validated_data.get("refresh_token")
        print(refresh_token)
        try:
            payload = jwt.decode(jwt=validated_data.get("refresh_token"), key=JWT_SECRET, algorithms=["HS256"])
            if payload.get("token_type") != "refresh":
                raise serializers.ValidationError("Token type is not refresh!")
            validated_data["payload"] = payload
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError("Refresh token is expired!")
        except jwt.InvalidTokenError:
            raise serializers.ValidationError("Refresh token is invalid!")

        return validated_data

    def create(self, validated_data):
        return create_jwt_token_dict(to_refresh=True, validated_data=validated_data)
