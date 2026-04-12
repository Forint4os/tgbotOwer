from aiogram import Router, F
from aiogram.types import Message

from database.db import get_tickets, get_stats

router = Router()


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
            category = item[0]
            count = item[1]
            text += f"• {category}: {count}\n"

    await message.answer(text)


@router.message(F.text == "📩 Тикеты")
async def tickets(message: Message):

    tickets = get_tickets()

    if not tickets:
        await message.answer("📭 Тикетов нет")
        return

    text = "📩 <b>Последние тикеты:</b>\n\n"

    for t in tickets[:10]:
        text += (
            f"🆔 {t[0]}\n"
            f"👤 {t[1]}\n"
            f"📂 {t[3]}\n"
            f"💬 {t[4]}\n"
            f"────────────\n"
        )

    await message.answer(text)
