from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import CustomUserRegisterForm, CustomUserLoginForm
from django.contrib.auth import logout
from django.contrib import messages
from .forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from order.models import Order
from django.db.models import Q
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def register(request):
    if request.method == 'POST':
        form = CustomUserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = CustomUserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('catalog')
    else:
        form = CustomUserLoginForm()
    return render(request, 'users/login.html', {'form': form})

def home(request):
    return render(request, 'users/home.html')

def logout_view(request):
    logout(request)
    return redirect('catalog')


@login_required
def account_data(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваши данные были успешно обновлены!')
            return redirect('account')  # Перенаправление на ту же страницу
    else:
        form = UserChangeForm(instance=request.user)

    return render(request, 'users/account.html', {'form': form})

@login_required
def my_orders(request):
    user = request.user
    my_orders = Order.objects.filter(user=user)

    return render(request, 'users/my_orders.html', {'my_orders': my_orders})

def users_orders(request):
    if request.user.is_superuser:
        orders_ready_or_cancelled = Order.objects.filter(
            Q(status="ВЫПОЛНЕН") | Q(status="ОТМЕНЕН")
        )
        orders_in_work = Order.objects.filter(
            Q(status="СБОРКА") | Q(status="В ПУТИ")
        )

        return render(request, 'users/orders_for_admin.html',
                  {'orders_ready_or_cancelled': orders_ready_or_cancelled,
                   'orders_in_work':orders_in_work})

    else:
        user = request.user
        my_orders = Order.objects.filter(user=user)

        return render(request, 'users/my_orders.html', {'my_orders': my_orders})


@csrf_exempt  # Используйте с осторожностью, убедитесь в безопасности
def update_order_status(request, order_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_status = data.get('status')

            # Проверяем, является ли новый статус допустимым
            if new_status not in ["СБОРКА", "В ПУТИ", "ВЫПОЛНЕН", "ОТМЕНЕН"]:
                return JsonResponse({'success': False, 'error': 'Недопустимый статус'})

            # Обновляем статус заказа
            order = Order.objects.get(id=order_id)
            order.status = new_status
            order.save()

            return JsonResponse({'success': True})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Заказ не найден'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Неподдерживаемый метод'})
