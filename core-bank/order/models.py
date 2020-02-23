from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from item.models import Item
from nasabah.models import Nasabah
# Create your models here.

NULL_BLANK = {
    'blank': True,
    'null': True
}


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    value = models.FloatField(validators=[MinValueValidator(0.25)])
    total = models.PositiveIntegerField(null=True, blank=True)
    nasabah = models.ForeignKey(Nasabah, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return "{} x {} kg".format(self.item, self.value)

    def get_delete_url(self):
        return reverse("order:delete_item", kwargs={
            "pk": self.pk
        })

    def get_sum(self):
        return abs(self.item.price*self.value)

    def get_total(self):
        self.total = self.get_sum()
        self.save()
        return self.total


class Order(models.Model):
    nasabah = models.ForeignKey(Nasabah, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    weigth = models.PositiveIntegerField(**NULL_BLANK)
    total = models.PositiveIntegerField(**NULL_BLANK)
    sums = models.BooleanField(default=False)
    ordered = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Order by {}".format(self.nasabah)

    def delete(self, using=None, keep_parents=False):
        self.items.all().delete()
        return super().delete(using=using, keep_parents=keep_parents)

    def get_absolute_url(self):
        return reverse("order:order", kwargs={
            'pk': self.nasabah.pk
        })

    def get_delete_url(self):
        return reverse("order:delete", kwargs={
            'pk': self.pk
        })

    def get_add_url(self):
        return reverse("order:order", kwargs={
            'pk': self.pk
        })

    def get_set_url(self):
        return reverse("order:set", kwargs={
            'pk': self.pk
        })

    def get_total(self):
        sums = 0
        for item in self.items.all():
            sums += item.get_total()
        self.total = sums
        return abs(sums)

    def get_weigth(self):
        sums = 0
        for item in self.items.all():
            sums += abs(item.value)
        self.weigth = sums
        return sums
