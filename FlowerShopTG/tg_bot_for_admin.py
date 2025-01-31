import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand, Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from config import TG_TOKEN

# Установите ваш токен бота и ID администратора
API_TOKEN = TG_TOKEN
ADMIN_CHAT_ID = '291746935'

# Создаем объект бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Функция для проверки новых заказов
async def check_new_orders():
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


@dp.message(CommandStart())
async def chat_id(message: Message):
    await message.answer(f'Ваш chat_id: {message.chat.id}')



# Основная функция, запускающая бота
async def main():
    # Устанавливаем команды бота (если необходимо)
    await bot.set_my_commands([
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/chat_id", description="Узанть свой chat_id"),
        BotCommand(command="/help", description="Справка"),
    ])

    # Запускаем проверку новых заказов
    asyncio.create_task(check_new_orders())

    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())