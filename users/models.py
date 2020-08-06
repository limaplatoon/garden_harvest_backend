from django.contrib.auth.models import AbstractUser
from django.db import models

from api.models import Zone


class User(AbstractUser):
    zip_code = models.CharField(max_length=5, blank=False)
    zone = models.ForeignKey(Zone, related_name="users",
                             on_delete=models.CASCADE)
