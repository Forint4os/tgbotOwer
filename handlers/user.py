from aiogram import Router, F
from aiogram.types import Message

from keyboards.user_kb import main_menu

router = Router()

user_state = {}

CATEGORIES = {
    "📩 Написать": "write",
    "🆘 Помощь": "help",
    "💼 Работа": "work",
    "💡 Предложения": "offer",
    "💰 Зарплата": "salary",
    "🤝 Коллаборация": "collab",
    "⚠️ Ошибки": "bug",
    "📞 Поддержка": "support",
    "👤 Личное": "private",
    "📦 Другое": "other"
}


@router.message(F.text == "/start")
async def start(message: Message):
    user_state[message.from_user.id] = None

    await message.answer(
        "👋 <b>Система активна</b>\n\nВыберите действие ниже 👇",
        reply_markup=main_menu()
    )


# 🔥 ЛЮБАЯ КНОПКА → режим ввода
@router.message(F.text.in_(list(CATEGORIES.keys())))
async def category_handler(message: Message):
    user_state[message.from_user.id] = CATEGORIES[message.text]

    await message.answer(
        "✍️ <b>Напишите ваше сообщение одним текстом:</b>\n\n"
        "📨 Оно будет отправлено администрации."
    )


@router.message()
async def message_handler(message: Message):
    state = user_state.get(message.from_user.id)

    if state:
        user_state[message.from_user.id] = None

        await message.answer(
            "✅ <b>Сообщение принято</b>\n"
            "📨 Отправлено в обработку\n"
            "⏳ Ожидайте ответ от администрации"
        )
        return

    await message.answer(
        "ℹ️ <b>Используйте кнопки меню ниже</b> 👇"
    )
