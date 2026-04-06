from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("admin"))
async def admin_handler(message: types.Message):
    await message.answer("Админ режим включен ✅")
