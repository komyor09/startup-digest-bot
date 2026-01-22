from app.parsers.sifted import parse_sifted_playwright

news = parse_sifted_playwright()
print("Entries:", len(news))

if news:
    print(news[0])
