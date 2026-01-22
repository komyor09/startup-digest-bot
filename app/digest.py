from app.storage import Storage
from app.scorer import score_item
from app.logger import logger

def get_top_news(limit: int = 5):
    storage = Storage()
    news = storage.get_today_news()

    for item in news:
        item["score"] = score_item(item)

    sorted_news = sorted(
        news,
        key=lambda x: (x["score"], x.get("published_at") or ""),
        reverse=True
    )
    
    logger.info(f"[Digest] Total items today: {len(news)}")
    logger.info(f"[Digest] Returning top {limit}")
    return sorted_news[:limit]
