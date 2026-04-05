# main.py
import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from database import init_db
from handlers import user, admin

# Получаем токены из переменных окружения (для GitHub Actions)
TOKEN = os.getenv("TOKEN")
DEEPIKA_KEY = os.getenv("DEEPIKA_KEY")

if not TOKEN:
    raise ValueError("BOT TOKEN не найден. Установите переменную окружения TOKEN.")
if not DEEPIKA_KEY:
    print("Внимание: DEEPIKA_KEY не установлен. Нейросеть не будет работать.")

async def main():
    # Создаём бота и диспетчер
    bot = Bot(token=TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Инициализация базы данных
    init_db()

    # Подключение роутеров
    dp.include_router(user.router)
    dp.include_router(admin.router)

    print("Бот запущен и готов к работе!")

    # Асинхронный запуск polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())