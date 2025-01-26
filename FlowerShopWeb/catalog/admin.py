from django.contrib import admin

# Register your models here.

from .models import Flower

admin.site.register(Flower)