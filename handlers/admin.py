from aiogram import Router, F
from aiogram.types import Message
from config import ADMIN_ID
from utils.stats import get_stats

router = Router()


@router.message(F.text == "/admin")
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        f"👨‍💻 <b>Админ панель</b>\n\n"
        f"📊 Пользователей: {get_stats()}"
    )
