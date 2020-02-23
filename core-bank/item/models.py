from django.db import models
from django.conf import settings
from django.shortcuts import reverse


# Create your models here.

nulls = {
    'blank': True,
    'null': True
}


class Item(models.Model):
    name = models.CharField(
        verbose_name='Nama barang', max_length=64)
    user = models.ForeignKey(
        verbose_name='Pengguna',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    price = models.PositiveIntegerField(
        verbose_name='Harga')
    timestamp = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(self.name, self.price)

    def get_absolute_url(self):
        return reverse("item:view", kwargs={
            'pk': self.pk
        })

    def get_delete_url(self):
        return reverse("item:delete", kwargs={
            'pk': self.pk
        })
