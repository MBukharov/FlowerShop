from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('account/', views.account_data, name='account'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('users_orders/', views.users_orders, name='users_orders'),
    path('update-order-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
]