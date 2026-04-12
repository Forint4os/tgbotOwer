from aiogram import Router, F
from aiogram.types import Message

from database.db import get_tickets, get_stats

router = Router()


# ---------------- STATS ----------------
@router.message(F.text == "📊 Статистика")
async def stats(message: Message):

    data = get_stats()

    total = data["total"]
    by_cat = data["by_category"]

    text = "📊 <b>Статистика</b>\n\n"
    text += f"Всего тикетов: <b>{total}</b>\n\n"
    text += "По категориям:\n"

    if not by_cat:
        text += "— нет данных"
    else:
        for item in by_cat:
            text += f"• {item[0]}: {item[1]}\n"

    await message.answer(text)


# ---------------- TICKETS ----------------
@router.message(F.text == "📩 Тикеты")
async def tickets(message: Message):

    data = get_tickets()

    if not data:
        await message.answer("📭 Тикетов нет")
        return

    text = "📩 <b>Последние тикеты</b>\n\n"

    for t in data[:10]:
        text += (
            f"🆔 {t[0]}\n"
            f"👤 {t[1]}\n"
            f"📂 {t[3]}\n"
            f"💬 {t[4]}\n"
            f"────────────\n"
        )

    await message.answer(text)
