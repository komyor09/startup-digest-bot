import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

DIGEST_HOUR = 15  # 09:00
DIGEST_MINUTE = 37
TIMEZONE = "Asia/Dushanbe"

CHAT_ID = int(os.getenv("CHAT_ID", "0"))
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "0"))