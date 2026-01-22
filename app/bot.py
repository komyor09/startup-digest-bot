import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from datetime import datetime
from app.logger import logger

from app.config import BOT_TOKEN
from app.digest import get_top_news
from app.storage import Storage

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def format_published_at(value: str | None) -> str:
    if not value:
        return "unknown date"

    try:
        dt = datetime.fromisoformat(value)
        return dt.strftime("%d %b %Y %H:%M")
    except Exception:
        return "unknown date"


@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "👋 Привет!\n\n"
        "Я собираю стартап и венчурные новости.\n"
        "Команда /now — показать свежий дайджест."
    )


@dp.message(Command("now"))
async def now_handler(message: Message):
    logger.info(f"[Bot] /now requested by {message.from_user.id}")
    news = get_top_news()

    if not news:
        await message.answer("Пока нет свежих новостей 😕")
        return

    today = datetime.utcnow().strftime("%d %b %Y")

    text = f"🚀 *Startup Digest* · {today}\n\n"

    for i, item in enumerate(news, 1):
        source = item.get("source", "Unknown")
        published = format_published_at(item.get("published_at"))

        text += (
            f"{i}️⃣ *{item['title']}*\n📍 {source}\n🕒 {published}\n🔗 {item['url']}\n\n"
        )

    await message.answer(text, parse_mode="Markdown")


@dp.message(Command("settime"))
async def set_time_handler(message: Message):
    parts = message.text.strip().split()

    if len(parts) != 2:
        await message.answer("❌ Usage: /settime HH:MM")
        return

    time_str = parts[1]

    try:
        datetime.strptime(time_str, "%H:%M")
    except ValueError:
        await message.answer("❌ Invalid time format. Use HH:MM")
        return

    storage = Storage()
    storage.set_user_time(message.from_user.id, time_str)
    logger.info(
        f"[Bot] settime called by user_id={message.from_user.id}, time={time_str}"
    )

    await message.answer(f"✅ Daily digest time set to {time_str}")


@dp.message(Command("time"))
async def get_time_handler(message: Message):
    storage = Storage()
    time = storage.get_user_time(message.from_user.id)

    if time:
        await message.answer(f"⏰ Your daily digest time: {time}")
    else:
        await message.answer("⏰ Digest time is not set yet")


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
