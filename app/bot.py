import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from app.config import BOT_TOKEN
from app.digest import get_top_news

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


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

    text = "🚀 Startup Digest\n\n"

    for i, item in enumerate(news, 1):
        text += (
            f"{i}️⃣ {item['title']}\n"
            f"{item.get('summary','')}\n"
            f"🔗 {item['url']}\n\n"
        )

    await message.answer(text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
