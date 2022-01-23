from django.conf import settings
from django.db   import models

from core.models import TimeStampModel


class Profile(TimeStampModel):
    user    = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)