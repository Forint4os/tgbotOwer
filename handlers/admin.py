from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from states import AdminStates
from config import ADMINS, CATEGORIES
from database import get_messages_for_admin, get_messages_by_category, get_message_by_id, update_message_status, get_stats

router = Router()

def is_admin(user_id):
    return user_id in ADMINS.values()

@router.message(Command("admin"))
async def admin_panel(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет доступа к админ-панели.")
        return
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(KeyboardButton("📩 Сообщения"), KeyboardButton("📊 Статистика"))
    await message.answer("⚙️ <b>Админ-панель</b>", parse_mode="HTML", reply_markup=kb)
    await state.set_state(AdminStates.menu)

@router.message(AdminStates.menu, F.text == "📩 Сообщения")
async def choose_filter(message: types.Message, state: FSMContext):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(0, len(CATEGORIES), 2):
        if i+1 < len(CATEGORIES):
            kb.row(
                KeyboardButton(f"💼 {CATEGORIES[i]}"),
                KeyboardButton(f"💰 {CATEGORIES[i+1]}")
            )
        else:
            kb.row(KeyboardButton(f"💼 {CATEGORIES[i]}"))
    kb.add(KeyboardButton("📥 Все"))
    await message.answer("📂 Выбери категорию для фильтрации:", reply_markup=kb)
    await state.set_state(AdminStates.filter_category)

@router.message(AdminStates.filter_category)
async def show_messages(message: types.Message, state: FSMContext):
    if message.text == "📥 Все":
        msgs = get_messages_for_admin(message.from_user.id)
    elif message.text.replace("💼 ","").replace("💰 ","") in CATEGORIES:
        category = message.text.replace("💼 ","").replace("💰 ","")
        msgs = get_messages_by_category(message.from_user.id, category)
    else:
        await message.answer("⚠️ Используй кнопки ниже!")
        return

    if not msgs:
        await message.answer("📭 Нет сообщений.")
        return

    for msg in msgs[:10]:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("✉️ Ответить", callback_data=f"reply_{msg[0]}"),
                 InlineKeyboardButton("❌ Пропустить", callback_data=f"skip_{msg[0]}")]
            ]
        )
        await message.answer(
            f"📩 <b>Сообщение #{msg[0]}</b>\n"
            f"📂 Категория: {msg[2]}\n"
            f"👤 От: {msg[1]}\n"
            f"💬 {msg[3]}\n"
            f"📌 Статус: {msg[4]}",
            parse_mode="HTML",
            reply_markup=kb
        )
    await state.set_state(AdminStates.view_messages)

@router.callback_query(F.data.startswith("reply_"))
async def reply_start(callback: types.CallbackQuery, state: FSMContext):
    msg_id = int(callback.data.split("_")[1])
    await state.update_data(msg_id=msg_id)
    await callback.message.answer("✍️ Напиши ответ:")
    await state.set_state(AdminStates.write_reply)
    await callback.answer()

@router.callback_query(F.data.startswith("skip_"))
async def skip_message(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("⏭ Пропущено. Следующее сообщение:")
    await show_messages(callback.message, state)
    await callback.answer()

@router.message(AdminStates.write_reply)
async def send_reply(message: types.Message, state: FSMContext):
    data = await state.get_data()
    msg_id = data["msg_id"]
    msg = get_message_by_id(msg_id)
    if not msg:
        await message.answer("⚠️ Ошибка, сообщение не найдено.")
        return

    user_id = msg[1]
    await message.bot.send_message(
        user_id,
        f"📬 <b>Ответ на сообщение #{msg_id}</b>\n💬 {message.text}",
        parse_mode="HTML"
    )

    update_message_status(msg_id, "✅")
    await message.answer("✅ Ответ отправлен! Следующее сообщение:")
    await show_messages(message, state)
    await state.set_state(AdminStates.view_messages)

@router.message(AdminStates.menu, F.text == "📊 Статистика")
async def stats(message: types.Message):
    total, new, done, categories = get_stats(message.from_user.id)
    text = f"📊 <b>Статистика</b>\n\nВсего: {total}\nНовые: {new}\nОтвеченные: {done}\n\nПо категориям:\n"
    for cat, count in categories:
        text += f"{cat}: {count}\n"
    await message.answer(text, parse_mode="HTML")