from rest_framework import serializers

from pages.models import Page, Tag


class PageListSerializer(serializers.ModelSerializer):
    """Serializer for list of pages"""

    class Meta:
        model = Page
        fields = ['id', 'name', 'uuid', 'description', 'image', 'tags', 'owner', 'is_private', 'unblock_date']
        read_only_fields = ['unblock_date']
        extra_kwargs = {'description': {'write_only': True},
                        'tags': {'write_only': True},
                        'image': {'write_only': True}}

    owner = serializers.ReadOnlyField(source='owner.username')


class PageDetailSerializer(serializers.ModelSerializer):
    """Serializer for separate page"""

    class Meta:
        model = Page
        fields = ['id', 'name', 'uuid', 'description', 'tags', 'owner', 'image', 'followers', 'image', 'is_private',
                  'follow_requests', 'unblock_date']
        read_only_fields = ['image', 'unblock_date']

    owner = serializers.ReadOnlyField(source='owner.username')
    tags = serializers.SlugRelatedField(many=True, slug_field='name', allow_null=True, queryset=Tag.objects.all())
    followers = serializers.SlugRelatedField(many=True, read_only=True, slug_field='username', allow_null=True)
    follow_requests = serializers.SlugRelatedField(many=True, read_only=True, slug_field='username', allow_null=True)


class TagSerializer(serializers.ModelSerializer):
    """Tags serializer"""

    class Meta:
        model = Tag
        fields = ['id', 'name']
