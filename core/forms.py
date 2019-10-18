from django import forms
from .models import (
    Nasabah
)

class UserCreateForm(forms.Form):
    name = forms.CharField(label='Nama', max_length=64)
    addres = forms.CharField(label='Alamat', max_length=126)