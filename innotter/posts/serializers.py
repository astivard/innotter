from posts.models import Post

from posts.utils import PostSerializerMixin


class PostListSerializer(PostSerializerMixin):
    """Serializer for list of post"""

    class Meta:
        model = Post
        fields = ('id', 'page', 'content', 'reply_to', 'created_at', 'updated_at')


class PostDetailSerializer(PostSerializerMixin):
    """Serializer for separate post"""

    class Meta:
        model = Post
        fields = ('id', 'page', 'content', 'reply_to', 'created_at', 'updated_at')
