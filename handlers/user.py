from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import OWNER_ID
from database.db import create_ticket

router = Router()

# ================= FSM =================
class UserStates(StatesGroup):
    choosing_category = State()
    choosing_admin = State()
    writing_message = State()

# ================= КНОПКИ =================
def main_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✍️ Написать"), KeyboardButton(text="ℹ️ Помощь")],
            [KeyboardButton(text="💼 Работа"), KeyboardButton(text="💡 Предложения")],
            [KeyboardButton(text="💰 Зарплата"), KeyboardButton(text="🤝 Коллаборация")],
            [KeyboardButton(text="⚠️ Ошибки"), KeyboardButton(text="🛠 Поддержка")],
            [KeyboardButton(text="👤 Личное"), KeyboardButton(text="📌 Другое")]
        ],
        resize_keyboard=True
    )

def admin_choice_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👑 Главный админ")],
            [KeyboardButton(text="👑 Админ 2")],
            [KeyboardButton(text="➖ Пусто"), KeyboardButton(text="➖ Пусто")],
            [KeyboardButton(text="⬅️ Назад")]
        ],
        resize_keyboard=True
    )

# ================= /start =================
@router.message(F.text.in_(["/start", "старт", "Start"]))
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "👋 Привет!\n\n"
        "Я — бот-помощник OWER.\n\n"
        "📩 Здесь ты можешь:\n"
        "• Написать админу\n"
        "• Задать вопрос\n"
        "• Отправить предложение\n\n"
        "⚠️ Пожалуйста, не спамь.\n\n"
        "👇 Выбери действие:",
        reply_markup=main_kb()
    )

# ================= ПОМОЩЬ =================
@router.message(F.text == "ℹ️ Помощь")
async def help_handler(message: Message):
    await message.answer(
        "📖 Помощь:\n\n"
        "1. Нажми 'Написать'\n"
        "2. Выбери категорию\n"
        "3. Выбери админа\n"
        "4. Напиши сообщение\n\n"
        "📬 Ответ придет сюда же."
    )

# ================= КАТЕГОРИИ =================
categories = [
    "💼 Работа", "💡 Предложения", "💰 Зарплата",
    "🤝 Коллаборация", "⚠️ Ошибки",
    "🛠 Поддержка", "👤 Личное", "📌 Другое"
]

@router.message(F.text.in_(categories))
async def choose_category(message: Message, state: FSMContext):
    await state.update_data(category=message.text)

    await message.answer(
        f"📂 Категория: {message.text}\n\n"
        "👤 Выберите администратора:",
        reply_markup=admin_choice_kb()
    )

    await state.set_state(UserStates.choosing_admin)

# ================= ВЫБОР АДМИНА =================
@router.message(UserStates.choosing_admin)
async def choose_admin(message: Message, state: FSMContext):

    if message.text == "⬅️ Назад":
        await state.clear()
        await message.answer("🔙 Возврат в меню", reply_markup=main_kb())
        return

    if "Пусто" in message.text:
        await message.answer("❌ Этот слот пока не используется")
        return

    admin_id = OWNER_ID

    await state.update_data(admin_id=admin_id)

    await message.answer(
        "✍️ Напишите ваше сообщение одним текстом.\n\n"
        "📩 Оно будет отправлено администратору.",
        reply_markup=None
    )

    await state.set_state(UserStates.writing_message)

# ================= ОТПРАВКА СООБЩЕНИЯ =================
@router.message(UserStates.writing_message)
async def send_ticket(message: Message, state: FSMContext):
    data = await state.get_data()

    create_ticket(
        user_id=message.from_user.id,
        category=data["category"],
        text=message.text
    )

    # отправка админу
    try:
        await message.bot.send_message(
            data["admin_id"],
            f"📩 Новое сообщение!\n\n"
            f"👤 Пользователь: {message.from_user.id}\n"
            f"📂 Категория: {data['category']}\n\n"
            f"💬 {message.text}"
        )
    except:
        pass  # если бот заблокирован — игнор

    await message.answer(
        "✅ Сообщение отправлено!\n\n"
        "📬 Ожидайте ответ администратора.",
        reply_markup=main_kb()
    )

    await state.clear()
