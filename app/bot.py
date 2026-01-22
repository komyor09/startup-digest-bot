import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from datetime import datetime

from app.config import BOT_TOKEN
from app.digest import get_top_news

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


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
