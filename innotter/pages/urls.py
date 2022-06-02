from django.urls import include, path
from rest_framework import routers

from pages.views import PageViewSet, TagViewSet


pages_router = routers.DefaultRouter()
pages_router.register(r'pages', PageViewSet, basename='pages')

tags_router = routers.DefaultRouter()
tags_router.register(r'tags', TagViewSet, basename='tags')


urlpatterns = [
    path('api/v1/', include(pages_router.urls)),
    path('api/v1/', include(tags_router.urls)),
]
