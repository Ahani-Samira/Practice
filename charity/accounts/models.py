from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    address = models.TextField(blank=True, null=True)
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    gender = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        choices=[
            ('M', 'Male'),
            ('F', 'Female'),
        ])
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username
