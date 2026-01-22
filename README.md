# Startup Digest Bot

Telegram bot that aggregates startup and venture news from multiple sources
and delivers a daily digest.

## Features
- News parsing from TechCrunch, Sifted, VC.ru, RB.ru, Hacker News
- Daily automatic digest
- On-demand digest via /now command

## Tech stack
- Python
- aiogram
- SQLite

## Data sources

The service aggregates startup and venture news from the following sources:

- **TechCrunch (Startups)** — via RSS feed  
- **Hacker News** — via official public API  
- **VC.ru (Tribuna / Startups)** — via RSS feed  
- **RB.ru (Rusbase)** — via RSS feed  
- **Sifted (startup-fundraise tag)** — via lightweight HTML parsing (MVP)

All sources are normalized into a unified internal format
(title, url, summary, publication date, source).

---

## Known limitations (MVP notes)

Some data sources apply technical restrictions that affect automated access.
These limitations are intentionally handled gracefully in this MVP version.

### VC.ru and RB.ru
- RSS feeds may occasionally return empty responses.
- This behavior depends on the external feed stability and is outside the control of the application.
- The parser implementation is kept simple and reliable for MVP purposes.

### Sifted
- Sifted serves content dynamically and applies anti-bot protection.
- Plain HTTP requests (and even headless browsers in some environments) may return
  empty or incomplete HTML.
- For this MVP, a lightweight HTML parser with graceful fallback is implemented.
- Production-grade integration would require:
  - official API access, or
  - licensed data feeds, or
  - a dedicated rendering service.

These limitations are documented intentionally to keep the MVP lightweight,
transparent, and focused on core functionality.

---

## Design decisions

- No heavy scraping or anti-bot bypassing is used.
- No headless browser is enabled by default to avoid unnecessary complexity.
- Priority is given to system robustness, clarity, and explainable behavior.
- The goal of this implementation is to demonstrate data flow, processing logic,
  and delivery, rather than exhaustive content extraction.

---

## Future improvements

- Add fallback strategies per source (API / rendered HTML where permitted)
- Improve relevance scoring using NLP techniques
- Extend digest personalization
- Add source health monitoring
