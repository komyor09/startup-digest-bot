from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from datetime import datetime

from app.digest import get_top_news
from app.logger import logger
from app.utils import format_published_at

router = Router()


@router.message(Command("now"))
async def now_handler(message: Message):
    logger.info(f"[Bot] /now requested by {message.from_user.id}")
    news = get_top_news()

    if not news:
        await message.answer("Пока нет свежих новостей 😕")
        return

    today = datetime.utcnow().strftime("%d %b %Y")
    text = f"🚀 *Startup Digest* · {today}\n\n"

    for i, item in enumerate(news, 1):
        text += (
            f"{i}️⃣ *{item['title']}*\n"
            f"📍 {item.get('source', 'Unknown')}\n"
            f"🕒 {format_published_at(item.get('published_at'))}\n"
            f"🔗 {item['url']}\n\n"
        )

    await message.answer(text, parse_mode="Markdown")
