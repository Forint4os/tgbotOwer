from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import CATEGORIES

def category_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for c in CATEGORIES:
        kb.add(KeyboardButton(c))
    return kb

def receiver_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("Админ1"))
    kb.add(KeyboardButton("⬅️ Назад"))
    return kb

def confirm_receiver_kb(receiver):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(f"✅ Подтвердить ({receiver})", callback_data="confirm_receiver"))
    kb.add(InlineKeyboardButton("🔄 Выбрать заново", callback_data="retry_receiver"))
    return kb

def navigation_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("➡️ Далее"), KeyboardButton("⬅️ Назад"))
    return kb

def optional_ai_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🧠 Определить категорию через ИИ", callback_data="use_ai"))
    kb.add(InlineKeyboardButton("Пропустить", callback_data="skip_ai"))
    return kb