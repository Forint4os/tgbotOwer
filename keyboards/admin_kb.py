from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import CATEGORIES

# Главное меню администратора
def admin_menu_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("📩 Мои сообщения"), KeyboardButton("📊 Статистика"))
    return kb

# Кнопки для выбора категории сообщений при фильтре
def select_category_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for cat in CATEGORIES:
        kb.add(KeyboardButton(cat))
    kb.add(KeyboardButton("⬅️ Назад"))
    return kb

# Кнопки для выбора конкретного сообщения по его ID
def select_message_kb(message_ids):
    kb = InlineKeyboardMarkup()
    for msg_id in message_ids:
        kb.add(InlineKeyboardButton(f"Сообщение #{msg_id}", callback_data=f"msg_{msg_id}"))
    kb.add(InlineKeyboardButton("⬅️ Назад", callback_data="back"))
    return kb

# Кнопки для навигации при ответе на сообщение
def reply_navigation_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("➡️ Далее"), KeyboardButton("⬅️ Назад"))
    return kb
