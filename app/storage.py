import sqlite3
from datetime import datetime
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
        self.conn.commit()

    def news_exists(self, url: str) -> bool:
        cursor = self.conn.execute(
            "SELECT 1 FROM news WHERE url = ? LIMIT 1",
            (url,)
        )
        return cursor.fetchone() is not None

    def save_news(self, item: dict):
        if self.news_exists(item["url"]):
            logger.debug(f"[Storage] Duplicate skipped: {item['url']}")
            return False

        self.conn.execute("""
        INSERT INTO news (title, url, summary, published_at, source, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            item["title"],
            item["url"],
            item.get("summary"),
            item.get("published_at"),
            item.get("source"),
            datetime.utcnow().isoformat()
        ))
        self.conn.commit()
        logger.info(f"[Storage] Saved news: {item['url']}")
        return True

    def get_today_news(self):
        today = datetime.utcnow().date().isoformat()
        cursor = self.conn.execute("""
        SELECT * FROM news
        WHERE date(created_at) = ?
        ORDER BY published_at DESC
        """, (today,))
        return [dict(row) for row in cursor.fetchall()]
