from django.urls import include, path
from rest_framework import routers

from posts.views import PostsViewSet, UserPostsViewSet


router = routers.DefaultRouter()
router.register(r'posts', PostsViewSet, basename='posts')
router.register(r'my-posts', UserPostsViewSet, basename='my-posts')

urlpatterns = [
    path('', include(router.urls)),
]
