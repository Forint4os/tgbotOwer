import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import user, admin
from config import TOKEN

async def main():
    # Создаем бота и диспетчер
    bot = Bot(token=TOKEN, parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())

    # Подключаем маршруты
    dp.include_router(user.router)
    dp.include_router(admin.router)

    print("🤖 Бот запущен!")
    # Запуск polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())