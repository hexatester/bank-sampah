from django.db import models


class NasabahQuerySet(models.QuerySet):
    def get_nasabah_by_user(self, user):
        return self.filter(user=user)


class NasabahManager(models.Manager):
    query_set = NasabahQuerySet

    def get_nasabah_by_user(self, user):
        return self.query_set()(user=user)
