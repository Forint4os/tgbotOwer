from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import ADMINS
from database.db import create_ticket

router = Router()


class TicketState(StatesGroup):
    choose_admin = State()
    choose_category = State()
    write_message = State()


# ---------------- START ----------------
@router.message(F.text.in_({"/start", "start"}))
async def start(message: Message):

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📩 Написать", callback_data="write")],
        [InlineKeyboardButton(text="❓ Помощь", callback_data="help")]
    ])

    await message.answer(
        "👋 <b>Система активна</b>\nВыберите действие:",
        reply_markup=kb
    )


# ---------------- WRITE ----------------
@router.callback_query(F.data == "write")
async def write(callback: CallbackQuery, state: FSMContext):

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👑 Админ 1", callback_data="admin_0")],
        [InlineKeyboardButton(text="👑 Админ 2", callback_data="admin_1")],
        [InlineKeyboardButton(text="⬜ Пусто", callback_data="empty")],
        [InlineKeyboardButton(text="⬜ Пусто", callback_data="empty")],
        [InlineKeyboardButton(text="⬜ Пусто", callback_data="empty")],
        [InlineKeyboardButton(text="⬜ Пусто", callback_data="empty")]
    ])

    await state.set_state(TicketState.choose_admin)

    await callback.message.edit_text(
        "👤 Выберите получателя:",
        reply_markup=kb
    )

    await callback.answer()


# ---------------- CHOOSE ADMIN ----------------
@router.callback_query(F.data.startswith("admin_"))
async def choose_admin(callback: CallbackQuery, state: FSMContext):

    index = int(callback.data.split("_")[1])

    admin_id = ADMINS[index]

    await state.update_data(admin_id=admin_id)
    await state.set_state(TicketState.choose_category)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Зарплата", callback_data="cat_salary")],
        [InlineKeyboardButton(text="💼 Предложение", callback_data="cat_offer")],
        [InlineKeyboardButton(text="⚠️ Ошибка", callback_data="cat_bug")],
        [InlineKeyboardButton(text="🛠 Поддержка", callback_data="cat_support")],
        [InlineKeyboardButton(text="📄 Другое", callback_data="cat_other")]
    ])

    await callback.message.edit_text(
        "📂 Выберите категорию:",
        reply_markup=kb
    )

    await callback.answer()


# ---------------- CATEGORY ----------------
@router.callback_query(F.data.startswith("cat_"))
async def choose_category(callback: CallbackQuery, state: FSMContext):

    map_cat = {
        "cat_salary": "Зарплата",
        "cat_offer": "Предложение",
        "cat_bug": "Ошибка",
        "cat_support": "Поддержка",
        "cat_other": "Другое"
    }

    category = map_cat.get(callback.data, "Другое")

    await state.update_data(category=category)
    await state.set_state(TicketState.write_message)

    await callback.message.edit_text(
        "✍️ Напишите сообщение одним текстом:"
    )

    await callback.answer()


# ---------------- MESSAGE ----------------
@router.message(TicketState.write_message)
async def send_ticket(message: Message, state: FSMContext):

    data = await state.get_data()

    ticket_id = create_ticket(
        user_id=message.from_user.id,
        admin_id=data["admin_id"],
        category=data["category"],
        message=message.text
    )

    await message.bot.send_message(
        data["admin_id"],
        f"📩 <b>Новый тикет #{ticket_id}</b>\n"
        f"📂 {data['category']}\n"
        f"👤 {message.from_user.id}\n\n"
        f"💬 {message.text}"
    )

    await message.answer("✅ <b>Отправлено</b>")

    await state.clear()
