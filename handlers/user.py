from aiogram import Router, F
from aiogram.types import Message

from keyboards.user_kb import main_menu
from utils.tickets import create_ticket
from config import ADMIN_ID

router = Router()

# простое хранение состояния (позже заменим на БД)
user_state = {}

# категории (кнопки → тикеты)
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


# ---------------- START ----------------
@router.message(F.text == "/start")
async def start(message: Message):
    user_state[message.from_user.id] = None

    await message.answer(
        "👋 <b>Система активна</b>\n\n"
        "Выберите нужный раздел ниже 👇",
        reply_markup=main_menu()
    )


# ---------------- CATEGORY SELECT ----------------
@router.message(F.text.in_(list(CATEGORIES.keys())))
async def category_handler(message: Message):
    user_state[message.from_user.id] = CATEGORIES[message.text]

    await message.answer(
        "✍️ <b>Напишите ваше сообщение одним текстом:</b>\n\n"
        "📨 Оно будет отправлено администрации."
    )


# ---------------- MAIN MESSAGE HANDLER ----------------
@router.message()
async def message_handler(message: Message):
    state = user_state.get(message.from_user.id)

    # если пользователь в режиме отправки тикета
    if state:
        user_state[message.from_user.id] = None

        ticket = create_ticket(
            user_id=message.from_user.id,
            username=message.from_user.username or "no_username",
            category=state,
            text=message.text
        )

        await message.answer(
            "✅ <b>Сообщение принято</b>\n\n"
            "📨 Отправлено администрации\n"
            "⏳ Ожидайте ответ"
        )

        # отправка админу
        await message.bot.send_message(
            ADMIN_ID,
            f"📩 <b>Новый тикет #{ticket['id']}</b>\n"
            f"👤 @{ticket['username']}\n"
            f"📂 Категория: <b>{ticket['category']}</b>\n\n"
            f"💬 {ticket['text']}"
        )

        return

    # если просто написал что-то без режима
    await message.answer(
        "ℹ️ <b>Используйте меню ниже</b> 👇",
        reply_markup=main_menu()
    )
