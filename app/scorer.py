from datetime import datetime

# Взвешенные ключевые слова (объяснимо и прозрачно)
KEYWORDS_WEIGHTS = {
    "investment": 3,
    "funding": 3,
    "raised": 3,
    "round": 2,
    "series": 2,
    "seed": 1,
    "exit": 4,
    "acquired": 4,
    "merger": 3,
    "ai": 1,
    "artificial intelligence": 1,
}

# Бонусы за источник (экспертиза / сигнал качества)
SOURCE_BONUS = {
    "TechCrunch": 2,
    "Sifted": 2,
    "Hacker News": 1,
    "VC.ru": 1,
    "RB.ru": 1,
}


def score_item(item: dict) -> int:
    score = 0

    title = item.get("title", "")
    summary = item.get("summary", "")
    text = f"{title} {summary}".lower()

    # 1️⃣ Ключевые слова
    for keyword, weight in KEYWORDS_WEIGHTS.items():
        if keyword in text:
            score += weight

    # 2️⃣ Свежесть (приоритет сегодняшним)
    published = item.get("published_at")
    if published:
        try:
            pub_date = datetime.fromisoformat(published).date()
            today = datetime.utcnow().date()

            if pub_date == today:
                score += 3
            elif (today - pub_date).days == 1:
                score += 1
        except Exception:
            pass

    # 3️⃣ Бонус за источник
    source = item.get("source")
    score += SOURCE_BONUS.get(source, 0)

    return score
