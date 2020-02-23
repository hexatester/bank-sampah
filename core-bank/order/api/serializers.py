from rest_framework.serializers import ModelSerializer
from order.models import OrderItem, Order


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ['user']


class OrderSerializer(ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        exclude = ['user']
        read_only_fields = ['total', 'weigth', 'sums', 'ordered']

    def create(self, validated_data: dict):
        items = validated_data.pop('items')
        nasabah = validated_data.get('nasabah')
        order: Order = Order.objects.create(**validated_data)
        for item in items:
            order.items.add(
                OrderItem.objects.create(
                    nasabah=nasabah,
                    **item)
            )
        order.save()
        return order
