from rest_framework import serializers

from pages.models import Page, Tag


class UserPageListSerializer(serializers.ModelSerializer):
    """Serializer for list of pages for users"""

    class Meta:
        model = Page
        fields = ('id', 'name', 'uuid', 'image', 'owner', 'is_private')

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())


class AdminPageListSerializer(serializers.ModelSerializer):
    """Serializer for list of pages for admins"""

    class Meta:
        model = Page
        fields = ('id', 'name', 'uuid', 'owner', 'owner_id', 'image',
                  'is_private', 'is_blocked', 'unblock_date')


class PageDetailSerializer(serializers.ModelSerializer):
    """Serializer for a simple page overview for any user"""

    class Meta:
        model = Page
        fields = ('name', 'uuid', 'description', 'tags', 'owner', 'image', 'followers', 'is_private')
        read_only_fields = ('name', 'uuid', 'description', 'tags', 'owner', 'image', 'followers', 'is_private')

    owner = serializers.ReadOnlyField(source='owner.username')
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name', allow_null=True)
    followers = serializers.SlugRelatedField(many=True, read_only=True, slug_field='username', allow_null=True)


class UserPageDetailSerializer(serializers.ModelSerializer):
    """Serializer for separate page for users only"""

    class Meta:
        model = Page
        fields = ('id', 'name', 'uuid', 'description', 'tags', 'owner', 'image', 'followers', 'is_private',
                  'follow_requests', 'is_blocked', 'unblock_date')

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    followers = serializers.SlugRelatedField(many=True, read_only=True, slug_field='username')
    follow_requests = serializers.SlugRelatedField(many=True, read_only=True, slug_field='username')
    tags = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Tag.objects.all())
    is_private = serializers.BooleanField(required=True)


class ModerPageListSerializer(serializers.ModelSerializer):
    """Serializer for list of pages for moderators"""

    class Meta:
        model = Page
        fields = ('id', 'name', 'uuid', 'owner', 'owner_id', 'image',
                  'is_private', 'is_blocked', 'unblock_date')


class AdminPageDetailSerializer(serializers.ModelSerializer):
    """Serializer for separate page for admins only"""

    class Meta:
        model = Page
        fields = ('id', 'name', 'uuid', 'description', 'tags', 'owner', 'image', 'followers', 'is_private',
                  'unblock_date', 'is_blocked')
        read_only_fields = ('id', 'name', 'uuid', 'description', 'tags', 'owner', 'image', 'followers',
                            'is_private')

    owner = serializers.ReadOnlyField(source='owner.username')
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name', allow_null=True)
    followers = serializers.SlugRelatedField(many=True, read_only=True, slug_field='username', allow_null=True)
    is_blocked = serializers.BooleanField()


class ModerPageDetailSerializer(serializers.ModelSerializer):
    """Serializer for separate page for moderators only"""

    class Meta:
        model = Page
        fields = ('id', 'name', 'uuid', 'description', 'tags', 'owner', 'image', 'followers', 'is_private',
                  'unblock_date', 'is_blocked')
        read_only_fields = ('id', 'name', 'uuid', 'description', 'tags', 'owner', 'image', 'followers',
                            'is_private', 'is_blocked')

    owner = serializers.ReadOnlyField(source='owner.username')
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name', allow_null=True)
    followers = serializers.SlugRelatedField(many=True, read_only=True, slug_field='username', allow_null=True)
    unblock_date = serializers.DateTimeField(required=True)


class TagSerializer(serializers.ModelSerializer):
    """Tags serializer"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
