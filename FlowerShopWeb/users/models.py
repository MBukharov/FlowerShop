from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    name = models.CharField(max_length=100, verbose_name="Имя",default='')
    phone = models.CharField(max_length=20, verbose_name="Телефон",default='')
    # add additional fields in here


