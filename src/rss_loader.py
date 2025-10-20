# src/rss_loader.py
from __future__ import annotations
from typing import List, Dict, Any
import feedparser

DEFAULT_FEED = "https://rpp.pe/rss"

def load_rpp_rss(limit: int = 50, feed_url: str = DEFAULT_FEED) -> List[Dict[str, Any]]:

    d = feedparser.parse(feed_url)
    items: List[Dict[str, Any]] = []
    for e in d.entries[:limit]:
        items.append({
            "title": e.get("title", ""),
            "description": e.get("summary", ""),
            "link": e.get("link", ""),
            "date_published": e.get("published", ""),
        })
    return items
