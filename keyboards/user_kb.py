from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📩 Написать", callback_data="write")],
        [InlineKeyboardButton(text="❓ Помощь", callback_data="help")]
    ])


def receiver_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👑 Admin", callback_data="rcv_admin"),
            InlineKeyboardButton(text="💼 Работа", callback_data="rcv_work")
        ],
        [
            InlineKeyboardButton(text="💡 Предложения", callback_data="rcv_offer"),
            InlineKeyboardButton(text="💰 Зарплата", callback_data="rcv_salary")
        ],
        [
            InlineKeyboardButton(text="⚠️ Ошибки", callback_data="rcv_bug"),
            InlineKeyboardButton(text="📞 Поддержка", callback_data="rcv_support")
        ],
        [
            InlineKeyboardButton(text="👤 Личное", callback_data="rcv_private"),
            InlineKeyboardButton(text="📦 Другое", callback_data="rcv_other")
        ]
    ])


def back_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
    ])
