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
    order
)

app_name = 'core'

urlpatterns = [
    path('', index, name='index'),
    path('add/user', UserCreateView.as_view(), name='create_user'),
    path('del/user', UserDeleteView.as_view(), name='delete_user'),
    path('users', UserListView.as_view(), name='users'),
    path('user/<pk>/', UserUpdateView.as_view(), name='user'),
    path('add/item', ItemCreateView.as_view(), name='create_item'),
    path('items', ItemListView.as_view(), name='items'),
    path('item/<pk>/', ItemUpdateView.as_view(), name='item'),
    path('order/<pk>/', order, name='order')
]
