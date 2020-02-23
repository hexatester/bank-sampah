from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

NULL_BLANK = {
    'blank': True,
    'null': True
}

class Nasabah(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=64)
    addres = models.TextField(max_length=126, **NULL_BLANK)
    balance = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.name)

    def get_absolute_url(self):
        return reverse("nasabah:view", kwargs={
            'pk': self.pk
        })

    def get_delete_url(self):
        return reverse("nasabah:delete", kwargs={
            'pk': self.pk
        })

    def get_order_url(self):
        return reverse("order:order", kwargs={
            'pk': self.pk
        })

    def get_withdraw_url(self):
        return reverse("nasabah:withdraw", kwargs={
            'pk': self.pk
        })

    def add_balance(self, value: int):
        self.balance += abs(value)
        return self.balance
