from aiogram import Router, F
from aiogram.types import Message

from keyboards.main_kb import main_keyboard
from utils.stats import add_user, get_stats
from config import ADMIN_ID

router = Router()


@router.message(F.text == "/start")
async def start(message: Message):
    add_user(message.from_user.id)

    await message.answer(
        "👋 <b>Добро пожаловать!</b>\nБот работает стабильно.",
        reply_markup=main_keyboard()
    )


@router.message()
async def all_messages(message: Message):
    add_user(message.from_user.id)

    text = message.text.lower() if message.text else ""

    if text == "📊 статистика":
        await message.answer(f"📊 Пользователей: {get_stats()}")
        return

    if text == "ℹ️ помощь":
        await message.answer("ℹ️ Просто пиши сообщения — я отвечу.")
        return

    if text == "👨‍💻 админ":
        await message.answer("👨‍💻 Админ ID активен.")
        return

    # основной авто-ответ
    await message.answer(
        f"🤖 Я получил сообщение:\n\n<b>{message.text}</b>"
    )
