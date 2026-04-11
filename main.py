import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from config import TOKEN
from handlers import user

async def main():
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )

    dp = Dispatcher()

    dp.include_router(user.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
