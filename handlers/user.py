import time

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.user_kb import main_menu
from utils.tickets import create_ticket
from config import ADMIN_ID

router = Router()

user_state = {}
spam_limit = {}
receivers = {}

# ---------------- START ----------------
@router.message(F.text == "/start")
async def start(message: Message):
    user_state[message.from_user.id] = None
    receivers[message.from_user.id] = None

    await message.answer(
        "👋 <b>Система активна</b>\n\nВыберите действие:",
        reply_markup=main_menu()
    )


# ---------------- WRITE FLOW ENTRY ----------------
@router.message(F.text == "📩 Написать")
async def choose_receiver(message: Message):
    user_state[message.from_user.id] = "choose_receiver"

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [F"👑 Admin"],
            ["💼 Работа", "💡 Предложения"],
            ["💰 Зарплата", "🤝 Коллаборация"],
            ["⚠️ Ошибки", "📞 Поддержка"],
            ["👤 Личное", "📦 Другое"]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "📨 <b>Выберите тему / получателя:</b>",
        reply_markup=kb
    )


# ---------------- SELECT CATEGORY ----------------
@router.message(F.text.in_([
    "👑 Admin",
    "💼 Работа",
    "💡 Предложения",
    "💰 Зарплата",
    "🤝 Коллаборация",
    "⚠️ Ошибки",
    "📞 Поддержка",
    "👤 Личное",
    "📦 Другое"
]))
async def category_selected(message: Message):
    receivers[message.from_user.id] = message.text
    user_state[message.from_user.id] = "write_message"

    await message.answer(
        "✍️ <b>Напишите сообщение одним текстом:</b>",
        reply_markup=ReplyKeyboardRemove()  # 🔥 КЛАВИАТУРА ИСЧЕЗАЕТ
    )


# ---------------- MAIN FLOW (IMPORTANT FIX) ----------------
@router.message()
async def handler(message: Message):

    uid = message.from_user.id
    text = message.text

    # ---------------- /ADMIN FIX (GLOBAL, ALWAYS WORKS) ----------------
    if text == "/admin":
        await message.answer(
            "👨‍💻 <b>Админ режим активирован</b>",
            reply_markup=main_menu()
        )
        return

    # ---------------- SPAM ----------------
    now = time.time()
    if uid in spam_limit and now - spam_limit[uid] < 2:
        return
    spam_limit[uid] = now

    state = user_state.get(uid)

    # ---------------- SEND MESSAGE ----------------
    if state == "write_message":
        user_state[uid] = None

        receiver = receivers.get(uid, "unknown")

        ticket = create_ticket(
            user_id=uid,
            username=message.from_user.username or "no_username",
            category=receiver,
            text=text
        )

        await message.answer(
            "✅ <b>Сообщение отправлено</b>\n"
            "⏳ Ожидайте ответа",
            reply_markup=main_menu()
        )

        await message.bot.send_message(
            ADMIN_ID,
            f"📩 <b>Новый тикет #{ticket['id']}</b>\n"
            f"👤 @{ticket['username']}\n"
            f"🎯 {ticket['category']}\n\n"
            f"💬 {ticket['text']}"
        )

        return

    # ---------------- DEFAULT (ONLY IF NOT HANDLED) ----------------
    await message.answer(
        "👇 <b>Используйте меню ниже</b>",
        reply_markup=main_menu()
    )
