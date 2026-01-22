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

## Data sources notes

VC.ru and RB.ru RSS feeds may occasionally return empty responses.
In this MVP version, RSS parsing is implemented, but content availability
depends on external feed stability.

For production use, HTML parsing or official APIs can be added as a fallback.
