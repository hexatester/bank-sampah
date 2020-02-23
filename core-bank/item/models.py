from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

nulls = {
    'blank': True,
    'null': True
}

class Item(models.Model):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
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

