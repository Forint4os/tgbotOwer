from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
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
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✍️ Написать", callback_data="write"),
            InlineKeyboardButton(text="ℹ️ Помощь", callback_data="help")
        ],
        [
            InlineKeyboardButton(text="💼 Работа", callback_data="cat_Работа"),
            InlineKeyboardButton(text="💡 Предложения", callback_data="cat_Предложения")
        ],
        [
            InlineKeyboardButton(text="💰 Зарплата", callback_data="cat_Зарплата"),
            InlineKeyboardButton(text="🤝 Коллаборация", callback_data="cat_Коллаборация")
        ],
        [
            InlineKeyboardButton(text="⚠️ Ошибки", callback_data="cat_Ошибки"),
            InlineKeyboardButton(text="🛠 Поддержка", callback_data="cat_Поддержка")
        ],
        [
            InlineKeyboardButton(text="👤 Личное", callback_data="cat_Личное"),
            InlineKeyboardButton(text="📌 Другое", callback_data="cat_Другое")
        ]
    ])

def admin_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👑 Главный админ", callback_data="admin_main")],
        [InlineKeyboardButton(text="👑 Админ 2", callback_data="admin_second")],
        [
            InlineKeyboardButton(text="➖ Пусто", callback_data="empty"),
            InlineKeyboardButton(text="➖ Пусто", callback_data="empty")
        ],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
    ])

# ================= START =================
@router.message(F.text.in_(["/start", "старт"]))
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "👋 Привет!\n\n"
        "Я бот-помощник OWER.\n\n"
        "📩 Здесь ты можешь отправить сообщение админу.\n"
        "⚠️ Не спамь.\n\n"
        "👇 Выбери действие:",
        reply_markup=main_kb()
    )

# ================= HELP =================
@router.callback_query(F.data == "help")
async def help_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "📖 Помощь:\n\n"
        "1. Выбери категорию\n"
        "2. Выбери админа\n"
        "3. Напиши сообщение\n\n"
        "📬 Ответ придёт сюда.",
        reply_markup=main_kb()
    )

# ================= КАТЕГОРИИ =================
@router.callback_query(F.data.startswith("cat_"))
async def category(callback: CallbackQuery, state: FSMContext):
    cat = callback.data.split("_")[1]

    await state.update_data(category=cat)

    await callback.message.edit_text(
        f"📂 Категория: {cat}\n\n"
        "👤 Выберите администратора:",
        reply_markup=admin_kb()
    )

    await state.set_state(UserStates.choosing_admin)

# ================= ВЫБОР АДМИНА =================
@router.callback_query(UserStates.choosing_admin)
async def choose_admin(callback: CallbackQuery, state: FSMContext):

    if callback.data == "back":
        await state.clear()
        await callback.message.edit_text(
            "🔙 Возврат в меню",
            reply_markup=main_kb()
        )
        return

    if callback.data == "empty":
        await callback.answer("❌ Пока не доступно", show_alert=True)
        return

    admin_id = OWNER_ID

    await state.update_data(admin_id=admin_id)

    await callback.message.edit_text(
        "✍️ Напишите сообщение одним текстом.\n\n"
        "📩 Оно будет отправлено админу."
    )

    await state.set_state(UserStates.writing_message)

# ================= ОТПРАВКА =================
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
            f"📩 Новое сообщение\n\n"
            f"👤 {message.from_user.id}\n"
            f"📂 {data['category']}\n\n"
            f"{message.text}"
        )
    except:
        pass

    await message.answer(
        "✅ Сообщение отправлено!\n\n"
        "📬 Ждите ответ.",
        reply_markup=main_kb()
    )

    await state.clear()
