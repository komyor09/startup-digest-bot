from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from datetime import datetime

from app.storage import Storage
from app.utils import format_published_at
from app.digest import get_top_news

router = Router()


@router.message(Command("time"))
@router.message(lambda m: m.text == "⏰ Моё время")
async def get_time_handler(message: Message):
    storage = Storage()
    time = storage.get_user_time(message.from_user.id)

    if time:
        await message.answer(f"⏰ Время рассылки: {time}")
    else:
        await message.answer("⏰ Время рассылки ещё не задано")


@router.message(lambda m: m.text == "⚙️ Установить время")
async def settime_help_handler(message: Message):
    await message.answer(
        "⚙️ *Установка времени рассылки*\n\n"
        "Отправь команду:\n"
        "`/settime ЧЧ:MM`\n\n"
        "Пример:\n"
        "`/settime 09:30`",
        parse_mode="Markdown"
    )


@router.message(Command("help"))
@router.message(lambda m: m.text == "📖 Инструкция")
async def help_handler(message: Message):
    await message.answer(
        "📖 *Как пользоваться ботом*\n\n"
        "🔄 Получить дайджест — свежие новости сейчас\n"
        "⏰ Моё время — текущее время рассылки\n"
        "⚙️ Установить время — инструкция\n\n"
        "Также доступны команды:\n"
        "/now, /time, /settime ЧЧ:MM",
        parse_mode="Markdown"
    )

@router.message(Command("now"))
@router.message(lambda m: m.text and "Получить дайджест" in m.text)
async def now_handler(message: Message):
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
