import feedparser
from datetime import datetime

FEED_URL = "https://rb.ru/rss/"


def parse_rusbase():
    feed = feedparser.parse(FEED_URL)
    items = []

    for entry in feed.entries:
        published = None
        if hasattr(entry, "published"):
            published = datetime(*entry.published_parsed[:6]).isoformat()

        items.append({
            "title": entry.title,
            "url": entry.link,
            "summary": entry.summary if hasattr(entry, "summary") else "",
            "published_at": published,
            "source": "RB.ru"
        })

    return items
