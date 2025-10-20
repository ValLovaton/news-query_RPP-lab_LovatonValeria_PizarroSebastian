from __future__ import annotations
from typing import List, Dict, Any, Optional
import os, json
import feedparser

DEFAULT_FEED = "https://rpp.pe/rss"

def load_rpp_rss(limit: int = 50, feed_url: str = DEFAULT_FEED, export_path: Optional[str] = None) -> List[Dict[str, Any]]:

    d = feedparser.parse(feed_url)
    if getattr(d, "bozo", 0):
        # Warning no bloqueante si el feed viene mal formado
        print(f"[warn] feedparser bozo={getattr(d, 'bozo_exception', '1')}. Intentando continuar.")
    entries = getattr(d, "entries", []) or []
    items: List[Dict[str, Any]] = []
    for e in entries[:limit]:
        items.append({
            "title": e.get("title", ""),
            "description": e.get("summary", ""),
            "link": e.get("link", ""),
            "date_published": e.get("published", ""),
        })
    if export_path:
        os.makedirs(os.path.dirname(export_path), exist_ok=True)
        with open(export_path, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
    return items

