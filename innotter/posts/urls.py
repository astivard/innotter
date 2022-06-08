from django.urls import include, path
from rest_framework import routers

from posts.views import PostViewSet


router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls)),
]
