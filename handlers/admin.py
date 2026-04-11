from aiogram import Router, F
from aiogram.types import Message

router = Router()

ADMIN_ID = 5476359789
ADMIN_PASSWORD = "123"

admin_logged = set()


@router.message(F.text.startswith("/admin"))
async def admin_login(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    parts = message.text.split()

    if len(parts) < 2:
        await message.answer("🔐 Введите пароль: /admin 123")
        return

    if parts[1] == ADMIN_PASSWORD:
        admin_logged.add(message.from_user.id)
        await message.answer("👨‍💻 Админ панель активирована")
    else:
        await message.answer("❌ Неверный пароль")
