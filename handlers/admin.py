from aiogram import Router, F
from aiogram.types import Message

from utils.tickets import get_tickets, get_ticket_by_id

router = Router()

ADMIN_ID = 5476359789
ADMIN_PASSWORD = "123"

admin_logged = set()


@router.message(F.text.startswith("/admin"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    parts = message.text.split()

    if len(parts) < 2:
        await message.answer("🔐 /admin 123")
        return

    if parts[1] != ADMIN_PASSWORD:
        await message.answer("❌ неверный пароль")
        return

    admin_logged.add(message.from_user.id)

    tickets = get_tickets()

    if not tickets:
        await message.answer("📭 тикетов нет")
        return

    text = "📋 <b>Список тикетов:</b>\n\n"

    for t in tickets[-10:]:
        status = "❌" if not t["answered"] else "✅"
        text += f"{status} #{t['id']} | {t['category']} | @{t['username']}\n"

    text += "\nОтвет: /reply ID текст"

    await message.answer(text)


@router.message(F.text.startswith("/reply"))
async def reply(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    parts = message.text.split(maxsplit=2)

    if len(parts) < 3:
        await message.answer("❌ /reply ID текст")
        return

    tid = int(parts[1])
    text = parts[2]

    ticket = get_ticket_by_id(tid)

    if not ticket:
        await message.answer("❌ тикет не найден")
        return

    await message.bot.send_message(
        ticket["user_id"],
        f"📩 <b>Ответ администратора:</b>\n\n{text}"
    )

    ticket["answered"] = True

    await message.answer("✅ ответ отправлен")
