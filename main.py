import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram.client.default import DefaultBotProperties
from aiohttp import web

from config import TOKEN
from handlers import user, admin

# ТВОЙ CLOUDLFARE URL
WEBHOOK_HOST = "rural-bacon-venice-convenience.trycloudflare.com"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = 3000

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)

dp = Dispatcher()

dp.include_router(user.router)
dp.include_router(admin.router)


async def handle(request: web.Request):
    data = await request.json()
    update = Update(**data)
    await dp.feed_update(bot, update)
    return web.Response()


async def on_startup(app):
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(WEBHOOK_URL)
    print(f"🚀 Webhook set: {WEBHOOK_URL}")


async def on_shutdown(app):
    await bot.delete_webhook()


def main():
    app = web.Application()

    app.router.add_post(WEBHOOK_PATH, handle)

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    print("🤖 Bot started (WEBHOOK MODE)")

    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)


if __name__ == "__main__":
    main()
