from app.digest import get_top_news

top = get_top_news()

print("TOP NEWS:")
for i, item in enumerate(top, 1):
    print(f"{i}. {item['title']} (score={item['score']})")
