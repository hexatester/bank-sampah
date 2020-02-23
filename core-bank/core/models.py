from django.db import models
from django.contrib.auth.models import User
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


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# EOF
