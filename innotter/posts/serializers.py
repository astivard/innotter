from rest_framework import serializers

from pages.models import Page
from posts.models import Post


class PostListSerializer(serializers.ModelSerializer):
    """Serializer for list of post"""

    class Meta:
        model = Post
        fields = ('id', 'content', 'page_id', 'page_name', 'reply_to', 'reply_to_id', 'created_at', 'updated_at')

    page_name = serializers.SerializerMethodField(read_only=True)
    reply_to = serializers.SlugRelatedField(slug_field='content', read_only=True)
    reply_to_id = serializers.SerializerMethodField(allow_null=True, read_only=True)

    def get_reply_to_id(self, post):
        return post.reply_to.pk if post.reply_to else None

    def get_page_name(self, post):
        return post.page.name


class PostDetailSerializer(serializers.ModelSerializer):
    """Serializer for separate post"""

    class Meta:
        model = Post
        fields = ('id', 'content', 'page', 'reply_to', 'reply_to_id', 'created_at', 'updated_at')

    page = serializers.SlugRelatedField(slug_field='name', queryset=Page.objects.all(), required=False)
    reply_to = serializers.SlugRelatedField(slug_field='content', queryset=Post.objects.all(), required=False)
    reply_to_id = serializers.SerializerMethodField(allow_null=True)

    def get_reply_to_id(self, post):
        return post.reply_to.pk if post.reply_to else None


class HomeSerializer(serializers.ModelSerializer):
    """Serializer for feed with posts"""

    page = serializers.SlugRelatedField(slug_field='name', read_only=True)
    reply_to = serializers.SlugRelatedField(slug_field='content', read_only=True)
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M')

    class Meta:
        model = Post
        fields = ('id', 'page', 'content', 'reply_to', 'created_at',)
