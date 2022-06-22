from rest_framework import serializers

from posts.models import Post


class PostListSerializer(serializers.ModelSerializer):
    """Serializer for list of post"""

    class Meta:
        model = Post
        fields = ('id', 'content', 'page', 'reply_to', 'created_at', 'updated_at')


class PostDetailSerializer(serializers.ModelSerializer):
    """Serializer for separate post"""

    page_name = serializers.SerializerMethodField()
    reply_to_content = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = Post
        fields = ('id', 'content', 'page', 'page_name', 'reply_to', 'reply_to_content', 'created_at', 'updated_at')
        read_only_fields = ('page', 'created_at', 'updated_at')

    def get_page_name(self, post):
        return post.page.name

    def get_reply_to_content(self, post):
        return post.reply_to.content if post.reply_to else None


class HomeSerializer(serializers.ModelSerializer):
    """Serializer for feed with posts"""

    page = serializers.SlugRelatedField(slug_field='name', read_only=True)
    reply_to = serializers.SlugRelatedField(slug_field='content', read_only=True)
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M')

    class Meta:
        model = Post
        fields = ('id', 'page', 'content', 'reply_to', 'created_at',)
