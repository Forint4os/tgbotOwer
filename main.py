import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import TOKEN
from database.db import init_db

from handlers import user, admin


# ---------------- LOGGING ----------------
logging.basicConfig(level=logging.INFO)


# ---------------- MAIN ----------------
async def main():
    # init DB
    init_db()

    # bot
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()

    # routers
    dp.include_router(user.router)
    dp.include_router(admin.router)

    print("🤖 Bot started")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
