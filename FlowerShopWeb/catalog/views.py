from django.shortcuts import render, redirect
from .models import Flower
# Create your views here.

def catalog(request):
    flowers = Flower.objects.all()
    return render(request, 'catalog/catalog.html', {'flowers': flowers})