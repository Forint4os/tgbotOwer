from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import ADMIN_ID
from states import AdminFlow
from database.db import get_tickets, get_ticket, mark_answered, get_stats
from keyboards.admin_kb import admin_menu, tickets_page, ticket_actions

router = Router()


# ---------------- ADMIN ENTRY ----------------
@router.message(F.text == "/admin")
async def admin_entry(message: Message, state: FSMContext):

    if message.from_user.id != ADMIN_ID:
        return

    await state.set_state(AdminFlow.menu)

    await message.answer(
        "👨‍💻 <b>CRM Панель</b>",
        reply_markup=admin_menu()
    )


# ---------------- TICKETS PAGINATION ----------------
@router.callback_query(F.data.startswith("adm_tickets:"))
async def tickets(callback: CallbackQuery):

    page = int(callback.data.split(":")[1])
    tickets = get_tickets()

    if not tickets:
        await callback.message.edit_text("📭 Нет тикетов")
        await callback.answer()
        return

    per_page = 5
    start = page * per_page
    end = start + per_page

    text = f"📋 <b>Тикеты</b> (стр. {page + 1})\n\n"

    for t in tickets[start:end]:
        status = "❌" if t[5] == 0 else "✅"
        text += f"{status} #{t[0]} | @{t[2]} | {t[3]}\n"

    kb = tickets_page(page, tickets, per_page)

    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()


# ---------------- OPEN TICKET ----------------
@router.callback_query(F.data.startswith("adm_open:"))
async def open_ticket(callback: CallbackQuery, state: FSMContext):

    ticket_id = int(callback.data.split(":")[1])
    ticket = get_ticket(ticket_id)

    if not ticket:
        await callback.answer("не найден")
        return

    await state.update_data(ticket_id=ticket_id)
    await state.set_state(AdminFlow.viewing_ticket)

    await callback.message.edit_text(
        f"📩 <b>Тикет #{ticket[0]}</b>\n\n"
        f"👤 @{ticket[2]}\n"
        f"📂 {ticket[3]}\n\n"
        f"💬 {ticket[4]}",
        reply_markup=ticket_actions(ticket_id)
    )

    await callback.answer()


# ---------------- REPLY MODE ----------------
@router.callback_query(F.data.startswith("adm_reply:"))
async def reply_mode(callback: CallbackQuery, state: FSMContext):

    ticket_id = int(callback.data.split(":")[1])

    await state.update_data(ticket_id=ticket_id)
    await state.set_state(AdminFlow.replying)

    await callback.message.answer("✍️ Напишите ответ одним сообщением")
    await callback.answer()


# ---------------- SEND REPLY ----------------
@router.message(AdminFlow.replying)
async def send_reply(message: Message, state: FSMContext):

    data = await state.get_data()
    ticket_id = data.get("ticket_id")

    ticket = get_ticket(ticket_id)

    if not ticket:
        await message.answer("❌ тикет не найден")
        return

    await message.bot.send_message(
        ticket[1],
        f"📩 <b>Ответ поддержки:</b>\n\n{message.text}"
    )

    mark_answered(ticket_id)

    await message.answer("✅ отправлено")

    await state.set_state(AdminFlow.menu)


# ---------------- CLOSE TICKET ----------------
@router.callback_query(F.data.startswith("adm_close:"))
async def close_ticket(callback: CallbackQuery):

    ticket_id = int(callback.data.split(":")[1])
    mark_answered(ticket_id)

    await callback.answer("закрыто")


# ---------------- STATS ----------------
@router.callback_query(F.data == "adm_stats")
async def stats(callback: CallbackQuery):

    total, by_cat = get_stats()

    text = "📊 <b>Статистика CRM</b>\n\n"
    text += f"📌 Всего: {total}\n\n"

    for c, n in by_cat:
        text += f"📂 {c}: {n}\n"

    await callback.message.edit_text(text)
    await callback.answer()


# ---------------- FIND TICKET ----------------
@router.message(F.text.startswith("/find"))
async def find_ticket(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    try:
        ticket_id = int(message.text.split()[1])
    except:
        await message.answer("❌ пример: /find 12")
        return

    ticket = get_ticket(ticket_id)

    if not ticket:
        await message.answer("❌ не найден")
        return

    await message.answer(
        f"📩 <b>Тикет #{ticket[0]}</b>\n\n"
        f"👤 @{ticket[2]}\n"
        f"📂 {ticket[3]}\n\n"
        f"💬 {ticket[4]}"
    )


# ---------------- BACK ----------------
@router.callback_query(F.data == "adm_back")
async def back(callback: CallbackQuery, state: FSMContext):

    await state.set_state(AdminFlow.menu)

    await callback.message.edit_text(
        "👨‍💻 <b>CRM Панель</b>",
        reply_markup=admin_menu()
    )

    await callback.answer()

    await callback.answer()
