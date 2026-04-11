from aiogram import Router, F
from aiogram.types import Message

from config import ADMIN_ID
from database.db import get_tickets, get_ticket, mark_answered
from keyboards.admin_kb import admin_menu

router = Router()

admin_session = set()


# ---------------- LOGIN ----------------
@router.message(F.text.startswith("/admin"))
async def admin_login(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    parts = message.text.split()

    if len(parts) < 2 or parts[1] != "123":
        await message.answer("🔐 /admin 123")
        return

    admin_session.add(message.from_user.id)

    await message.answer(
        "👨‍💻 Админ панель активирована",
        reply_markup=admin_menu()
    )


# ---------------- TICKETS LIST ----------------
@router.message(F.text == "📋 Тикеты")
async def tickets_list(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    tickets = get_tickets()

    if not tickets:
        await message.answer("📭 тикетов нет")
        return

    text = "📋 <b>Последние тикеты:</b>\n\n"

    for t in tickets:
        status = "❌" if t[5] == 0 else "✅"
        text += f"{status} #{t[0]} | {t[3]} | @{t[2]}\n"

    text += "\n👉 Напиши: open ID (например open 3)"

    await message.answer(text)


# ---------------- OPEN TICKET ----------------
@router.message(F.text.startswith("open"))
async def open_ticket(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    parts = message.text.split()

    if len(parts) < 2:
        await message.answer("❌ open ID")
        return

    ticket = get_ticket(int(parts[1]))

    if not ticket:
        await message.answer("❌ не найден")
        return

    await message.answer(
        f"📩 <b>Тикет #{ticket[0]}</b>\n"
        f"👤 @{ticket[2]}\n"
        f"📂 {ticket[3]}\n\n"
        f"💬 {ticket[4]}\n\n"
        f"✍️ Ответь командой:\nreply {ticket[0]} текст"
    )


# ---------------- REPLY ----------------
@router.message(F.text.startswith("reply"))
async def reply_ticket(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    parts = message.text.split(maxsplit=2)

    if len(parts) < 3:
        await message.answer("❌ reply ID текст")
        return

    ticket_id = int(parts[1])
    text = parts[2]

    ticket = get_ticket(ticket_id)

    if not ticket:
        await message.answer("❌ не найден")
        return

    await message.bot.send_message(
        ticket[1],
        f"📩 <b>Ответ администратора:</b>\n\n{text}"
    )

    mark_answered(ticket_id)

    await message.answer("✅ отправлено")
