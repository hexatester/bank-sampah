from core.api.base import BaseUserViewSet
from order.models import (
    Order,
    OrderItem
)
from order.api.serializers import (
    OrderSerializer,
    OrderItemSerializer,
)


class OrderViewSet(BaseUserViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderItemViewSet(BaseUserViewSet):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()
