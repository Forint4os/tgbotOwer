import time

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

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
        "👋 <b>Система активна</b>\n\nВыберите действие 👇",
        reply_markup=main_menu()
    )


# ---------------- OPEN WRITE FLOW ----------------
@router.message(F.text == "📩 Написать")
async def choose_receiver(message: Message):
    user_state[message.from_user.id] = "choose_receiver"

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="👑 Admin 1"),
                KeyboardButton(text="👑 Admin 2"),
            ],
            [
                KeyboardButton(text="👤 Slot 1"),
                KeyboardButton(text="👤 Slot 2"),
            ],
            [
                KeyboardButton(text="👤 Slot 3"),
                KeyboardButton(text="👤 Slot 4"),
            ],
        ],
        resize_keyboard=True
    )

    await message.answer(
        "📨 <b>Выберите получателя:</b>",
        reply_markup=kb
    )


# ---------------- RECEIVER SELECT ----------------
@router.message(F.text.in_([
    "👑 Admin 1", "👑 Admin 2",
    "👤 Slot 1", "👤 Slot 2",
    "👤 Slot 3", "👤 Slot 4"
]))
async def receiver_selected(message: Message):
    receivers[message.from_user.id] = message.text
    user_state[message.from_user.id] = "write_message"

    await message.answer(
        "✍️ <b>Напишите сообщение одним текстом:</b>",
        reply_markup=main_menu()
    )


# ---------------- MAIN HANDLER ----------------
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

    # ---------------- WRITE MESSAGE FLOW ----------------
    if state == "write_message":
        user_state[uid] = None

        receiver = receivers.get(uid, "unknown")

        ticket = create_ticket(
            user_id=uid,
            username=message.from_user.username or "no_username",
            category=receiver,
            text=message.text
        )

        await message.answer(
            "✅ <b>Сообщение отправлено</b>\n"
            "📨 Принято системой\n"
            "⏳ Ожидайте ответа"
        )

        await message.bot.send_message(
            ADMIN_ID,
            f"📩 <b>Новый тикет #{ticket['id']}</b>\n"
            f"👤 @{ticket['username']}\n"
            f"🎯 Получатель: {ticket['category']}\n\n"
            f"💬 {ticket['text']}"
        )

        return

    # ---------------- DEFAULT ----------------
    await message.answer(
        "ℹ️ <b>Используйте меню ниже</b>",
        reply_markup=main_menu()
    )
