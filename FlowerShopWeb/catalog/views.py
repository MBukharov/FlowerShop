from django.shortcuts import render, redirect

# Create your views here.

def catalog(request):
    return render(request, 'catalog/catalog.html')