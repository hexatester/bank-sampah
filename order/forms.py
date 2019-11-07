from django.utils.translation import gettext_lazy as _
from django import forms
from core.models import (
    Nasabah,
    Item,
    OrderItem,
    Order
)


class OrderItemCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(OrderItemCreateForm, self).__init__(*args, **kwargs)
        self.fields['item'].queryset = Item.objects.filter(user=user).order_by("name")

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


class OrderSubmitForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['sums']
        label = {
            'sums': _('Tambah'),
        }
        help_texts = {
            'sums': _('Tambahkan ke saldo?'),
        }
