import sqlite3
from datetime import datetime, date
from pathlib import Path
from app.logger import logger

DB_PATH = Path(__file__).resolve().parent / "news.db"


class Storage:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT NOT NULL UNIQUE,
            summary TEXT,
            published_at TEXT,
            source TEXT,
            created_at TEXT
        )
        """)

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS user_settings (
            user_id INTEGER PRIMARY KEY,
            digest_time TEXT
        )
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS delivery_state (
                user_id INTEGER PRIMARY KEY,
                last_sent_date TEXT
            );
            """)
        self.conn.commit()

    def news_exists(self, url: str) -> bool:
        cursor = self.conn.execute("SELECT 1 FROM news WHERE url = ? LIMIT 1", (url,))
        return cursor.fetchone() is not None

    def save_news(self, item: dict):
        if self.news_exists(item["url"]):
            logger.debug(f"[Storage] Duplicate skipped: {item['url']}")
            return False

        self.conn.execute(
            """
        INSERT INTO news (title, url, summary, published_at, source, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                item["title"],
                item["url"],
                item.get("summary"),
                item.get("published_at"),
                item.get("source"),
                datetime.utcnow().isoformat(),
            ),
        )
        self.conn.commit()
        logger.info(f"[Storage] Saved news: {item['url']}")
        return True

    def get_today_news(self):
        today = datetime.utcnow().date().isoformat()
        cursor = self.conn.execute(
            """
        SELECT * FROM news
        WHERE date(created_at) = ?
        ORDER BY published_at DESC
        """,
            (today,),
        )
        return [dict(row) for row in cursor.fetchall()]

    def set_user_time(self, user_id: int, time_str: str):
        self.conn.execute(
            """
        INSERT INTO user_settings (user_id, digest_time)
        VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET digest_time=excluded.digest_time
        """,
            (user_id, time_str),
        )
        self.conn.commit()

    def get_user_time(self, user_id: int) -> str | None:
        cursor = self.conn.execute(
            "SELECT digest_time FROM user_settings WHERE user_id = ?", (user_id,)
        )
        row = cursor.fetchone()
        return row["digest_time"] if row else None

    def get_last_sent_date(self, user_id: int) -> date | None:
        cursor = self.conn.execute(
            "SELECT last_sent_date FROM delivery_state WHERE user_id = ?", (user_id,)
        )
        row = cursor.fetchone()
        if not row or not row["last_sent_date"]:
            return None
        return date.fromisoformat(row["last_sent_date"])

    def set_last_sent_date(self, user_id: int, sent_date: date):
        self.conn.execute(
            """
            INSERT INTO delivery_state (user_id, last_sent_date)
            VALUES (?, ?)
            ON CONFLICT(user_id)
            DO UPDATE SET last_sent_date = excluded.last_sent_date
            """,
            (user_id, sent_date.isoformat()),
        )
        self.conn.commit()
        logger.info(f"[Storage] Digest marked as sent for {sent_date}")
