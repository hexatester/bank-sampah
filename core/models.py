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

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.PositiveIntegerField(default=0)
    weight = models.PositiveIntegerField(default=0)
    timezone = models.CharField(default="Asia/Jakarta", max_length=64)
    timestamp = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def tz(self):
        return self.timezone

    def add_balance(self, value: int):
        if value > 0:
            self.balance += value
            return True
        return False

    def add_weight(self, value: int):
        if value > 0:
            self.balance += value
            return True
        return False


class Nasabah(models.Model):
    name = models.CharField(max_length=64)
    addres = models.TextField(max_length=126, **nulls)
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    weigth = models.PositiveIntegerField(**nulls)
    total = models.PositiveIntegerField(**nulls)
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

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# EOF

