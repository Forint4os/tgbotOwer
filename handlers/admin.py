from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import OWNER_ID
from database.db import get_tickets

router = Router()

class AdminStates(StatesGroup):
    password = State()

def admin_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Статистика")],
            [KeyboardButton(text="📩 Тикеты")],
            [KeyboardButton(text="⬅️ Выход")]
        ],
        resize_keyboard=True
    )

# ================= ВХОД =================
@router.message(F.text == "/admin")
async def admin_login(message: Message, state: FSMContext):
    await state.set_state(AdminStates.password)
    await message.answer("🔐 Введите пароль:")

@router.message(AdminStates.password)
async def check_password(message: Message, state: FSMContext):
    if message.text == "123":
        await message.answer(
            "✅ Доступ разрешён",
            reply_markup=admin_kb()
        )
        await state.clear()
    else:
        await message.answer("❌ Неверный пароль")

# ================= ТИКЕТЫ =================
@router.message(F.text == "📩 Тикеты")
async def tickets(message: Message):
    if message.from_user.id != OWNER_ID:
        return

    tickets = get_tickets()

    if not tickets:
        await message.answer("📭 Нет тикетов")
        return

    text = "📩 Список сообщений:\n\n"

    for t in tickets:
        text += f"ID: {t[0]} | {t[2]}\n"

    await message.answer(text)

# ================= СТАТИСТИКА =================
@router.message(F.text == "📊 Статистика")
async def stats(message: Message):
    await message.answer(
        "📊 Статистика:\n\n"
        "Пока простая версия\n"
        "Позже подключим AI анализ"
    )
