from core.api.base import BaseUserViewSet
from item.api.serializers import ItemSerializer
from item.models import Item


class ItemViewSet(BaseUserViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
