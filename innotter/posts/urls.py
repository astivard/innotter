from django.urls import include, path
from rest_framework import routers

from posts.views import HomeViewSet, PostsViewSet, UserPostsViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostsViewSet, basename='posts')
router.register(r'my-posts', UserPostsViewSet, basename='my-posts')
router.register(r'home', HomeViewSet, basename='home')

urlpatterns = [
    path('', include(router.urls)),
]
