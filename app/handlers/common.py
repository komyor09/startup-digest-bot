from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.keyboards.main import user_keyboard, admin_keyboard
from app.storage import Storage
from app.config import ADMIN_USER_ID

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    storage = Storage()
    storage.save_user(message.from_user)

    is_admin = message.from_user.id == ADMIN_USER_ID
    keyboard = admin_keyboard() if is_admin else user_keyboard()

    text = (
        "👋 *Добро пожаловать!*\n\n"
        "Я автоматически собираю стартап- и венчурные новости "
        "из ведущих источников и формирую удобный ежедневный дайджест.\n\n"
        "👇 *Выберите действие с помощью кнопок внизу* "
        "или используйте команды:\n\n"
        "🔄 `/now` — получить свежий дайджест прямо сейчас\n"
        "⏰ `/time` — посмотреть время ежедневной рассылки\n"
        "⚙️ `/settime ЧЧ:MM` — установить удобное время доставки\n\n"
        "📌 *Пример:*\n"
        "👉 `/settime 14:30`"
    )

    if is_admin:
        text += "\n\n🛡 *Режим администратора активен*"

    await message.answer(
        text,
        parse_mode="Markdown",
        reply_markup=keyboard,
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
        reply_markup=main_keyboard(),
    )
