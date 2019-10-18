from django.db import models
from django.conf import settings
from django.shortcuts import reverse

# Create your models here.


class Nasabah(models.Model):
    name = models.CharField(max_length=64)
    addres = models.TextField(max_length=126, blank=True, null=True)
    balance = models.PositiveIntegerField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.name)
    
    def get_absolute_url(self):
        return reverse("core:user", kwargs={
            'pk': self.pk
        })
    
    def get_order_url(self):
        return reverse("core:order", kwargs={
            'pk': self.pk
        })



class Item(models.Model):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(self.name, self.price)
    
    def get_absolute_url(self):
        return reverse("core:item", kwargs={
            'pk': self.pk
        })


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField()
    nasabah = models.ForeignKey(Nasabah, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return "{} x {}".format(self.item, self.value)
    
    def get_sum(self):
        return self.item.price*self.value


class Order(models.Model):
    nasabah = models.ForeignKey(Nasabah, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem, null=True)
    ordered = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Order by {}".format(self.nasabah)