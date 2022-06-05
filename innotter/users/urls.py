from django.urls import include, path
from rest_framework import routers

from users.views import UserViewSet, UserRegistrationViewSet, UserLoginViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/registration/', UserRegistrationViewSet.as_view({'post': 'create'})),
    path('api/v1/login/', UserLoginViewSet.as_view({'post': 'create'})),
]
