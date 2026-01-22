from datetime import datetime

def format_published_at(value: str | None) -> str:
    if not value:
        return "unknown date"

    try:
        dt = datetime.fromisoformat(value)
        return dt.strftime("%d %b %Y %H:%M")
    except Exception:
        return "unknown date"
