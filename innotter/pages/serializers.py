from rest_framework import serializers

from pages.models import Page, Tag
from users.models import User


class UserPageListSerializer(serializers.ModelSerializer):
    """Serializer for list of pages for users."""

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Page
        fields = ('id', 'name', 'uuid', 'image', 'owner', 'is_private', 'is_blocked',)


class StaffPageListSerializer(serializers.ModelSerializer):
    """Serializer for list of pages for admins."""

    class Meta:
        model = Page
        fields = ('id', 'name', 'uuid', 'owner', 'owner_id', 'image',
                  'is_private', 'is_blocked', 'unblock_date')


class PageDetailSerializer(serializers.ModelSerializer):
    """Serializer for a simple page overview for any user."""

    owner = serializers.ReadOnlyField(source='owner.username')
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name', allow_null=True)
    followers = serializers.SlugRelatedField(many=True, read_only=True, slug_field='username', allow_null=True)

    class Meta:
        model = Page
        fields = ('name', 'uuid', 'description', 'tags', 'owner', 'image', 'followers', 'is_private')
        read_only_fields = ('name', 'uuid', 'description', 'tags', 'owner', 'image', 'followers', 'is_private')


class UserPageDetailSerializer(serializers.ModelSerializer):
    """Serializer for separate page for users only"""

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    followers = serializers.SlugRelatedField(many=True, read_only=True, slug_field='username')
    follow_requests = serializers.SlugRelatedField(many=True, read_only=True, slug_field='username')
    tags = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Tag.objects.all())
    is_private = serializers.BooleanField(required=True)

    class Meta:
        model = Page
        fields = ('id', 'name', 'uuid', 'description', 'tags', 'owner', 'image', 'followers', 'is_private',
                  'follow_requests',)
        read_only_fields = ('followers', 'follow_requests',)


class AdminPageDetailSerializer(serializers.ModelSerializer):
    """Serializer for separate page for admins only"""

    owner = serializers.ReadOnlyField(source='owner.username')
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name', allow_null=True)
    followers = serializers.SlugRelatedField(many=True, read_only=True, slug_field='username', allow_null=True)
    is_blocked = serializers.BooleanField()

    class Meta:
        model = Page
        fields = ('id', 'name', 'uuid', 'description', 'tags', 'owner', 'image', 'followers', 'is_private',
                  'unblock_date', 'is_blocked')
        read_only_fields = ('id', 'name', 'uuid', 'description', 'tags', 'owner', 'image', 'followers',
                            'is_private')


class ModerPageDetailSerializer(serializers.ModelSerializer):
    """Serializer for separate page for moderators only"""

    owner = serializers.ReadOnlyField(source='owner.username')
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name', allow_null=True)
    followers = serializers.SlugRelatedField(many=True, read_only=True, slug_field='username', allow_null=True)
    unblock_date = serializers.DateTimeField(required=True)

    class Meta:
        model = Page
        fields = ('id', 'name', 'uuid', 'description', 'tags', 'owner', 'image', 'followers', 'is_private',
                  'unblock_date', 'is_blocked')
        read_only_fields = ('id', 'name', 'uuid', 'description', 'tags', 'owner', 'image', 'followers',
                            'is_private', 'is_blocked')


class FollowersListSerializer(serializers.ModelSerializer):
    """
    Serializer for list of users that following page
    Methods: list
    For any user
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'title', 'email',)


class FollowerSerializer(serializers.ModelSerializer):
    """Serializer for accepting follow request"""

    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email',)


class TagSerializer(serializers.ModelSerializer):
    """Tags serializer"""

    class Meta:
        model = Tag
        fields = ('id', 'name')


class AddTagSerializer(serializers.ModelSerializer):
    """Add tag to page serializer"""

    name = serializers.CharField(max_length=30, required=True)

    class Meta:
        model = Tag
        fields = ('name',)
