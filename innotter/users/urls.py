from django.urls import include, path
from rest_framework import routers

from users.views import UserViewSet


users_router = routers.DefaultRouter()
users_router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('api/v1/', include(users_router.urls)),
]
