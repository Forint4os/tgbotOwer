from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from states import AdminStates
from config import ADMINS, CATEGORIES
from database import (
    get_messages_for_admin,
    get_messages_by_category,
    get_message_by_id,
    update_message_status,
    get_stats
)

router = Router()

def is_admin(user_id):
    return user_id in ADMINS.values()

# Главное меню
@router.message(Command("admin"))
async def admin_panel(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="📩 Сообщения")],
            [types.KeyboardButton(text="📊 Статистика")]
        ],
        resize_keyboard=True
    )

    await message.answer("⚙️ Админ панель:", reply_markup=kb)
    await state.set_state(AdminStates.menu)

# ================= СООБЩЕНИЯ =================

@router.message(AdminStates.menu, F.text == "📩 Сообщения")
async def choose_filter(message: types.Message, state: FSMContext):
    kb = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text=cat)] for cat in CATEGORIES] + [[types.KeyboardButton(text="📥 Все")]],
        resize_keyboard=True
    )
    await message.answer("Выбери категорию:", reply_markup=kb)
    await state.set_state(AdminStates.filter_category)

# Фильтр
@router.message(AdminStates.filter_category)
async def show_messages(message: types.Message, state: FSMContext):
    if message.text == "📥 Все":
        msgs = get_messages_for_admin(message.from_user.id)
    elif message.text in CATEGORIES:
        msgs = get_messages_by_category(message.from_user.id, message.text)
    else:
        await message.answer("Выбери кнопку.")
        return

    if not msgs:
        await message.answer("Нет сообщений.")
        return

    for msg in msgs[:10]:  # последние 10
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✉️ Ответить", callback_data=f"reply_{msg[0]}")]
        ])

        await message.answer(
            f"📩 #{msg[0]}\n"
            f"📂 {msg[2]}\n"
            f"📄 {msg[3]}\n"
            f"📌 {msg[4]}",
            reply_markup=kb
        )

    await state.set_state(AdminStates.view_messages)

# Кнопка "ответить"
@router.callback_query(F.data.startswith("reply_"))
async def reply_start(callback: types.CallbackQuery, state: FSMContext):
    msg_id = int(callback.data.split("_")[1])

    await state.update_data(msg_id=msg_id)
    await callback.message.answer("Напиши ответ:")
    await state.set_state(AdminStates.write_reply)

# Отправка ответа
@router.message(AdminStates.write_reply)
async def send_reply(message: types.Message, state: FSMContext):
    data = await state.get_data()
    msg_id = data["msg_id"]

    msg = get_message_by_id(msg_id)

    if not msg:
        await message.answer("Ошибка.")
        return

    user_id = msg[1]

    await message.bot.send_message(
        user_id,
        f"📬 Ответ на сообщение #{msg_id}:\n{message.text}"
    )

    update_message_status(msg_id, "✅")

    await message.answer("Ответ отправлен ✅")
    await state.clear()

# ================= СТАТИСТИКА =================

@router.message(AdminStates.menu, F.text == "📊 Статистика")
async def stats(message: types.Message):
    total, new, done, categories = get_stats(message.from_user.id)

    text = f"""
📊 Статистика:

Всего: {total}
Новые: {new}
Отвеченные: {done}

По категориям:
"""

    for cat, count in categories:
        text += f"{cat}: {count}\n"

    await message.answer(text)