from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from states import UserStates
from config import CATEGORIES, ADMINS
from database import add_message

router = Router()

WELCOME_TEXT = "👋 Привет! Я твой помощник. Выбери категорию сообщения:"

@router.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    await state.clear()
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    # Две колонки с эмодзи
    for i in range(0, len(CATEGORIES), 2):
        if i+1 < len(CATEGORIES):
            kb.row(
                KeyboardButton(f"💼 {CATEGORIES[i]}"),
                KeyboardButton(f"💰 {CATEGORIES[i+1]}")
            )
        else:
            kb.row(KeyboardButton(f"💼 {CATEGORIES[i]}"))

    await message.answer(WELCOME_TEXT, reply_markup=kb)
    await state.set_state(UserStates.choose_category)

@router.message(UserStates.choose_category)
async def choose_category(message: types.Message, state: FSMContext):
    if message.text.replace("💼 ","").replace("💰 ","") not in CATEGORIES:
        await message.answer("⚠️ Используй кнопки ниже!")
        return
    category = message.text.replace("💼 ","").replace("💰 ","")
    await state.update_data(category=category)

    # Выбор администратора в 2 колонки с эмодзи
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    admin_list = list(ADMINS.keys())
    for i in range(0, len(admin_list), 2):
        if i+1 < len(admin_list):
            kb.row(
                KeyboardButton(f"👤 {admin_list[i]}"),
                KeyboardButton(f"👤 {admin_list[i+1]}")
            )
        else:
            kb.row(KeyboardButton(f"👤 {admin_list[i]}"))

    await message.answer("Выберите администратора, которому отправите сообщение:", reply_markup=kb)
    await state.set_state(UserStates.choose_receiver)

@router.message(UserStates.choose_receiver)
async def confirm_receiver(message: types.Message, state: FSMContext):
    admin_name = message.text.replace("👤 ","")
    if admin_name not in ADMINS:
        await message.answer("⚠️ Используй кнопки ниже!")
        return
    await state.update_data(admin=admin_name)
    await message.answer("✍️ Напиши сообщение:")
    await state.set_state(UserStates.write_message)

@router.message(UserStates.write_message)
async def send_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    category = data["category"]
    admin_name = data["admin"]
    admin_id = ADMINS[admin_name]

    msg_id = add_message(from_user=message.from_user.id, to_user=admin_id, category=category, text=message.text)
    await message.answer(f"✅ Сообщение #{msg_id} отправлено администратору {admin_name}!")

    # Цикл: снова выбор категории
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(0, len(CATEGORIES), 2):
        if i+1 < len(CATEGORIES):
            kb.row(
                KeyboardButton(f"💼 {CATEGORIES[i]}"),
                KeyboardButton(f"💰 {CATEGORIES[i+1]}")
            )
        else:
            kb.row(KeyboardButton(f"💼 {CATEGORIES[i]}"))
    await message.answer("Вы можете отправить ещё одно сообщение. Выберите категорию:", reply_markup=kb)
    await state.set_state(UserStates.choose_category)