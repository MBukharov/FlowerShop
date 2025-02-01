from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db import transaction
from catalog.models import Cart, CartItem
from .models import Order, OrderProduct
from .forms import OrderForm
from django.utils import timezone
from django.contrib import messages
from FlowerShopTG_bot.tg_bot_for_admin import send_order_to_admin
import asyncio
from multiprocessing import Process


# Create your views here.
@login_required
def make_order(request):
    user = request.user
    order_form = OrderForm(request.POST)
    if request.method == 'POST':
        # Проверяем, что форма валидна
        if not order_form.is_valid():
            raise ValueError("Order form is not valid")

        # Получаем корзину пользователя
        cart = get_object_or_404(Cart, user=user)
        cart_items = CartItem.objects.filter(cart=cart)

        # Проверяем, что в корзине есть товары
        if not cart_items.exists():
            raise ValueError("Cart is empty")

        # Начинаем транзакцию, чтобы гарантировать целостность данных
        with transaction.atomic():
            # Создаем заказ
            order = Order.objects.create(
                user=user,
                delivery_address=order_form.cleaned_data['delivery_address'],
                phone_number=order_form.cleaned_data['phone_number'],
                sum = sum(item.product.price * item.quantity for item in cart.items.all()),
                status='СБОРКА',  # или другой начальный статус
                date=timezone.now()
            )

            # Создаем записи для каждого товара в заказе
            for item in cart_items:
                OrderProduct.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity
                )
                # print(f"{item.product.name} x {item.quantity} for Order {order.id}")

            products_name = [item.product.name + ' ' + str(item.quantity) + ' шт.' for item in cart_items]
            message = (f"Заказ {order.id}, сумма {order.sum} руб., товары: {products_name}\n"
                      f"Адрес доставки: {order.delivery_address}, телефон заказчика {order.phone_number}")

            send_telegram_message(message)


            # Очищаем корзину
            cart_items.delete()

        # Добавляем сообщение для пользователя
        messages.success(request, "Вы успешно сделали заказ. Менеджер свяжется с вами в ближайшее время для подтверждения заказа.")


        return redirect('cart_detail')


def send_telegram_message(message_text):
    # Создаем новый event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(send_order_to_admin(message_text))
    finally:
        loop.close()
