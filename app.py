from mistralai import Mistral

import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.methods import DeleteWebhook
from aiogram.types import Message

# ВСТАВЛЕННЫЕ ДАННЫЕ
mistral_api_key = "qZgGPe8jVwCtbl1G8NCNKjc6PJPFW7R0"  # API ключ Mistral
TOKEN = "7383862092:AAFRbwktHcjJebe79WyhFbxO2jMNwbMGx2k"  # Токен бота

model = "mistral-large-latest"
client = Mistral(api_key=mistral_api_key)

logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN)
dp = Dispatcher()

# ОБРАБОТЧИК КОМАНДЫ СТАРТ
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я - бот с подключенной нейросетью, отправь свой запрос")

# ОБРАБОТЧИК ЛЮБОГО ТЕКСТОВОГО СООБЩЕНИЯ
@dp.message(F.text)
async def filter_messages(message: Message):
    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "system",
                "content": ""
            },
            {
                "role": "user",
                "content": message.text
            }
        ]
    )

    text = chat_response.choices[0].message.content
    await message.answer(text, parse_mode="Markdown")

async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())