from django.urls import path
from .views import (
    OrderListView,
    OrderCreateView,
    OrderDeleteView,
    OrderSubmitView,
)

app_name = 'order'

urlpatterns = [
    path('', OrderDeleteView.as_view(), name='index'),
    path('add/<pk>/', OrderCreateView.as_view(), name='order'),
    path('del/<pk>', OrderDeleteView.as_view(), name='delete'),
    path('set/<pk>/', OrderSubmitView.as_view(), name='set'),
]
