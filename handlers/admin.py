from aiogram import types
from states import AdminStates
from database import get_messages_for_admin, update_message_status

async def admin_menu(msg: types.Message, state):
    await msg.answer("Выберите действие:", reply_markup=admin_menu_kb())
    await state.set_state(AdminStates.menu)

# Логика просмотра сообщений, выбор категории, ответ админа, обновление статуса
