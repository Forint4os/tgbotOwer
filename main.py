# main.py
import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from database import init_db
from handlers import user, admin

# Получаем токены из переменных окружения и убираем пробелы
TOKEN = os.getenv("TOKEN")
DEEPIKA_KEY = os.getenv("DEEPIKA_KEY")

TOKEN = TOKEN.strip() if TOKEN else None
DEEPIKA_KEY = DEEPIKA_KEY.strip() if DEEPIKA_KEY else None

if not TOKEN:
    raise ValueError("BOT TOKEN не найден или пустой! Проверьте GitHub Secrets.")
if not DEEPIKA_KEY:
    print("Внимание: DEEPIKA_KEY не установлен. Нейросеть не будет работать.")

async def main():
    # Создание бота и диспетчера
    bot = Bot(token=TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Инициализация базы данных
    init_db()

    # Подключение роутеров
    dp.include_router(user.router)
    dp.include_router(admin.router)

    print("Бот запущен и готов к работе!")

    # Запуск polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())