from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from config import ADMIN_ID
from database.db import get_tickets, get_ticket, mark_answered, get_stats
from keyboards.admin_kb import admin_menu
from keyboards.tickets_kb import tickets_keyboard

router = Router()

admin_state = {}


# ---------------- LOGIN ----------------
@router.message(F.text.startswith("/admin"))
async def admin_login(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    parts = message.text.split()

    if len(parts) < 2 or parts[1] != "123":
        await message.answer("🔐 /admin 123")
        return

    await message.answer(
        "👨‍💻 <b>Админ панель активирована</b>",
        reply_markup=admin_menu()
    )


# ---------------- TICKETS ----------------
@router.message(F.text == "📋 Тикеты")
async def tickets_list(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    tickets = get_tickets()

    if not tickets:
        await message.answer("📭 тикетов нет")
        return

    await message.answer(
        "📋 <b>Тикеты:</b>",
        reply_markup=tickets_keyboard(tickets)
    )


# ---------------- OPEN TICKET (INLINE) ----------------
@router.callback_query(F.data.startswith("ticket_"))
async def open_ticket(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return

    ticket_id = int(callback.data.split("_")[1])
    ticket = get_ticket(ticket_id)

    if not ticket:
        await callback.answer("Не найдено")
        return

    admin_state[callback.from_user.id] = ticket_id

    await callback.message.answer(
        f"📩 <b>Тикет #{ticket[0]}</b>\n"
        f"👤 @{ticket[2]}\n"
        f"📂 {ticket[3]}\n\n"
        f"💬 {ticket[4]}\n\n"
        f"✍️ Напишите ответ одним сообщением"
    )

    await callback.answer()


# ---------------- ANSWER MESSAGE ----------------
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
        f"📩 <b>Ответ поддержки:</b>\n\n{message.text}"
    )

    mark_answered(ticket_id)

    admin_state[message.from_user.id] = None

    await message.answer("✅ отправлено")
    

# ---------------- STATS ----------------
@router.message(F.text == "📊 Статистика")
async def stats(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    total, by_cat = get_stats()

    text = f"📊 <b>Статистика</b>\n\nВсего тикетов: {total}\n\n"

    for cat, count in by_cat:
        text += f"📂 {cat}: {count}\n"

    await message.answer(text)
