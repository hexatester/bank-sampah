from rest_framework.routers import SimpleRouter
from order.api.viewsets import (
    OrderViewSet,
)
router = SimpleRouter()
router.register(
    prefix=r'',
    viewset=OrderViewSet,
    basename='OrderViewSet',
)
urlpatterns = router.urls
