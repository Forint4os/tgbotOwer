from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from config import ADMIN_ID, ADMIN_PASSWORD
from states.user_states import UserStates
from database.db import get_tickets, get_stats, get_ticket_by_id, close_ticket
from keyboards.inline import admin_menu

router = Router()


# ─── Вход в админку ───────────────────────────────────────────────────────────

@router.message(Command("admin"))
async def admin_login(message: Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        # Уже известный админ — сразу показываем меню
        await state.clear()
        await message.answer("👑 Панель администратора:", reply_markup=admin_menu())
    else:
        await state.set_state(UserStates.admin_password)
        await message.answer("🔑 Введите пароль:")


@router.message(UserStates.admin_password)
async def check_password(message: Message, state: FSMContext):
    if message.text == ADMIN_PASSWORD:
        await state.clear()
        await message.answer("✅ Вы вошли в админку", reply_markup=admin_menu())
    else:
        await message.answer("❌ Неверный пароль")


# ─── Тикеты ──────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "tickets")
async def show_tickets(callback: CallbackQuery):
    tickets = get_tickets()

    if not tickets:
        await callback.message.edit_text(
            "📭 Открытых тикетов нет.",
            reply_markup=admin_menu()
        )
        await callback.answer()
        return

    lines = ["📩 <b>Открытые тикеты:</b>\n"]
    for t in tickets:
        ticket_id, user_id, category, msg_text, status = t
        preview = msg_text[:60] + "..." if len(msg_text) > 60 else msg_text
        lines.append(f"<b>#{ticket_id}</b> [{category}]\n💬 {preview}\n/reply {ticket_id} · /close {ticket_id}\n")

    await callback.message.edit_text(
        "\n".join(lines),
        reply_markup=admin_menu(),
        parse_mode="HTML"
    )
    await callback.answer()


# ─── Статистика ───────────────────────────────────────────────────────────────

@router.callback_query(F.data == "stats")
async def show_stats(callback: CallbackQuery):
    stats = get_stats()

    if not stats:
        await callback.message.edit_text("📊 Данных пока нет.", reply_markup=admin_menu())
        await callback.answer()
        return

    lines = ["📊 <b>Статистика по категориям:</b>\n"]
    for cat, count in stats:
        lines.append(f"• {cat}: <b>{count}</b>")

    await callback.message.edit_text(
        "\n".join(lines),
        reply_markup=admin_menu(),
        parse_mode="HTML"
    )
    await callback.answer()


# ─── Ответ на тикет (/reply <id>) ─────────────────────────────────────────────

@router.message(Command("reply"))
async def reply_to_ticket(message: Message, state: FSMContext):
    parts = message.text.split()

    if len(parts) < 2 or not parts[1].isdigit():
        await message.answer("Использование: /reply <номер_тикета>")
        return

    ticket_id = int(parts[1])
    ticket = get_ticket_by_id(ticket_id)

    if not ticket:
        await message.answer(f"❌ Тикет #{ticket_id} не найден.")
        return

    _, user_id, category, ticket_text, status = ticket

    await state.update_data(reply_ticket_id=ticket_id, reply_user_id=user_id)
    await state.set_state(UserStates.admin_reply)

    await message.answer(
        f"✏️ Пишете ответ на тикет <b>#{ticket_id}</b>\n"
        f"📂 Категория: {category}\n"
        f"💬 Вопрос: {ticket_text}\n\n"
        "Напишите ответ пользователю:",
        parse_mode="HTML"
    )


@router.message(UserStates.admin_reply)
async def send_reply(message: Message, state: FSMContext):
    data = await state.get_data()
    ticket_id = data.get("reply_ticket_id")
    user_id = data.get("reply_user_id")

    try:
        await message.bot.send_message(
            user_id,
            f"📬 <b>Ответ по вашему обращению #{ticket_id}:</b>\n\n"
            f"{message.text}",
            parse_mode="HTML"
        )
        await message.answer(f"✅ Ответ отправлен пользователю (тикет #{ticket_id})")
    except Exception as e:
        await message.answer(f"❌ Не удалось отправить: {e}")

    await state.clear()


# ─── Закрытие тикета (/close <id>) ────────────────────────────────────────────

@router.message(Command("close"))
async def close_ticket_cmd(message: Message):
    parts = message.text.split()

    if len(parts) < 2 or not parts[1].isdigit():
        await message.answer("Использование: /close <номер_тикета>")
        return

    ticket_id = int(parts[1])
    ticket = get_ticket_by_id(ticket_id)

    if not ticket:
        await message.answer(f"❌ Тикет #{ticket_id} не найден.")
        return

    close_ticket(ticket_id)
    await message.answer(f"✅ Тикет #{ticket_id} закрыт.")
