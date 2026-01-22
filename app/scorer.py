from datetime import datetime

KEYWORDS = [
    "investment",
    "funding",
    "raised",
    "round",
    "seed",
    "series",
    "acquired",
    "exit",
    "AI",
]


def score_item(item: dict) -> int:
    score = 0

    text = f"{item.get('title', '')} {item.get('summary', '')}".lower()

    for kw in KEYWORDS:
        if kw.lower() in text:
            score += 1

    # бонус за свежесть (сегодня)
    published = item.get("published_at")
    if published:
        try:
            pub_date = datetime.fromisoformat(published).date()
            if pub_date == datetime.utcnow().date():
                score += 2
        except:
            pass

    return score
