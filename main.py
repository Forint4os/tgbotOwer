# main.py
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN
from database import init_db
from handlers import user, admin

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