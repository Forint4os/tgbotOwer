from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

router = Router()

@router.message(F.text == "/start")
async def start_handler(message: Message):

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📩 Написать админу"), KeyboardButton(text="ℹ️ Помощь")],
            [KeyboardButton(text="📊 Статистика")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "👋 Привет! Бот запущен и работает.",
        reply_markup=kb
    )
