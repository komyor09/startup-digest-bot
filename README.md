# Startup Digest Bot

Telegram bot that aggregates startup and venture capital news from multiple
industry sources and delivers a curated daily digest.

The project is implemented as an MVP prototype to demonstrate
data extraction, processing, and delivery pipelines in a clear
and explainable way.

---

## Overview

The service automatically monitors selected technology and venture-focused
media sources, extracts structured news data, filters duplicates,
calculates relevance, and distributes a daily top-5 digest via Telegram.

Two delivery modes are supported:

- **Automatic daily digest** at a scheduled time
- **On-demand digest** via the `/now` command

---

## Functional Scope

### Data Extraction

The system performs regular monitoring of predefined sources.
From each publication, the following data is extracted (when available):

- News title
- Direct link to the original source
- Short description or lead paragraph
- Publication date and time
- Source identifier

All data is normalized into a unified internal format.

---

### Data Processing

- Duplicate content is eliminated using URL-based uniqueness
- All collected items are stored in SQLite
- A daily relevance score is calculated for each item based on:
  - weighted keyword indicators (funding, investment rounds, exits, etc.)
  - publication recency
  - source credibility bonus
- A daily **Top-5** most relevant news items is generated automatically

The relevance model is intentionally rule-based and explainable,
which is appropriate for an MVP and easy to calibrate.

---

### Delivery

Information is delivered via a Telegram bot built with **aiogram**.

Supported modes:

1. **Scheduled delivery** — automatic daily digest at a fixed time
2. **On-demand delivery** — instant digest generation via `/now`

Each digest entry includes:

- title
- source
- publication date/time
- direct link

---

## Data Sources

The service aggregates startup and venture news from the following resources:

- **TechCrunch (Startups)** — RSS feed
- **Hacker News** — official public API
- **VC.ru (Tribuna / Startups)** — RSS feed
- **RB.ru (Rusbase)** — RSS feed
- **Sifted (startup-fundraise tag)** — lightweight HTML parsing (MVP)

---

## Known Limitations (MVP Notes)

Some sources apply technical restrictions that affect automated access.
These limitations are intentionally handled gracefully in this MVP.

### VC.ru and RB.ru

- RSS feeds may occasionally return empty responses
- This behavior depends on external feed stability and is outside
  the control of the application
- The parsers are intentionally kept simple and reliable

### Sifted

- Sifted serves content dynamically and applies anti-bot protection
- Plain HTTP requests (and even headless browsers in some environments)
  may return empty or incomplete HTML
- A lightweight HTML parser with graceful fallback is implemented for the MVP
- Production-grade integration would require:
  - official API access, or
  - licensed data feeds, or
  - a dedicated rendering service

These limitations are documented intentionally to keep the MVP lightweight,
transparent, and focused on core functionality.

---

## Design Decisions

- No heavy scraping or anti-bot bypassing is used
- No headless browser is enabled by default to avoid unnecessary complexity
- Priority is given to robustness, clarity, and explainable behavior
- The goal of this implementation is to demonstrate:
  - data flow
  - duplicate protection
  - relevance scoring
  - delivery mechanics

rather than exhaustive content extraction.

---

## Tech Stack

- Python 3
- aiogram (Telegram Bot API)
- SQLite
- asyncio
- requests / feedparser / BeautifulSoup

---

## Future Improvements

- Source-specific fallback strategies (API / rendered HTML where permitted)
- More advanced relevance scoring (NLP-based models)
- Digest personalization per user
- Source health monitoring and alerting
- Deployment on VPS with unrestricted network access

---

## How to Run

```bash
pip install -r requirements.txt
python -m app.bot
```

For scheduled delivery:

```bash
python -m app.scheduler
```

## Notes

Local access to Telegram Bot API may be restricted due to network,
OS-level (e.g. Windows + IPv6), or regional limitations.
In production, this is resolved by deploying the bot on a VPS
with unrestricted network access.