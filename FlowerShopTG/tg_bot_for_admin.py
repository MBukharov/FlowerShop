import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand, Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from config import TG_TOKEN
import db_comands as db

# Установите ваш токен бота и ID администратора
API_TOKEN = TG_TOKEN
ADMIN_CHAT_ID = '291746935'

# Создаем объект бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher()




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
    asyncio.create_task(db.check_new_orders(bot,ADMIN_CHAT_ID))

    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())