from app.storage import Storage

storage = Storage()

item = {
    "title": "Test news",
    "url": "https://example.com/test",
    "summary": "Just a test",
    "published_at": "2026-01-22T10:00:00",
    "source": "test"
}

print(storage.save_news(item))  # должно быть True
print(storage.save_news(item))  # должно быть False
print(storage.get_today_news())
