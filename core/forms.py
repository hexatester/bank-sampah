from django.utils.translation import gettext_lazy as _
from django import forms
from .models import (
    Nasabah,
    Item,
    OrderItem,
    Order
)


class NasabahCreateForm(forms.ModelForm):
    class Meta:
        model = Nasabah
        fields = ['name', 'addres']
        labels = {
            'name': _('Nama'),
            'addres': _('Alamat')
        }
        help_texts = {
            'name': _('Nama nasabah'),
            'addres': _('Alamat nasabah')
        }
        error_messages = {
            'name': {
                'max_length': _('Nama terlalu panjang'),
            },
            'addres': {
                'max_length': _('Alamat terlalu panjang'),
            },
        }


class ItemCreateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price']
        labels = {
            'name': _('Nama'),
            'price': _('Harga'),
        }
        help_texts = {
            'name': _('Nama barang'),
            'price': _('Harga barang'),
        }
        error_messages = {
            'name': {
                'max_length': _('Nama barang terlalu panjang'),
            },
            'price': {
                'required': _('Harus diisi'),
                'min_value': _('Minimal 1'),
            },
        }


class OrderItemCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(OrderItemCreateForm, self).__init__(*args, **kwargs)
        self.fields['item'].queryset = Item.objects.filter(user=user)
    
    class Meta:
        model = OrderItem
        fields = ['item', 'value']
        labels = {
            'item': _('Nama'),
            'value': _('Berat'),
        }
        help_texts = {
            'item': _(''),
            'value': _('Kg'),
        }
        error_messages = {
            'value': {
                'required': _('Harus diisi'),
                'min_value': _('Minimal 0.25'),
            },
        }
