from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import OWNER_ID
from database.db import get_tickets

router = Router()

class AdminStates(StatesGroup):
    password = State()

def admin_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Статистика", callback_data="stats")],
        [InlineKeyboardButton(text="📩 Тикеты", callback_data="tickets")]
    ])

# ================= LOGIN =================
@router.message(F.text == "/admin")
async def admin_login(message: Message, state: FSMContext):
    await state.set_state(AdminStates.password)
    await message.answer("🔐 Введите пароль:")

@router.message(AdminStates.password)
async def check_pass(message: Message, state: FSMContext):
    if message.text == "ower":
        await message.answer("✅ Доступ получен", reply_markup=admin_kb())
        await state.clear()
    else:
        await message.answer("❌ Неверный пароль")

# ================= ТИКЕТЫ =================
@router.callback_query(F.data == "tickets")
async def tickets(callback: CallbackQuery):
    if callback.from_user.id != OWNER_ID:
        return

    tickets = get_tickets()

    if not tickets:
        await callback.message.edit_text("📭 Нет сообщений")
        return

    text = "📩 Сообщения:\n\n"
    for t in tickets:
        text += f"{t[0]}. {t[2]}\n"

    await callback.message.edit_text(text)

# ================= СТАТИСТИКА =================
@router.callback_query(F.data == "stats")
async def stats(callback: CallbackQuery):
    await callback.message.edit_text(
        "📊 Статистика пока базовая.\n\n"
        "Позже добавим AI анализ."
    )
