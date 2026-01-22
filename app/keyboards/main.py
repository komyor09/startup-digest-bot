from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🔄 Получить дайджест")
            ],
            [
                KeyboardButton(text="⏰ Моё время"),
                KeyboardButton(text="⚙️ Установить время")
            ],
            [
                KeyboardButton(text="📖 Инструкция")
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )
