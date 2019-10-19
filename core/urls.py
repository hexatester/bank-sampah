from django.urls import path
from .views import (
    IndexView,
    Login,
    Logout,
    UserListView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
    ItemListView,
    ItemUpdateView,
    ItemCreateView,
    ItemDeleteView,
    OrderCreateView,
    OrderDeleteView,
    OrderSubmitView,
    WithdrawView
)

app_name = 'core'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
    path('user/add', UserCreateView.as_view(), name='create_user'),
    path('user/del/<pk>/', UserDeleteView.as_view(), name='delete_user'),
    path('users', UserListView.as_view(), name='users'),
    path('user/<pk>/', UserUpdateView.as_view(), name='user'),
    path('item/add', ItemCreateView.as_view(), name='create_item'),
    path('item/del/<pk>/', ItemDeleteView.as_view(), name='delete_item'),
    path('items', ItemListView.as_view(), name='items'),
    path('item/<pk>/', ItemUpdateView.as_view(), name='item'),
    path('order/del/<pk>', OrderDeleteView.as_view(), name='delete_order'),
    path('order/<pk>/', OrderCreateView.as_view(), name='order'),
    path('order/set/<pk>/', OrderSubmitView.as_view(), name='order_set'),
    path('wd/<pk>/', WithdrawView.as_view(), name='withdraw'),
]
