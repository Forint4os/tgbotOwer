from aiogram import Router, types
from aiogram.filters import Command

# ОБЯЗАТЕЛЬНО создаём router
router = Router()

# Пример команды /start
@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Привет! Бот работает ✅")
