from django.urls import path
from .views import (
    ItemListView,
    ItemUpdateView,
    ItemCreateView,
    ItemDeleteView,
)

app_name = 'item'

urlpatterns = [
    path('', ItemListView.as_view(), name='index'),
    path('<pk>/', ItemUpdateView.as_view(), name='view'),
    path('add', ItemCreateView.as_view(), name='add'),
    path('del/<pk>/', ItemDeleteView.as_view(), name='delete'),
]
