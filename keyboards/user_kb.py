from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📩 Написать"), KeyboardButton(text="🆘 Помощь")],
            [KeyboardButton(text="💼 Работа"), KeyboardButton(text="💡 Предложения")],
            [KeyboardButton(text="💰 Зарплата"), KeyboardButton(text="🤝 Коллаборация")],
            [KeyboardButton(text="⚠️ Ошибки"), KeyboardButton(text="📞 Поддержка")],
            [KeyboardButton(text="👤 Личное"), KeyboardButton(text="📦 Другое")]
        ],
        resize_keyboard=True
    )
