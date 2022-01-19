from main import bot, dp

from aiogram.types import Message
from config import admin_id


async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id, text='Бот запущен')


# Доставка сообщение(декоратор)
@dp.message_handler()
async def echo(messange: Message):
    text = f"Привет, ты написал: {messange.text}"
    await messange.answer(text=text)