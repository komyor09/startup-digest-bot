import requests
from datetime import datetime
from app.logger import logger

TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"


def parse_hackernews(limit: int = 20):
    ids = requests.get(TOP_STORIES_URL, timeout=10).json()
    items = []

    for story_id in ids[:limit]:
        data = requests.get(ITEM_URL.format(story_id), timeout=10).json()
        if not data:
            continue

        # нас интересуют только статьи с ссылкой
        if data.get("type") != "story" or "url" not in data:
            continue

        items.append({
            "title": data.get("title"),
            "url": data.get("url"),
            "summary": "",  # HN не даёт summary — это нормально
            "published_at": datetime.utcfromtimestamp(
                data.get("time")
            ).isoformat(),
            "source": "Hacker News"
        })
    logger.info(f"[HackerNews] Parsed {len(items)} items")
    return items
