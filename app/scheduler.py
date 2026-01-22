import asyncio
from datetime import datetime, timedelta

from app.bot import bot
from app.digest import get_top_news
from app.config import DIGEST_HOUR, DIGEST_MINUTE, CHAT_ID
from aiogram.exceptions import TelegramNetworkError


async def send_daily_digest():
    news = get_top_news()
    if not news:
        return

    text = "🚀 Daily Startup Digest\n\n"
    for i, item in enumerate(news, 1):
        text += f"{i}️⃣ {item['title']}\n🔗 {item['url']}\n\n"

    try:
        await bot.send_message(CHAT_ID, text)
    except TelegramNetworkError as e:
        print("Telegram network error:", e)


async def scheduler():
    while True:
        now = datetime.now()
        target = now.replace(
            hour=DIGEST_HOUR, minute=DIGEST_MINUTE, second=0, microsecond=0
        )

        if target <= now:
            target += timedelta(days=1)

        await asyncio.sleep((target - now).total_seconds())
        await send_daily_digest()


if __name__ == "__main__":
    asyncio.run(scheduler())
