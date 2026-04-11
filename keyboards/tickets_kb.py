from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def tickets_keyboard(tickets):
    buttons = []

    for t in tickets:
        buttons.append([
            InlineKeyboardButton(
                text=f"#{t[0]} | {t[3]} | @{t[2]}",
                callback_data=f"ticket_{t[0]}"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
