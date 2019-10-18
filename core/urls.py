from django.urls import path
from .views import (
    index,
    UserListView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
    ItemListView,
    ItemUpdateView,
    ItemCreateView,
    ItemDeleteView,
    OrderCreateView,
    OrderDeleteView
)

app_name = 'core'

urlpatterns = [
    path('', index, name='index'),
    path('user/add', UserCreateView.as_view(), name='create_user'),
    path('user/del/<pk>', UserDeleteView.as_view(), name='delete_user'),
    path('users', UserListView.as_view(), name='users'),
    path('user/<pk>/', UserUpdateView.as_view(), name='user'),
    path('item/add', ItemCreateView.as_view(), name='create_item'),
    path('item/del/<pk>', ItemDeleteView.as_view(), name='delete_item'),
    path('items', ItemListView.as_view(), name='items'),
    path('item/<pk>/', ItemUpdateView.as_view(), name='item'),
    path('order/del/<pk>', OrderDeleteView.as_view(), name='delete_order'),
    path('order/<pk>/', OrderCreateView.as_view(), name='order')
]
