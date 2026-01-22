from playwright.sync_api import sync_playwright

URL = "https://sifted.eu/tag/startup-fundraise"


def parse_sifted_playwright():
    items = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto(URL, timeout=60000, wait_until="networkidle")

        # иногда Sifted показывает cookie banner
        try:
            page.click("button:has-text('Accept')", timeout=3000)
        except:
            pass

        # ждём появления ссылок вообще
        page.wait_for_timeout(5000)

        links = page.query_selector_all("a")

        for link in links:
            try:
                title = link.inner_text().strip()
                href = link.get_attribute("href")
            except:
                continue

            if not href or not title:
                continue

            # фильтр по смыслу
            if "sifted.eu" not in href and not href.startswith("/"):
                continue

            if len(title) < 20:
                continue

            # нормализуем URL
            if href.startswith("/"):
                href = "https://sifted.eu" + href

            items.append({
                "title": title,
                "url": href,
                "summary": "",
                "published_at": None,
                "source": "Sifted"
            })

        browser.close()

    # убираем дубли
    unique = {item["url"]: item for item in items}
    return list(unique.values())
