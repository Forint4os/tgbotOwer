from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Тикеты", callback_data="adm_tickets:0")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="adm_stats")]
    ])


def tickets_page(page: int, tickets, per_page=5):

    start = page * per_page
    end = start + per_page
    chunk = tickets[start:end]

    buttons = []

    for t in chunk:
        status = "❌" if t[5] == 0 else "✅"

        buttons.append([
            InlineKeyboardButton(
                text=f"{status} #{t[0]} | @{t[2]}",
                callback_data=f"adm_open:{t[0]}"
            )
        ])

    nav = []

    if page > 0:
        nav.append(
            InlineKeyboardButton(text="⬅️", callback_data=f"adm_tickets:{page-1}")
        )

    if end < len(tickets):
        nav.append(
            InlineKeyboardButton(text="➡️", callback_data=f"adm_tickets:{page+1}")
        )

    if nav:
        buttons.append(nav)

    buttons.append([
        InlineKeyboardButton(text="🔙 Назад", callback_data="adm_back")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
