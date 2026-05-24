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
            {"name": "Google News", "url": "https://news.google.com/rss/search?q=ChatGPT+Claude+Gemini+大語言模型&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"},
            {"name": "Google News", "url": "https://news.google.com/rss/search?q=AI+晶片+算力+資料中心&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"},
            {"name": "Reuters Tech", "url": "https://feeds.reuters.com/reuters/technologyNews"},
            {"name": "BBC 科技", "url": "http://feeds.bbci.co.uk/news/technology/rss.xml"},
            {"name": "Google News EN", "url": "https://news.google.com/rss/search?q=artificial+intelligence+OpenAI+Nvidia&hl=en-US&gl=US&ceid=US:en"},
        ]
    },
    {
        "category": "台海 & 中美",
        "sources": [
            {"name": "Google News", "url": "https://news.google.com/rss/search?q=台灣+中美關係+台海&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"},
            {"name": "Google News", "url": "https://news.google.com/rss/search?q=兩岸關係+解放軍+美台&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"},
            {"name": "Google News", "url": "https://news.google.com/rss/search?q=中美貿易戰+關稅+制裁&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"},
            {"name": "BBC 中文", "url": "https://feeds.bbci.co.uk/zhongwen/trad/rss.xml"},
            {"name": "Reuters 地緣", "url": "https://feeds.reuters.com/reuters/worldNews"},
            {"name": "Google News EN", "url": "https://news.google.com/rss/search?q=Taiwan+China+US+relations&hl=en-US&gl=US&ceid=US:en"},
        ]
    },
    {
        "category": "科技公司",
        "sources": [
            {"name": "Google News", "url": "https://news.google.com/rss/search?q=Apple+蘋果+新品&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"},
            {"name": "Google News", "url": "https://news.google.com/rss/search?q=Tesla+特斯拉+電動車&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"},
            {"name": "Google News", "url": "https://news.google.com/rss/search?q=Google+Meta+Microsoft+科技巨頭&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"},
            {"name": "Google News", "url": "https://news.google.com/rss/search?q=台積電+TSMC+半導體&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"},
            {"name": "Reuters Tech", "url": "https://feeds.reuters.com/reuters/technologyNews"},
            {"name": "Google News EN", "url": "https://news.google.com/rss/search?q=Apple+Tesla+Google+Meta+earnings&hl=en-US&gl=US&ceid=US:en"},
        ]
    },
    {
        "category": "總體經濟",
        "sources": [
            {"name": "Google News", "url": "https://news.google.com/rss/search?q=Fed+聯準會+利率+降息&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"},
            {"name": "Google News", "url": "https://news.google.com/rss/search?q=通膨+油價+黃金+美元&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"},
            {"name": "Google News", "url": "https://news.google.com/rss/search?q=美股+台股+股市+經濟&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"},
            {"name": "Google News", "url": "https://news.google.com/rss/search?q=比特幣+加密貨幣+BTC&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"},
            {"name": "Reuters 經濟", "url": "https://feeds.reuters.com/reuters/businessNews"},
            {"name": "Google News EN", "url": "https://news.google.com/rss/search?q=Federal+Reserve+inflation+economy&hl=en-US&gl=US&ceid=US:en"},
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

def fetch_category(category_name, sources, max_per_source=8):
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
                # 去掉重複（標題前 15 字相同就算重複）
                key = title[:15]
                if not title or key in seen_titles:
                    continue
                seen_titles.add(key)
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
