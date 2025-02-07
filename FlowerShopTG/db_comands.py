import asyncio
import sqlite3

# Функция для проверки новых заказов
async def check_new_orders(bot, ADMIN_CHAT_ID):
    # Подключение к базе данных
    conn = sqlite3.connect('../FlowerShopWeb/db.sqlite3')
    cursor = conn.cursor()

    # Сохраняем последнее проверенное значение ID заказа
    last_checked_order_id = 11

    while True:
        # Получаем заказы, ID которых больше, чем последний проверенный
        cursor.execute("SELECT ID, delivery_address, phone_number, sum FROM order_order WHERE ID > ?", (last_checked_order_id,))
        new_orders = cursor.fetchall()

        for order in new_orders:
            order_id, delivery_address, phone_number, order_sum = order
            cursor.execute("SELECT name, picture,order_orderproduct.quantity FROM catalog_flower JOIN order_orderproduct "
                           "ON catalog_flower.id = order_orderproduct.product_id WHERE order_orderproduct.order_id = ?",
                           (order_id,))
            products = cursor.fetchall()

            products_name = [x+' '+str(z)+' шт.' for x, y, z in products]

            # Формируем сообщение для администратора
            message = (f"Заказ {order_id}, сумма {order_sum} руб., товары: {products_name}\n"
                       f"Адрес доставки: {delivery_address}, телефон заказчика {phone_number}")

            # Отправляем сообщение администратору
            await bot.send_message(chat_id=ADMIN_CHAT_ID, text=message)

            # Обновляем последнее проверенное значение ID
            last_checked_order_id = order_id

        # Ждем 10 секунд перед следующей проверкой
        await asyncio.sleep(10)

    conn.close()