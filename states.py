from aiogram.fsm.state import StatesGroup, State

class UserStates(StatesGroup):
    choose_category = State()
    choose_receiver = State()
    confirm_receiver = State()
    write_message = State()
    confirm_send = State()
    optional_ai = State()

class AdminStates(StatesGroup):
    menu = State()
    select_category = State()
    select_message = State()
    write_reply = State()