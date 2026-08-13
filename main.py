import asyncio
import logging
import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.enums import ParseMode

from config import BOT_TOKEN, WEBAPP_URL, PLATFORM, API_BASE
from database import init_db
from handlers import start_router, search_router, admin_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def on_startup(bot: Bot):
    await init_db()
    logger.info("Database initialized")
    me = await bot.get_me()
    logger.info(f"Platform = {PLATFORM}")
    logger.info(f"API_BASE = {API_BASE}")
    logger.info(f"Bot started: @{me.username} (id={me.id})")
    logger.info(f"WEBAPP_URL = {WEBAPP_URL}")


def create_webapp_app():
    """سرور ساده برای سرو کردن مینی‌اپ اسکنر"""
    app = web.Application()

    async def scanner_page(request):
        # یک فایل HTML برای هر دو پلتفرم؛ خودش تشخیص می‌دهد تلگرام است یا بله
        html = open("webapp/scanner.html", "r", encoding="utf-8").read()
        return web.Response(text=html, content_type="text/html")

    async def health(request):
        return web.Response(text=f"ok platform={PLATFORM}")

    app.router.add_get("/scanner", scanner_page)
    app.router.add_get("/", health)
    app.router.add_get("/health", health)
    return app


def build_bot() -> Bot:
    """ساخت Bot با endpoint مناسب پلتفرم"""
    if PLATFORM == "bale":
        # aiogram را به سرور بله وصل می‌کنیم
        session = AiohttpSession(
            api=TelegramAPIServer.from_base(API_BASE)
        )
        return Bot(
            token=BOT_TOKEN,
            session=session,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
    # تلگرام (پیش‌فرض)
    return Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )


async def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not set")

    bot = build_bot()
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start_router)
    dp.include_router(search_router)
    dp.include_router(admin_router)

    dp.startup.register(on_startup)

    web_app = create_webapp_app()
    runner = web.AppRunner(web_app)
    await runner.setup()
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info(f"WebApp server started on port {port}")

    try:
        await dp.start_polling(bot)
    finally:
        await runner.cleanup()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
