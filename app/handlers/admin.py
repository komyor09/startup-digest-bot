from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from datetime import datetime

from app.storage import Storage
from app.config import ADMIN_USER_ID

router = Router()


@router.message(Command("settime"))
async def set_time_handler(message: Message):
    parts = message.text.strip().split()

    if len(parts) != 2:
        await message.answer(
            "❌ *Неверный формат команды*\n\n"
            "Используй:\n"
            "`/settime ЧЧ:MM`\n\n"
            "Пример:\n"
            "`/settime 09:30`",
            parse_mode="Markdown",
        )
        return

    time_str = parts[1]

    try:
        datetime.strptime(time_str, "%H:%M")
    except ValueError:
        await message.answer(
            "❌ *Неверный формат времени*\n\n"
            "Используй формат `ЧЧ:MM`, например:\n"
            "`/settime 14:30`",
            parse_mode="Markdown",
        )
        return

    storage = Storage()
    storage.set_user_time(message.from_user.id, time_str)

    await message.answer(
        f"✅ *Время ежедневного дайджеста установлено*\n\n⏰ Новое время: `{time_str}`",
        parse_mode="Markdown",
    )


@router.message(Command("time"))
async def get_time_handler(message: Message):
    storage = Storage()
    time = storage.get_user_time(message.from_user.id)

    if time:
        await message.answer(
            f"⏰ *Ваше текущее время рассылки*\n\n`{time}`", parse_mode="Markdown"
        )
    else:
        await message.answer(
            "⏰ *Время рассылки ещё не задано*\n\nИспользуй команду:\n`/settime ЧЧ:MM`",
            parse_mode="Markdown",
        )


@router.message(Command("resetsent"))
async def reset_sent_handler(message: Message):
    if message.from_user.id != ADMIN_USER_ID:
        await message.answer("⛔ Команда доступна только администратору")
        return

    parts = message.text.strip().split()
    target_user_id = ADMIN_USER_ID

    if len(parts) == 2:
        try:
            target_user_id = int(parts[1])
        except ValueError:
            await message.answer("❌ Неверный формат user_id")
            return

    storage = Storage()
    storage.clear_last_sent_date(target_user_id)

    await message.answer(
        f"♻️ *Состояние доставки сброшено*\n\n"
        f"👤 Пользователь: `{target_user_id}`\n"
        "📬 Дайджест может быть отправлен снова сегодня.",
        parse_mode="Markdown",
    )


@router.message(Command("users"))
async def users_handler(message: Message):
    if message.from_user.id != ADMIN_USER_ID:
        await message.answer("⛔ Команда доступна только администратору")
        return

    storage = Storage()
    users = storage.get_users(limit=20)

    if not users:
        await message.answer("Пока нет пользователей")
        return

    total = len(users)
    text = (
        f"👥 Пользователи бота\n"
        f"Всего в списке: {total}\n\n"
    )

    for i, u in enumerate(users, start=1):
        username = f"@{u['username']}" if u["username"] else "—"

        text += (
            f"{i}. ID: {u['user_id']}\n"
            f"Username: {username}\n"
            f"Name: {u['full_name']}\n\n"
        )

    await message.answer(text)

@router.message(lambda m: m.text == "👥 Пользователи")
async def users_button_handler(message: Message):
    if message.from_user.id != ADMIN_USER_ID:
        return

    await users_handler(message)

@router.message(lambda m: m.text == "♻️ Reset today")
async def reset_today_button(message: Message):
    if message.from_user.id != ADMIN_USER_ID:
        return

    storage = Storage()
    storage.clear_last_sent_date(ADMIN_USER_ID)

    await message.answer("♻️ Состояние доставки сброшено для сегодня")
