import django.contrib.auth.password_validation as validators
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class UserRegistrationSerializerMethods:
    """Registration serializer methods"""

    def validate_password(self, value):
        try:
            validators.validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return make_password(value)
