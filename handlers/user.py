from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import ADMIN_ID
from states import UserFlow
from keyboards.user_kb import main_menu, receiver_menu

router = Router()

# ---------------- ADMIN LIST (6 BUTTONS LOGIC) ----------------
ADMINS_UI = [
    ("👑 Главный админ", ADMIN_ID),
    ("🛠 Админ 2", None),
    ("🧩 Зам 1", None),
    ("🧩 Зам 2", None),
    ("🧩 Зам 3", None),
    ("🧩 Зам 4", None),
]


# ---------------- START ----------------
@router.message(F.text == "/start")
async def start(message: Message, state: FSMContext):

    await state.set_state(UserFlow.menu)

    await message.answer(
        "👋 <b>Система активна</b>\n\nВыберите действие:",
        reply_markup=main_menu()
    )


# ---------------- MAIN MENU ----------------
@router.callback_query(F.data == "write")
async def write(callback: CallbackQuery, state: FSMContext):

    await state.set_state(UserFlow.choose_receiver)

    await callback.message.edit_text(
        "📨 <b>Выберите категорию:</b>",
        reply_markup=receiver_menu()
    )

    await callback.answer()


# ---------------- CATEGORY SELECT ----------------
@router.callback_query(F.data.startswith("rcv_"))
async def category(callback: CallbackQuery, state: FSMContext):

    category_map = {
        "rcv_admin": "Админ",
        "rcv_work": "Работа",
        "rcv_offer": "Предложения",
        "rcv_salary": "Зарплата",
        "rcv_bug": "Ошибки",
        "rcv_support": "Поддержка",
        "rcv_private": "Личное",
        "rcv_other": "Другое",
    }

    cat = category_map.get(callback.data, "Другое")

    await state.update_data(category=cat)
    await state.set_state(UserFlow.write_message)

    await callback.message.edit_text(
        f"📂 <b>Категория:</b> {cat}\n\n"
        f"👥 <b>Выберите получателя:</b>\n\n"
        f"(первые 2 активны, остальные резерв)",
        reply_markup=admins_keyboard()
    )

    await callback.answer()


# ---------------- ADMINS KEYBOARD (6 BUTTONS) ----------------
def admins_keyboard():

    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    buttons = []

    for name, uid in ADMINS_UI:

        if uid is None:
            buttons.append([
                InlineKeyboardButton(
                    text=f"{name} (неактивен)",
                    callback_data="disabled"
                )
            ])
        else:
            buttons.append([
                InlineKeyboardButton(
                    text=name,
                    callback_data=f"select_admin:{uid}"
                )
            ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


# ---------------- ADMIN SELECT ----------------
@router.callback_query(F.data.startswith("select_admin:"))
async def select_admin(callback: CallbackQuery, state: FSMContext):

    admin_id = int(callback.data.split(":")[1])

    await state.update_data(target_admin=admin_id)
    await state.set_state(UserFlow.write_message)

    await callback.message.edit_text(
        "✍️ <b>Напишите сообщение одним текстом:</b>"
    )

    await callback.answer()


# ---------------- DISABLED BUTTON ----------------
@router.callback_query(F.data == "disabled")
async def disabled(callback: CallbackQuery):
    await callback.answer("❌ пока недоступно", show_alert=True)


# ---------------- HELP BUTTON ----------------
@router.callback_query(F.data == "help")
async def help_menu(callback: CallbackQuery):

    await callback.message.edit_text(
        "❓ <b>Помощь</b>\n\n"
        "• 📩 Написать — отправка сообщения\n"
        "• 📂 Категории — выбор темы\n"
        "• 👥 Админы — выбор получателя\n\n"
        "Если что-то не работает — попробуйте /start",
        reply_markup=main_menu()
    )

    await callback.answer()


# ---------------- SEND MESSAGE ----------------
@router.message(UserFlow.write_message)
async def send(message: Message, state: FSMContext):

    data = await state.get_data()

    category = data.get("category", "Другое")
    target = data.get("target_admin", ADMIN_ID)

    await message.bot.send_message(
        target,
        f"📩 <b>Новое сообщение</b>\n\n"
        f"📂 {category}\n"
        f"👤 @{message.from_user.username or 'no_username'}\n\n"
        f"💬 {message.text}"
    )

    await message.answer(
        "✅ <b>Отправлено</b>\n⏳ Ожидайте ответ",
        reply_markup=main_menu()
    )

    await state.clear()
