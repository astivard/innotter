from django.urls import include, path
from posts.views import HomeViewSet, PostsViewSet, UserPostsViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"posts", PostsViewSet, basename="posts")
router.register(r"my-posts", UserPostsViewSet, basename="my-posts")
router.register(r"home", HomeViewSet, basename="home")

urlpatterns = [
    path("", include(router.urls)),
]
