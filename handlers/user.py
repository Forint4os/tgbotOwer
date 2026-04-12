from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import ADMINS
from database.db import create_ticket

router = Router()


# ---------------- STATES ----------------
class TicketState(StatesGroup):
    choose_admin = State()
    choose_category = State()
    write_message = State()


# ---------------- START ----------------
@router.message(F.text.in_({"/start", "start"}))
async def start(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📩 Написать")],
            [KeyboardButton(text="❓ Помощь")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "👋 <b>Система поддержки активна</b>\n\nВыберите действие:",
        reply_markup=kb
    )


# ---------------- WRITE BUTTON ----------------
@router.message(F.text == "📩 Написать")
async def write_start(message: Message, state: FSMContext):

    admins_buttons = []

    # первые 2 — реальные админы
    for admin_id in ADMINS[:2]:
        admins_buttons.append([KeyboardButton(text=f"👑 Админ {admin_id}")])

    # остальные 4 пустые слоты
    for i in range(4):
        admins_buttons.append([KeyboardButton(text="⬜ Свободно")])

    kb = ReplyKeyboardMarkup(
        keyboard=admins_buttons,
        resize_keyboard=True
    )

    await state.set_state(TicketState.choose_admin)

    await message.answer(
        "👤 Выберите получателя:",
        reply_markup=kb
    )


# ---------------- CHOOSE ADMIN ----------------
@router.message(TicketState.choose_admin)
async def choose_admin(message: Message, state: FSMContext):

    text = message.text

    if "Свободно" in text:
        await message.answer("⚠️ Этот слот пока не активен.")
        return

    # берём первого админа (упрощённо)
    admin_id = ADMINS[0]

    await state.update_data(admin_id=admin_id)

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💰 Зарплата")],
            [KeyboardButton(text="💼 Предложение")],
            [KeyboardButton(text="⚠️ Ошибка")],
            [KeyboardButton(text="🛠 Поддержка")],
            [KeyboardButton(text="📄 Другое")],
        ],
        resize_keyboard=True
    )

    await state.set_state(TicketState.choose_category)

    await message.answer(
        "📂 Выберите категорию:",
        reply_markup=kb
    )


# ---------------- CATEGORY ----------------
@router.message(TicketState.choose_category)
async def choose_category(message: Message, state: FSMContext):

    await state.update_data(category=message.text)

    await state.set_state(TicketState.write_message)

    await message.answer(
        "✍️ Напишите сообщение одним текстом:"
    )


# ---------------- SEND MESSAGE ----------------
@router.message(TicketState.write_message)
async def send_ticket(message: Message, state: FSMContext):

    data = await state.get_data()

    admin_id = data["admin_id"]
    category = data["category"]

    ticket_id = create_ticket(
        user_id=message.from_user.id,
        admin_id=admin_id,
        category=category,
        message=message.text
    )

    # уведомление админу
    await message.bot.send_message(
        admin_id,
        f"📩 <b>Новый тикет #{ticket_id}</b>\n"
        f"📂 {category}\n"
        f"👤 @{message.from_user.username or message.from_user.id}\n\n"
        f"💬 {message.text}"
    )

    await message.answer(
        "✅ <b>Сообщение отправлено!</b>\nОжидайте ответ."
    )

    await state.clear()
