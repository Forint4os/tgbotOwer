import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from aiohttp import web

from config import TOKEN
from handlers import user, admin

logging.basicConfig(level=logging.INFO)

WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = "https://rural-bacon-venice-convenience.trycloudflare.com/webhook"

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

# Роутеры
dp.include_router(user.router)
dp.include_router(admin.router)


# --- WEBHOOK HANDLER ---
async def handle(request):
    data = await request.json()
    update = dp.resolve_update(data)
    await dp.feed_update(bot, update)
    return web.Response()


async def on_startup(app):
    print("🤖 Bot started (WEBHOOK MODE)")
    await bot.set_webhook(WEBHOOK_URL)
    print(f"🚀 Webhook set: {WEBHOOK_URL}")


async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()


async def main():
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle)

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, "0.0.0.0", 3000)
    await site.start()

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
