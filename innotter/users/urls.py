from django.urls import include, path
from rest_framework import routers

from users.views import UserViewSet, UserRegistrationViewSet, UserLoginViewSet, RefreshLoginViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'registration', UserRegistrationViewSet, basename='registration')
router.register(r'login', UserLoginViewSet, basename='login')
router.register(r'refresh', RefreshLoginViewSet, basename='refresh')

urlpatterns = [
    path('', include(router.urls)),
]
