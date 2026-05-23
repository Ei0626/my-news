import feedparser
import json
import os
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

FEEDS = [
    {
        "category": "AI 科技",
        "sources": [
            {"name": "Google News", "url": "https://news.google.com/rss/search?q=AI+人工智慧+Nvidia+OpenAI&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"},
            {"name": "Reuters Tech", "url": "https://feeds.reuters.com/reuters/technologyNews"},
        ]
    },
    {
        "category": "台海 & 中美",
        "sources": [
            {"name": "Google News", "url": "https://news.google.com/rss/search?q=台灣+中美關係+台海&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"},
            {"name": "BBC 中文", "url": "https://feeds.bbci.co.uk/zhongwen/trad/rss.xml"},
        ]
    },
    {
        "category": "科技公司",
        "sources": [
            {"name": "Google News", "url": "https://news.google.com/rss/search?q=Apple+Tesla+Google+Meta+科技&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"},
        ]
    },
    {
        "category": "總體經濟",
        "sources": [
            {"name": "Google News", "url": "https://news.google.com/rss/search?q=Fed+利率+通膨+油價+美債&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"},
        ]
    },
]

def parse_date(entry):
    try:
        if hasattr(entry, "published"):
            dt = parsedate_to_datetime(entry.published)
            return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        pass
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def fetch_category(category_name, sources, max_per_source=5):
    items = []
    seen_titles = set()
    for src in sources:
        try:
            feed = feedparser.parse(src["url"])
            count = 0
            for entry in feed.entries:
                if count >= max_per_source:
                    break
                title = entry.get("title", "").strip()
                if not title or title in seen_titles:
                    continue
                seen_titles.add(title)
                items.append({
                    "title": title,
                    "link": entry.get("link", ""),
                    "source": src["name"],
                    "date": parse_date(entry),
                })
                count += 1
        except Exception as e:
            print(f"[WARN] Failed to fetch {src['url']}: {e}")
    return items

def main():
    result = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "categories": []
    }
    for feed_cfg in FEEDS:
        items = fetch_category(feed_cfg["category"], feed_cfg["sources"])
        result["categories"].append({
            "name": feed_cfg["category"],
            "items": items
        })
        print(f"[OK] {feed_cfg['category']}: {len(items)} items")

    out_path = os.path.join(os.path.dirname(__file__), "..", "data", "news.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"[DONE] Saved to {out_path}")

if __name__ == "__main__":
    main()
