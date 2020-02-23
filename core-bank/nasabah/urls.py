from django.urls import path
from .views import (
    UserListView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
    WithdrawView
)

app_name = 'nasabah'

urlpatterns = [
    path('', UserListView.as_view(), name='index'),
    path('add', UserCreateView.as_view(), name='add'),
    path('del/<pk>/', UserDeleteView.as_view(), name='delete'),
    path('user/<pk>/', UserUpdateView.as_view(), name='view'),
    path('wd/<pk>/', WithdrawView.as_view(), name='withdraw'),
]
