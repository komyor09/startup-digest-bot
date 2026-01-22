from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.keyboards.main import main_keyboard

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "👋 Привет!\n\n"
        "Я собираю стартап и венчурные новости "
        "и отправляю удобный ежедневный дайджест.\n\n"
        "Используй кнопки внизу 👇",
        reply_markup=main_keyboard()
    )


@router.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(
        "📖 *Как пользоваться ботом*\n\n"
        "🔄 /now — получить свежий дайджест\n"
        "⏰ /time — посмотреть время рассылки\n"
        "⚙️ /settime ЧЧ:MM — установить время\n\n"
        "Пример:\n"
        "`/settime 14:30`",
        parse_mode="Markdown",
        reply_markup=main_keyboard()
    )
