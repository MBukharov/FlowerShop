import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand, Message, CallbackQuery
from aiogram.filters import CommandStart, Command
# from config import TG_TOKEN

# Установите ваш токен бота и ID администратора
API_TOKEN = '8049346263:AAE5DNAH1V3DwAUVERWAVOnz5LSaoNheJk4'
ADMIN_CHAT_ID = '291746935'

# Создаем объект бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def chat_id(message: Message):
    await message.answer(f'Ваш chat_id: {message.chat.id}')

async def send_order_to_admin(message):
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=message)



# Основная функция, запускающая бота
async def main():
    # Устанавливаем команды бота (если необходимо)
    await bot.set_my_commands([
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/chat_id", description="Узнать свой chat_id"),
        BotCommand(command="/help", description="Справка"),
    ])

    # Запускаем проверку новых заказов
    # asyncio.create_task(check_new_orders())

    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())