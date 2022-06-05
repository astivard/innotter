from django.urls import include, path
from rest_framework import routers

from pages.views import PageViewSet, TagViewSet


router = routers.DefaultRouter()
router.register(r'pages', PageViewSet, basename='pages')
router.register(r'tags', TagViewSet, basename='tags')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
