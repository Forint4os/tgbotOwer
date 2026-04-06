from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states import UserStates
from config import CATEGORIES, ADMINS
from database import add_message

router = Router()

# Старт
@router.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    await state.clear()
    kb = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text=cat)] for cat in CATEGORIES],
        resize_keyboard=True
    )
    await message.answer("Выберите категорию:", reply_markup=kb)
    await state.set_state(UserStates.choose_category)

# Выбор категории
@router.message(UserStates.choose_category)
async def choose_category(message: types.Message, state: FSMContext):
    if message.text not in CATEGORIES:
        await message.answer("Выберите категорию кнопкой.")
        return

    await state.update_data(category=message.text)

    # список админов
    kb = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text=name)] for name in ADMINS.keys()],
        resize_keyboard=True
    )
    await message.answer("Выберите получателя:", reply_markup=kb)
    await state.set_state(UserStates.choose_receiver)

# Выбор получателя
@router.message(UserStates.choose_receiver)
async def choose_receiver(message: types.Message, state: FSMContext):
    if message.text not in ADMINS:
        await message.answer("Выберите получателя из списка.")
        return

    await state.update_data(receiver=message.text)

    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="✅ Подтвердить")],
            [types.KeyboardButton(text="⬅️ Назад")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        f"Вы выбрали: {message.text}\nПодтвердить?",
        reply_markup=kb
    )
    await state.set_state(UserStates.confirm_receiver)

# Подтверждение получателя
@router.message(UserStates.confirm_receiver)
async def confirm_receiver(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        return await start_handler(message, state)

    if message.text != "✅ Подтвердить":
        await message.answer("Нажмите кнопку.")
        return

    await message.answer("Напишите сообщение:")
    await state.set_state(UserStates.write_message)

# Ввод сообщения
@router.message(UserStates.write_message)
async def write_message(message: types.Message, state: FSMContext):
    if not message.text:
        await message.answer("Сообщение не может быть пустым.")
        return

    await state.update_data(text=message.text)

    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="📤 Отправить")],
            [types.KeyboardButton(text="⬅️ Назад")]
        ],
        resize_keyboard=True
    )

    await message.answer("Отправить сообщение?", reply_markup=kb)
    await state.set_state(UserStates.confirm_send)

# Подтверждение отправки
@router.message(UserStates.confirm_send)
async def confirm_send(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        await message.answer("Напишите сообщение заново:")
        await state.set_state(UserStates.write_message)
        return

    if message.text != "📤 Отправить":
        await message.answer("Нажмите кнопку.")
        return

    data = await state.get_data()

    receiver_name = data["receiver"]
    receiver_id = ADMINS[receiver_name]

    # если ID пока нет
    if receiver_id is None:
        await message.answer("Админ пока не настроен.")
        return

    # сохраняем в БД
    msg_id = add_message(
        from_user=message.from_user.id,
        to_user=receiver_id,
        category=data["category"],
        text=data["text"]
    )

    # отправка админу
    await message.bot.send_message(
        receiver_id,
        f"📩 Новое сообщение #{msg_id}\n"
        f"Категория: {data['category']}\n"
        f"Текст: {data['text']}"
    )

    await message.answer("✅ Сообщение отправлено!")
    await state.clear()