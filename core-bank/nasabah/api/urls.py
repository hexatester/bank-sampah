from rest_framework.routers import SimpleRouter
from nasabah.api.viewsets import NasabahViewSet
router = SimpleRouter()
router.register(
    prefix=r'',
    viewset=NasabahViewSet,
    basename='NasabahViewSet',
)

urlpatterns = router.urls
