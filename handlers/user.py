import time

from aiogram import Router, F
from aiogram.types import Message

from keyboards.user_kb import main_menu
from utils.tickets import create_ticket
from config import ADMIN_ID

router = Router()

user_state = {}
spam_limit = {}

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
        "👋 <b>Система активна</b>\n\nВыберите действие 👇",
        reply_markup=main_menu()
    )


@router.message(F.text.in_(list(CATEGORIES.keys())))
async def category(message: Message):
    user_state[message.from_user.id] = CATEGORIES[message.text]

    await message.answer(
        "✍️ Напишите сообщение одним текстом:"
    )


@router.message()
async def handler(message: Message):

    # ---------------- SPAM PROTECTION ----------------
    now = time.time()
    uid = message.from_user.id

    if uid in spam_limit:
        if now - spam_limit[uid] < 2:
            return

    spam_limit[uid] = now

    state = user_state.get(uid)

    if state:
        user_state[uid] = None

        ticket = create_ticket(
            user_id=uid,
            username=message.from_user.username or "no_username",
            category=state,
            text=message.text
        )

        await message.answer(
            "✅ <b>Принято</b>\n📨 Отправлено администрации"
        )

        await message.bot.send_message(
            ADMIN_ID,
            f"📩 Новый тикет #{ticket['id']}\n"
            f"👤 @{ticket['username']}\n"
            f"📂 {ticket['category']}\n\n"
            f"{ticket['text']}"
        )

        return

    await message.answer("ℹ️ Используйте меню 👇", reply_markup=main_menu())
