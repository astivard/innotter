from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    """Posts serializer"""

    class Meta:
        model = Post
        fields = '__all__'
