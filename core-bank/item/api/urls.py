from rest_framework.routers import SimpleRouter
from item.api.viewsets import ItemViewSet
router = SimpleRouter()
router.register(
    prefix=r'',
    viewset=ItemViewSet,
    basename='ItemViewSet',
)

urlpatterns = router.urls
