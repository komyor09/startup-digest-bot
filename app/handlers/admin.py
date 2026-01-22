from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from datetime import datetime

from app.storage import Storage
from app.config import ADMIN_USER_ID

router = Router()


@router.message(Command("settime"))
async def set_time_handler(message: Message):
    parts = message.text.strip().split()

    if len(parts) != 2:
        await message.answer("❌ Использование: /settime ЧЧ:MM")
        return

    time_str = parts[1]

    try:
        datetime.strptime(time_str, "%H:%M")
    except ValueError:
        await message.answer("❌ Неверный формат времени. Use ЧЧ:MM")
        return

    storage = Storage()
    storage.set_user_time(message.from_user.id, time_str)

    await message.answer(f"✅ Время ежедневного дайджест установлено на {time_str}")


@router.message(Command("time"))
async def get_time_handler(message: Message):
    storage = Storage()
    time = storage.get_user_time(message.from_user.id)

    if time:
        await message.answer(f"⏰ Время для ежедневного дайджест:{time}")
    else:
        await message.answer("⏰ Время ежедневного дайджест еще не установлено.")


@router.callback_query(lambda c: c.data == "time")
async def time_callback(callback: CallbackQuery):
    storage = Storage()
    time = storage.get_user_time(callback.from_user.id)

    if time:
        await callback.message.answer(f"⏰ Время для ежедневного дайджест: {time}")
    else:
        await callback.message.answer("⏰ Время ежедневного дайджест еще не установлено.")

    await callback.answer()


@router.callback_query(lambda c: c.data == "settime_help")
async def settime_help_callback(callback: CallbackQuery):
    await callback.message.answer(
        "⚙️ *Установка времени рассылки*\n\n"
        "Отправь команду:\n"
        "`/settime HH:MM`\n\n"
        "Пример:\n"
        "`/settime 09:30`",
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "help")
async def help_callback(callback: CallbackQuery):
    await callback.message.answer(
        "📖 *Как пользоваться ботом*\n\n"
        "🔄 /now — получить свежий дайджест\n"
        "⏰ /time — посмотреть время рассылки\n"
        "⚙️ /settime HH:MM — установить время\n\n"
        "Используй кнопки ниже 👇",
        parse_mode="Markdown"
    )
    await callback.answer()

@router.message(Command("resetsent"))
async def reset_sent_handler(message: Message):
    # доступ только админу
    if message.from_user.id != ADMIN_USER_ID:
        await message.answer("⛔ Команда доступна только администратору")
        return

    parts = message.text.strip().split()

    # по умолчанию — сбрасываем админу
    target_user_id = ADMIN_USER_ID

    # если передали user_id
    if len(parts) == 2:
        try:
            target_user_id = int(parts[1])
        except ValueError:
            await message.answer("❌ Неверный формат user_id")
            return

    storage = Storage()
    storage.clear_last_sent_date(target_user_id)

    await message.answer(
        f"♻️ Состояние доставки сброшено для пользователя `{target_user_id}`.\n"
        "Дайджест может быть отправлен снова сегодня.",
        parse_mode="Markdown"
    )

