from django.urls import path
from .views import (
    OrderListView,
    OrderCreateView,
    OrderDeleteView,
    OrderSubmitView,
    OrderItemDeleteView,
)

app_name = 'order'

urlpatterns = [
    path('', OrderListView.as_view(), name='index'),
    path('add/<pk>/', OrderCreateView.as_view(), name='order'),
    path('del/<pk>', OrderDeleteView.as_view(), name='delete'),
    path('set/<pk>/', OrderSubmitView.as_view(), name='set'),
    path('item/<pk>', OrderItemDeleteView.as_view(), name='delete_item'),
]
