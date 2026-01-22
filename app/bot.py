import asyncio
from aiogram import Bot, Dispatcher

from app.config import BOT_TOKEN
from app.logger import logger

from app.handlers.common import router as common_router
from app.handlers.digest import router as digest_router
from app.handlers.admin import router as admin_router

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(common_router)
dp.include_router(digest_router)
dp.include_router(admin_router)


async def main():
    try:
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        logger.info("Bot polling cancelled")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user (Ctrl+C)")
