import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

DIGEST_HOUR = 13  # 09:00
DIGEST_MINUTE = 2
TIMEZONE = "Asia/Dushanbe"

CHAT_ID = int(os.getenv("CHAT_ID", "0"))