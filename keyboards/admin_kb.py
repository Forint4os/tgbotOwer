from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Тикеты", callback_data="adm_tickets")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="adm_stats")]
    ])


def ticket_actions(ticket_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✍️ Ответить", callback_data=f"adm_reply:{ticket_id}"),
            InlineKeyboardButton(text="✅ Закрыть", callback_data=f"adm_close:{ticket_id}")
        ],
        [
            InlineKeyboardButton(text="🔙 Назад", callback_data="adm_back")
        ]
    ])
