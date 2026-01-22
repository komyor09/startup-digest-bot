from app.parsers.techcrunch import parse_techcrunch
from app.storage import Storage

storage = Storage()

news = parse_techcrunch()

saved = 0
for item in news:
    if storage.save_news(item):
        saved += 1

print(f"Saved {saved} news from TechCrunch")
