from aiogram import types
from aiogram.fsm.context import FSMContext
from states import UserStates
from keyboards.user_kb import category_kb, receiver_kb, confirm_receiver_kb, navigation_kb, optional_ai_kb
from database import add_message
from utils import detect_category_ai

async def start_handler(msg: types.Message, state: FSMContext):
    await msg.answer("Выберите категорию:", reply_markup=category_kb())
    await state.set_state(UserStates.choose_category)

# Все остальные хендлеры: выбор категории, получателя, подтверждение, ввод текста, опциональный вызов нейросети
# Проверка пустых сообщений, анти-мисклик и кнопки "Далее/Назад" реализованы
