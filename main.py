from aiogram import Bot, Dispatcher, executor
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN
from database import init_db
from handlers import user, admin

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Инициализация БД
init_db()

# Регистрация хендлеров
dp.message.register(user.start_handler, commands=["start"])
# Здесь нужно добавить регистрацию всех остальных хендлеров из user.py и admin.py

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
