from aiogram import Router, F
from aiogram.types import Message

from keyboards.user_kb import main_menu

router = Router()

# временное хранение состояния (позже заменим на БД)
user_state = {}

@router.message(F.text == "/start")
async def start(message: Message):
    user_state[message.from_user.id] = None

    await message.answer(
        "👋 <b>Система активна</b>\nВыберите действие:",
        reply_markup=main_menu()
    )


@router.message(F.text == "📩 Написать")
async def write_start(message: Message):
    user_state[message.from_user.id] = "write"

    await message.answer("✍️ Напишите ваше сообщение одним текстом:")


@router.message()
async def handler(message: Message):
    state = user_state.get(message.from_user.id)

    if state == "write":
        user_state[message.from_user.id] = None

        await message.answer(
            "✅ Принято!\n📨 Ваше сообщение отправлено администрации.\n⏳ Ожидайте ответ."
        )

        # тут позже будет отправка админу
        return

    await message.answer("ℹ️ Используйте меню ниже 👇")
