from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from datetime import datetime

from app.storage import Storage
from app.config import ADMIN_USER_ID
from app.logger import logger

router = Router()


@router.message(Command("settime"))
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


@router.message(Command("time"))
async def get_time_handler(message: Message):
    storage = Storage()
    time = storage.get_user_time(message.from_user.id)

    if time:
        await message.answer(f"⏰ Your daily digest time: {time}")
    else:
        await message.answer("⏰ Digest time is not set yet")


@router.message(Command("resetsent"))
async def reset_sent_handler(message: Message):
    if message.from_user.id != ADMIN_USER_ID:
        return

    storage = Storage()
    storage.clear_last_sent_date(ADMIN_USER_ID)

    await message.answer("♻️ Delivery state reset. Digest can be sent again today.")
