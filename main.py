import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import TOKEN
from database.db import init_db
from handlers import user, admin

logging.basicConfig(level=logging.INFO)


async def main():

    init_db()

    # ❗ НОРМАЛЬНЫЙ bot (без aiohttp вручную)
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()

    dp.include_router(user.router)
    dp.include_router(admin.router)

    print("🤖 Bot started")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
