from rest_framework import serializers

from pages.models import Page, Tag


class PageSerializer(serializers.ModelSerializer):
    """Pages serializer"""

    class Meta:
        model = Page
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    """Tags serializer"""

    class Meta:
        model = Tag
        fields = '__all__'
