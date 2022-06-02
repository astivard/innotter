from django.urls import include, path
from rest_framework import routers

from posts.views import PostViewSet


posts_router = routers.DefaultRouter()
posts_router.register(r'posts', PostViewSet, basename='posts')

urlpatterns = [
    path('api/v1/', include(posts_router.urls)),
]
