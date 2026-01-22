from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def user_keyboard() -> ReplyKeyboardMarkup:
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



def admin_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔄 Получить дайджест")],
            [
                KeyboardButton(text="⏰ Моё время"),
                KeyboardButton(text="⚙️ Установить время")
            ],
            [
                KeyboardButton(text="👥 Пользователи"),
                KeyboardButton(text="♻️ Reset today")
            ],
            [KeyboardButton(text="📊 Статистика")],
            [KeyboardButton(text="📖 Инструкция")]
        ],
        resize_keyboard=True
    )