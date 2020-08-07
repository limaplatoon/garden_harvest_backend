from django.contrib.auth.models import AbstractUser
from django.db import models


class ZipZone(models.Model):
    zip_code = models.CharField(max_length=5, primary_key=True)
    zone = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return f'{self.zip_code} (zone {self.zone})'


class User(AbstractUser):
    zip_code = models.CharField(max_length=5, blank=False)
    zone = models.ForeignKey('api.Zone', related_name="users",
                             on_delete=models.CASCADE)
