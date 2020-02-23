from django.utils.translation import gettext_lazy as _
from django import forms
from core.models import (
    Nasabah,
    Item,
    OrderItem,
    Order
)


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
