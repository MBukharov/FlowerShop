from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
]