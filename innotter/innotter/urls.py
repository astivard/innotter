from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from pages.urls import router as pages_router
from posts.urls import router as posts_router
from users.urls import router as users_router


router = routers.DefaultRouter()
router.registry.extend(pages_router.registry)
router.registry.extend(posts_router.registry)
router.registry.extend(users_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
]
