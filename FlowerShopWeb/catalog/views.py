from django.shortcuts import render, redirect
from .models import Flower, Cart, CartItem
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
# Create your views here.

def catalog(request):
    flowers = Flower.objects.all()
    return render(request, 'catalog/catalog.html', {'flowers': flowers})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Flower, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('catalog')

@login_required
def remove_from_cart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    cart_item.delete()
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart = get_object_or_404(Cart, user=request.user)
    total_sum = sum(item.product.price * item.quantity for item in cart.items.all())
    return render(request, 'catalog/cart_detail.html', {'cart': cart, 'total_sum': total_sum})

