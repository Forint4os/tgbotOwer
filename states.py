from aiogram.fsm.state import StatesGroup, State

class UserStates(StatesGroup):
    choose_category = State()
    choose_receiver = State()
    confirm_receiver = State()
    write_message = State()
    confirm_send = State()

class AdminStates(StatesGroup):
    menu = State()
    filter_category = State()
    view_messages = State()
    write_reply = State()