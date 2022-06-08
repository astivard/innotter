from rest_framework import serializers

from pages.models import Page, Tag


class PageListSerializer(serializers.ModelSerializer):
    """Serializer for list of pages"""

    class Meta:
        model = Page
        fields = ('id', 'name', 'uuid', 'description', 'image', 'tags', 'owner', 'is_private')
        extra_kwargs = {'description': {'write_only': True},
                        'tags': {'write_only': True},
                        'image': {'write_only': True}}


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
        read_only_fields = ('image',)

    owner = serializers.ReadOnlyField(source='owner.username')
    tags = serializers.SlugRelatedField(many=True, slug_field='name', allow_null=True, queryset=Tag.objects.all())
    followers = serializers.SlugRelatedField(many=True, read_only=True, slug_field='username', allow_null=True)
    follow_requests = serializers.SlugRelatedField(many=True, read_only=True, slug_field='username', allow_null=True)


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
    unblock_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S')


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
    unblock_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S')


class TagSerializer(serializers.ModelSerializer):
    """Tags serializer"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
