from django.urls import include, path
from rest_framework import routers

from pages.views import PagesViewSet, CurrentUserPagesViewSet, TagViewSet


router = routers.DefaultRouter()
router.register(r'all-pages', PagesViewSet, basename='all-pages')
router.register(r'my-pages', CurrentUserPagesViewSet, basename='my-pages')
router.register(r'tags', TagViewSet, basename='tags')

urlpatterns = [
    path('', include(router.urls)),
]
