
from django.urls import path, include

urlpatterns = [
    path('item/', include('item.api.urls'), name='item'),
    path('nasabah/', include('nasabah.api.urls'), name='nasabah'),
    path('order/', include('order.api.urls'), name='order'),
]
