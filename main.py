import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import user, admin


TOKEN = "YOUR_BOT_TOKEN_HERE"


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(
        token=TOKEN,
        parse_mode=ParseMode.HTML
    )

    dp = Dispatcher(storage=MemoryStorage())

    # регистрация роутеров
    dp.include_router(user.router)
    dp.include_router(admin.router)

    print("🤖 Bot started")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
