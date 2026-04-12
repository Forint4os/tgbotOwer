import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiohttp import ClientSession, TCPConnector, ClientTimeout

from config import TOKEN
from handlers import user, admin

async def main():
    timeout = ClientTimeout(total=60)

    session = ClientSession(
        connector=TCPConnector(limit=100),
        timeout=timeout
    )

    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode="HTML"),
        session=session
    )

    dp = Dispatcher()

    dp.include_router(user.router)
    dp.include_router(admin.router)

    print("🤖 Bot started")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
