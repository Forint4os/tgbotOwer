from aiogram.fsm.state import State, StatesGroup


class UserFlow(StatesGroup):
    menu = State()
    choose_receiver = State()
    write_message = State()


class AdminFlow(StatesGroup):
    idle = State()
    viewing_ticket = State()
    replying = State()
