from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def admin_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Тикеты"), KeyboardButton(text="📊 Статистика")],
            [KeyboardButton(text="🚪 Выйти")]
        ],
        resize_keyboard=True
    )
