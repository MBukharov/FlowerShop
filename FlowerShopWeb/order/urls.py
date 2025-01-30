from django.urls import path, include
from . import views

urlpatterns = [
    path('make_order/', views.make_order, name='make_order'),
    # path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]