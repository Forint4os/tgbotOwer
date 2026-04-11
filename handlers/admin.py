from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from config import ADMIN_ID
from database.db import get_tickets, get_ticket, mark_answered, get_stats
from keyboards.admin_kb import admin_menu
from keyboards.tickets_kb import tickets_keyboard
from handlers.user import user_state

router = Router()

admin_state = {}


# ---------------- ADMIN LOGIN ----------------
@router.message(F.text.startswith("/admin"))
async def admin_login(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    user_state[message.from_user.id] = None  # сброс user flow

    await message.answer(
        "👨‍💻 <b>Админ панель активирована</b>",
        reply_markup=admin_menu()
    )


# ---------------- TICKETS LIST ----------------
@router.message(F.text == "📋 Тикеты")
async def tickets_list(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    tickets = get_tickets()

    if not tickets:
        await message.answer("📭 Тикетов нет")
        return

    await message.answer(
        "📋 <b>Список тикетов:</b>",
        reply_markup=tickets_keyboard(tickets)
    )


# ---------------- OPEN TICKET ----------------
@router.callback_query(F.data.startswith("ticket_"))
async def open_ticket(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return

    ticket_id = int(callback.data.split("_")[1])
    ticket = get_ticket(ticket_id)

    if not ticket:
        await callback.answer("❌ Не найден")
        return

    admin_state[callback.from_user.id] = ticket_id

    await callback.message.answer(
        f"📩 <b>Тикет #{ticket[0]}</b>\n\n"
        f"👤 @{ticket[2]}\n"
        f"🎯 {ticket[3]}\n\n"
        f"💬 {ticket[4]}\n\n"
        f"✍️ Напишите ответ одним сообщением"
    )

    await callback.answer()


# ---------------- ADMIN REPLY ----------------
@router.message()
async def admin_reply(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    ticket_id = admin_state.get(message.from_user.id)

    if not ticket_id:
        return

    ticket = get_ticket(ticket_id)

    if not ticket:
        await message.answer("❌ тикет не найден")
        return

    await message.bot.send_message(
        ticket[1],
        f"📩 <b>Ответ администратора:</b>\n\n{message.text}"
    )

    mark_answered(ticket_id)

    admin_state[message.from_user.id] = None

    await message.answer("✅ Ответ отправлен")


# ---------------- STATISTICS ----------------
@router.message(F.text == "📊 Статистика")
async def stats(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    total, by_cat = get_stats()

    text = "📊 <b>Статистика системы</b>\n\n"
    text += f"📌 Всего тикетов: {total}\n\n"

    for cat, count in by_cat:
        text += f"📂 {cat}: {count}\n"

    await message.answer(text)
