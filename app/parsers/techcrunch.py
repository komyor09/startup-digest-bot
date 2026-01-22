import feedparser
from datetime import datetime
from app.logger import logger


FEED_URL = "https://techcrunch.com/category/startups/feed/"


def parse_techcrunch():
    feed = feedparser.parse(FEED_URL)
    items = []

    for entry in feed.entries:
        published = None
        if hasattr(entry, "published"):
            published = datetime(*entry.published_parsed[:6]).isoformat()

        items.append(
            {
                "title": entry.title,
                "url": entry.link,
                "summary": entry.summary if hasattr(entry, "summary") else "",
                "published_at": published,
                "source": "TechCrunch",
            }
        )
    logger.info(f"[TechCrunch] Parsed {len(items)} items")
    return items
