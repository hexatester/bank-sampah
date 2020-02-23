from core.api.base import BaseUserViewSet
from nasabah.models import Nasabah
from nasabah.api.serializers import NasabahSerializer


class NasabahViewSet(BaseUserViewSet):
    serializer_class = NasabahSerializer
    queryset = Nasabah.objects.all()
