from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.inline import main_menu, categories, recipients
from states.user_states import UserStates
from database.db import create_ticket
from config import ADMIN_ID

router = Router()


@router.message(F.text == "/start")
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "👋 Привет! Я бот-помощник OWER.\n\n"
        "Здесь ты можешь:\n"
        "— задать вопрос\n"
        "— отправить предложение\n"
        "— написать администрации\n\n"
        "Пожалуйста, не спамь.",
        reply_markup=main_menu()
    )


@router.callback_query(F.data == "write")
async def write(callback: CallbackQuery):
    await callback.message.edit_text(
        "📂 Выберите категорию:",
        reply_markup=categories()
    )
    await callback.answer()


@router.callback_query(F.data == "help")
async def help_section(callback: CallbackQuery):
    await callback.message.edit_text(
        "ℹ️ Помощь\n\n"
        "Этот бот позволяет анонимно связаться с администрацией.\n\n"
        "Нажмите «Написать», выберите тему и получателя — и отправьте сообщение.",
        reply_markup=main_menu()
    )
    await callback.answer()


@router.callback_query(F.data == "tips")
async def tips_section(callback: CallbackQuery):
    await callback.message.edit_text(
        "💡 Советы\n\n"
        "— Пишите конкретно и по делу\n"
        "— Укажите суть проблемы\n"
        "— Одно обращение = одна тема",
        reply_markup=main_menu()
    )
    await callback.answer()


@router.callback_query(F.data == "back")
async def go_back(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "👋 Главное меню:",
        reply_markup=main_menu()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("cat_"))
async def choose_category(callback: CallbackQuery, state: FSMContext):
    category_map = {
        "salary": "💰 Зарплата",
        "complaint": "⚠️ Жалоба",
        "suggest": "💡 Предложение",
        "other": "📌 Другое"
    }
    key = callback.data.split("_")[1]
    category = category_map.get(key, key)

    await state.update_data(category=category)

    await callback.message.edit_text(
        f"Категория: {category}\n\n👤 Выберите получателя:",
        reply_markup=recipients()
    )
    await callback.answer()


@router.callback_query(F.data == "admin_1")
async def choose_admin(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.waiting_message)
    await state.update_data(msg_id=callback.message.message_id)

    await callback.message.edit_text(
        "✏️ Напишите ваше сообщение одним текстом.\n\n"
        "Для отмены — /start"
    )
    await callback.answer()


@router.callback_query(F.data == "none")
async def not_available(callback: CallbackQuery):
    await callback.answer("Этот получатель пока недоступен", show_alert=True)


@router.message(UserStates.waiting_message)
async def send_ticket(message: Message, state: FSMContext):
    data = await state.get_data()
    category = data.get("category", "Другое")

    ticket_id = create_ticket(
        user_id=message.from_user.id,
        category=category,
        message=message.text
    )

    await message.answer(
        f"✅ Сообщение отправлено!\n\n"
        f"Номер обращения: #{ticket_id}\n"
        f"Категория: {category}\n\n"
        "Ответ придёт в этот чат.",
        reply_markup=main_menu()
    )

    username = f"@{message.from_user.username}" if message.from_user.username else f"id:{message.from_user.id}"

    await message.bot.send_message(
        ADMIN_ID,
        f"📩 Новый тикет #{ticket_id}\n\n"
        f"👤 Пользователь: {username}\n"
        f"📂 Категория: {category}\n\n"
        f"💬 Сообщение:\n{message.text}\n\n"
        f"Чтобы ответить: /reply {ticket_id}"
    )

    await state.clear()
