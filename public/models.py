from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Profile(models.Model):
    """
    Extra information that isn't accessed as much as the User model.
    This example code uses the Client + Server integration method because
    we want to remember a customer_id from Stripe with our own server.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class MagazineTitles(models.Model):
    """
    These are simply magazine titles that a user can select
    """
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=250, unique=True)


class DistributedMagazine(models.Model):
    """
    These are the magazines that we distribute.

    Assume that a completely different service distributes
    these magazines. Our only concern is the financial component.
    """
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    magazine = models.ForeignKey(MagazineTitles, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    expires = models.DateTimeField()
