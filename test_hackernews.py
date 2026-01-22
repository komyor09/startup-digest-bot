from app.parsers.hackernews import parse_hackernews
from app.storage import Storage

storage = Storage()

news = parse_hackernews(limit=20)

saved = 0
for item in news:
    if storage.save_news(item):
        saved += 1

print(f"Saved {saved} news from Hacker News")