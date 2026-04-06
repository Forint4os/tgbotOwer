from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states import AdminStates
from config import ADMINS, CATEGORIES
from database import get_messages_for_admin, update_message_status

router = Router()

# Проверка: админ ли
def is_admin(user_id):
    return user_id in ADMINS.values()

# Вход в админку
@router.message(Command("admin"))
async def admin_panel(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="📩 Мои сообщения")],
            [types.KeyboardButton(text="📊 Статистика")]
        ],
        resize_keyboard=True
    )

    await message.answer("Админ панель:", reply_markup=kb)
    await state.set_state(AdminStates.menu)

# Просмотр сообщений
@router.message(AdminStates.menu, F.text == "📩 Мои сообщения")
async def my_messages(message: types.Message, state: FSMContext):
    msgs = get_messages_for_admin(message.from_user.id)

    if not msgs:
        await message.answer("Нет сообщений.")
        return

    text = "Ваши сообщения:\n\n"
    for msg in msgs:
        text += f"#{msg[0]} | {msg[2]} | {msg[4]}\n"

    await message.answer(text)
    await message.answer("Введите номер сообщения для ответа:")
    await state.set_state(AdminStates.select_message)

# Выбор сообщения
@router.message(AdminStates.select_message)
async def select_message(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите номер сообщения (цифру).")
        return

    msg_id = int(message.text)

    msgs = get_messages_for_admin(message.from_user.id)
    msg_ids = [m[0] for m in msgs]

    if msg_id not in msg_ids:
        await message.answer("Сообщение не найдено.")
        return

    await state.update_data(msg_id=msg_id)

    await message.answer("Введите ответ пользователю:")
    await state.set_state(AdminStates.write_reply)

# Ответ пользователю
@router.message(AdminStates.write_reply)
async def reply_to_user(message: types.Message, state: FSMContext):
    data = await state.get_data()
    msg_id = data["msg_id"]

    msgs = get_messages_for_admin(message.from_user.id)
    target_msg = None

    for m in msgs:
        if m[0] == msg_id:
            target_msg = m
            break

    if not target_msg:
        await message.answer("Ошибка.")
        return

    user_id = target_msg[1]

    # отправка пользователю
    await message.bot.send_message(
        user_id,
        f"📬 Ответ на ваше сообщение #{msg_id}:\n{message.text}"
    )

    # обновляем статус
    update_message_status(msg_id, "✅")

    await message.answer("Ответ отправлен ✅")
    await state.clear()