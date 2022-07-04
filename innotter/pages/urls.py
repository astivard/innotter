from pages.views import CurrentUserPagesViewSet, PagesViewSet, TagsViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"pages", PagesViewSet, basename="pages")
router.register(r"my-pages", CurrentUserPagesViewSet, basename="my-pages")
router.register(r"tags", TagsViewSet, basename="tags")
