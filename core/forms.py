from django import forms
from .models import (
    Nasabah,
    Item
)


class NasabahCreateForm(forms.ModelForm):
    class Meta:
        model = Nasabah
        fields = ['name', 'addres']


class ItemCreateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price']
