from mistralai.client import Mistral
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F

# 🔑 Твои ключи
MISTRAL_API_KEY = "mst_api_c9b21cfb8c47b194b83649df9872ec68b5e80c49"  # API ключ из фото
BOT_TOKEN = "6997394593:AAHe1G0VmfTW2uOHUAvIfmksh-Wr3VpKKSA"           # Токен Telegram-бота

# 🤖 Настройка клиента Mistral
model = "mistral-large-latest"
client = Mistral(api_key=MISTRAL_API_KEY)

# 📜 История сообщений
chat_history = {}

# ⚙️ Настройка логов
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Я бот с памятью на базе нейросети Mistral. Напиши что-нибудь!")

# Обработка сообщений
@dp.message(F.text)
async def handle_message(message: Message):
    chat_id = message.chat.id

    # Если история чата не существует, создаём
    if chat_id not in chat_history:
        chat_history[chat_id] = [
            {
                "role": "system",
                "content": "Ты полезный ассистент. Отвечай кратко и понятно."
            }
        ]

    # Добавляем сообщение пользователя
    chat_history[chat_id].append({
        "role": "user",
        "content": message.text
    })

    # Получаем ответ от Mistral
    response = client.chat(
        model=model,
        messages=chat_history[chat_id]
    )

    response_text = response.choices[0].message.content

    # Добавляем ответ ассистента
    chat_history[chat_id].append({
        "role": "assistant",
        "content": response_text
    })

    # Сокращаем историю до 10 сообщений + system
    if len(chat_history[chat_id]) > 10:
        chat_history[chat_id] = [chat_history[chat_id][0]] + chat_history[chat_id][-9:]

    # Отправляем ответ
    await message.answer(response_text)

# Запуск бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
