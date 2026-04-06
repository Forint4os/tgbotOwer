from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states import UserStates
from config import CATEGORIES, ADMINS
from database import add_message

router = Router()

WELCOME_TEXT = """
👋 Привет! Добро пожаловать в систему сообщений.

📩 Отправляй сообщение администратору. Выбирай категорию:
"""

SENT_TEXT = "✅ <b>Сообщение отправлено!</b>\nТы можешь сразу отправить новое."

ERROR_TEXT = "⚠️ Пожалуйста, используй кнопки ниже."

# /start или цикл
@router.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    await state.clear()
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(*[types.KeyboardButton(f"📂 {cat}") for cat in CATEGORIES])
    await message.answer(WELCOME_TEXT, reply_markup=kb, parse_mode="HTML")
    await state.set_state(UserStates.choose_category)

# Выбор категории
@router.message(UserStates.choose_category)
async def choose_category(message: types.Message, state: FSMContext):
    cat = message.text.replace("📂 ", "")
    if cat not in CATEGORIES:
        await message.answer(ERROR_TEXT)
        return
    await state.update_data(category=cat)

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(*[types.KeyboardButton(f"👤 {name}") for name in ADMINS.keys()])
    await message.answer("👤 Выбери получателя:", reply_markup=kb)
    await state.set_state(UserStates.choose_receiver)

# Выбор получателя
@router.message(UserStates.choose_receiver)
async def choose_receiver(message: types.Message, state: FSMContext):
    name = message.text.replace("👤 ", "")
    if name not in ADMINS:
        await message.answer(ERROR_TEXT)
        return
    await state.update_data(receiver=name)

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(types.KeyboardButton("✅ Подтвердить"), types.KeyboardButton("🔙 Назад"))
    await message.answer(f"📌 Ты выбрал: <b>{name}</b>\nПодтверждаешь?", reply_markup=kb, parse_mode="HTML")
    await state.set_state(UserStates.confirm_receiver)

# Подтверждение
@router.message(UserStates.confirm_receiver)
async def confirm_receiver(message: types.Message, state: FSMContext):
    if message.text == "🔙 Назад":
        return await start_handler(message, state)
    if message.text != "✅ Подтвердить":
        await message.answer(ERROR_TEXT)
        return
    await message.answer("✍️ Напиши сообщение:")
    await state.set_state(UserStates.write_message)

# Написание сообщения
@router.message(UserStates.write_message)
async def write_message(message: types.Message, state: FSMContext):
    if not message.text:
        await message.answer("⚠️ Сообщение не может быть пустым.")
        return
    await state.update_data(text=message.text)

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(types.KeyboardButton("🚀 Отправить"), types.KeyboardButton("🔙 Назад"))
    await message.answer("📤 Отправляем сообщение?", reply_markup=kb)
    await state.set_state(UserStates.confirm_send)

# Отправка
@router.message(UserStates.confirm_send)
async def confirm_send(message: types.Message, state: FSMContext):
    if message.text == "🔙 Назад":
        await message.answer("✍️ Напиши сообщение заново:")
        await state.set_state(UserStates.write_message)
        return
    if message.text != "🚀 Отправить":
        await message.answer(ERROR_TEXT)
        return

    data = await state.get_data()
    receiver_id = ADMINS[data["receiver"]]

    msg_id = add_message(
        from_user=message.from_user.id,
        to_user=receiver_id,
        category=data["category"],
        text=data["text"]
    )

    await message.bot.send_message(
        receiver_id,
        f"📩 <b>Новое сообщение #{msg_id}</b>\n"
        f"📂 Категория: {data['category']}\n"
        f"👤 От: {message.from_user.full_name}\n"
        f"💬 {data['text']}",
        parse_mode="HTML"
    )

    await message.answer(SENT_TEXT, parse_mode="HTML")

    # после отправки сразу начать заново (цикл)
    await start_handler(message, state)