from django.utils.translation import gettext_lazy as _
from django import forms
from nasabah.models import Nasabah


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



class WithdrawForm(forms.Form):
    value = forms.IntegerField(min_value=100)

