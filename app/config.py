import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

DIGEST_HOUR = 9   # 09:00
DIGEST_MINUTE = 0
TIMEZONE = "Asia/Dushanbe"
