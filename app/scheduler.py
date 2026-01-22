import asyncio
from datetime import datetime, timedelta
from app.logger import logger

from app.bot import bot
from app.digest import get_top_news
from app.config import DIGEST_HOUR, DIGEST_MINUTE, CHAT_ID
from aiogram.exceptions import TelegramNetworkError
from app.storage import Storage
from app.config import ADMIN_USER_ID


def format_published_at(value: str | None) -> str:
    if not value:
        return "unknown date"

    try:
        dt = datetime.fromisoformat(value)
        return dt.strftime("%d %b %Y %H:%M")
    except Exception:
        return "unknown date"


async def send_daily_digest():
    news = get_top_news()
    if not news:
        return

    today = datetime.utcnow().strftime("%d %b %Y")
    text = f"🚀 *Daily Startup Digest* · {today}\n\n"

    for i, item in enumerate(news, 1):
        source = item.get("source", "Unknown")
        published = format_published_at(item.get("published_at"))

        text += (
            f"{i}️⃣ *{item['title']}*\n📍 {source}\n🕒 {published}\n🔗 {item['url']}\n\n"
        )

    try:
        logger.info("[Scheduler] Daily digest sent")
        await bot.send_message(CHAT_ID, text, parse_mode="Markdown")
    except TelegramNetworkError as e:
        logger.error(f"[Scheduler] Telegram error: {e}")


async def scheduler():
    storage = Storage()
    logger.info("[Scheduler] Started")

    while True:
        now = datetime.now()

        user_time = storage.get_user_time(ADMIN_USER_ID)
        if not user_time:
            await asyncio.sleep(20)
            continue

        try:
            hour, minute = map(int, user_time.split(":"))
        except ValueError:
            await asyncio.sleep(20)
            continue

        target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

        last_sent = storage.get_last_sent_date(ADMIN_USER_ID)

        # ГЛАВНОЕ УСЛОВИЕ
        if now >= target and last_sent != now.date():
            await send_daily_digest()
            storage.set_last_sent_date(ADMIN_USER_ID, now.date())

        await asyncio.sleep(20)

        


if __name__ == "__main__":
    try:
        asyncio.run(scheduler())
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user (Ctrl+C)")