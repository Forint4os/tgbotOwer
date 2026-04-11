from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import ADMIN_ID
from keyboards.user_kb import main_menu, receiver_menu, back_menu
from states import UserFlow
from utils.tickets import create_ticket

router = Router()


# ---------------- START ----------------
@router.message(F.text == "/start")
async def start(message: Message, state: FSMContext):
    await state.set_state(UserFlow.menu)

    await message.answer(
        "👋 <b>Система активна</b>",
        reply_markup=main_menu()
    )


# ---------------- MENU CLICK ----------------
@router.callback_query(F.data == "write")
async def write(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserFlow.choose_receiver)

    await callback.message.edit_text(
        "📨 <b>Выберите тему:</b>",
        reply_markup=receiver_menu()
    )

    await callback.answer()


# ---------------- RECEIVER ----------------
@router.callback_query(F.data.startswith("rcv_"))
async def receiver(callback: CallbackQuery, state: FSMContext):

    mapping = {
        "rcv_admin": "Admin",
        "rcv_work": "Работа",
        "rcv_offer": "Предложения",
        "rcv_salary": "Зарплата",
        "rcv_bug": "Ошибки",
        "rcv_support": "Поддержка",
        "rcv_private": "Личное",
        "rcv_other": "Другое",
    }

    choice = mapping.get(callback.data, "Unknown")

    await state.update_data(receiver=choice)
    await state.set_state(UserFlow.write_message)

    await callback.message.edit_text(
        "✍️ <b>Напишите сообщение одним текстом:</b>",
        reply_markup=back_menu()
    )

    await callback.answer()


# ---------------- BACK ----------------
@router.callback_query(F.data == "back")
async def back(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserFlow.menu)

    await callback.message.edit_text(
        "🏠 <b>Главное меню</b>",
        reply_markup=main_menu()
    )

    await callback.answer()


# ---------------- MESSAGE INPUT ----------------
@router.message(UserFlow.write_message)
async def send(message: Message, state: FSMContext):

    data = await state.get_data()
    receiver = data.get("receiver", "unknown")

    ticket = create_ticket(
        user_id=message.from_user.id,
        username=message.from_user.username or "no_username",
        category=receiver,
        text=message.text
    )

    await message.answer(
        "✅ <b>Отправлено</b>\n⏳ Ожидайте ответ",
        reply_markup=main_menu()
    )

    await message.bot.send_message(
        ADMIN_ID,
        f"📩 <b>Тикет #{ticket['id']}</b>\n"
        f"👤 @{ticket['username']}\n"
        f"🎯 {ticket['category']}\n\n"
        f"💬 {ticket['text']}"
    )

    await state.clear()
