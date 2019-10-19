from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.core.validators import MinValueValidator

# Create your models here.


class Nasabah(models.Model):
    name = models.CharField(max_length=64)
    addres = models.TextField(max_length=126, blank=True, null=True)
    balance = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.name)

    def get_absolute_url(self):
        return reverse("core:user", kwargs={
            'pk': self.pk
        })

    def get_delete_url(self):
        return reverse("core:delete_user", kwargs={
            'pk': self.pk
        })

    def get_order_url(self):
        return reverse("core:order", kwargs={
            'pk': self.pk
        })
    
    def get_withdraw_url(self):
        return reverse("core:withdraw", kwargs={
            'pk': self.pk
        })

    def add_balance(self, value: int):
        self.balance += abs(value)
        return self.balance


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
        return reverse("core:item", kwargs={
            'pk': self.pk
        })

    def get_delete_url(self):
        return reverse("core:delete_item", kwargs={
            'pk': self.pk
        })


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    value = models.FloatField(validators=[MinValueValidator(0.25)])
    total = models.PositiveIntegerField(null=True, blank=True)
    nasabah = models.ForeignKey(Nasabah, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return "{} x {}".format(self.item, self.value)

    def get_sum(self):
        return abs(self.item.price*self.value)

    def sum(self):
        self.total = self.get_sum()
        return self.total


class Order(models.Model):
    nasabah = models.ForeignKey(Nasabah, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    total = models.PositiveIntegerField(null=True, blank=True)
    sums = models.BooleanField(default=True)
    ordered = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Order by {}".format(self.nasabah)

    def delete(self, using=None, keep_parents=False):
        self.items.all().delete()
        return super().delete(using=using, keep_parents=keep_parents)
    
    def get_absolute_url(self):
        return reverse("core:order", kwargs={
            'pk': self.nasabah.pk
        })

    def get_delete_url(self):
        return reverse("core:delete_order", kwargs={
            'pk': self.pk
        })
    
    def get_set_url(self):
        return reverse("core:order_set", kwargs={
            'pk': self.pk
        })

    def get_sum(self):
        sums = 0
        for item in self.items.all():
            sums += item.sum()
        self.total = sums
        return abs(sums)
    
    def get_values(self):
        value = 0
        for item in self.items.all():
            value += abs(item.value)
        self.total = value
        return value

