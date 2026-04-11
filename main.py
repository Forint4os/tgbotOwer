import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from config import TOKEN
from handlers import user, admin
from database.db import init_db


async def main():
    init_db()

    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )

    dp = Dispatcher()

    dp.include_router(user.router)
    dp.include_router(admin.router)

    print("🤖 Bot started")

    await dp.start_polling(
        bot,
        skip_updates=True,
        allowed_updates=["message", "callback_query"]
    )


if __name__ == "__main__":
    asyncio.run(main())
