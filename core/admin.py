from django.contrib import admin
from .models import (
    Nasabah,
    Item,
    OrderItem,
    Order
)


# Register your models here.

admin.site.register(Nasabah)
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
