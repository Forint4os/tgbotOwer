from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📩 Написать"),
                KeyboardButton(text="ℹ️ Помощь")
            ],
            [
                KeyboardButton(text="📊 Статистика"),
                KeyboardButton(text="👨‍💻 Админ")
            ]
        ],
        resize_keyboard=True
    )
