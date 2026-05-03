import feedparser
import json
from datetime import datetime

feeds = [
  "http://zmiiv-lyceum1.kh.sch.in.ua/rss",
  "https://media-zmiev.net.ua/engine/rss.php",
  "http://osvita-zm.org.ua/category/novini/feed/",
  "http://www.zmiivmisto.gov.ua/?format=feed&type=rss",
  "http://www.zmiiv-cbs.edu.kh.ua/rss",
  "https://zpf.company/feed/",
  "https://rayrada.org.ua/rss/9167/",
  "https://gomilsha.org.ua/feed/",
  "https://izum.church.ua/ru/feed/",
  "https://zmiev-societas.at.ua/news/rss/",
  "https://lycei1museum.at.ua/news/rss/",
  "http://zmiiv-school2.kh.sch.in.ua/rss",
  "https://zmiiv.com.ua/news-zmiiv/feed/",
  "https://rda.org.ua/rss/286/",
  "https://rsshub.app/telegram/channel/podslushano_zmiev",
  "https://zmiiv-service.com.ua/index.php/news?format=feed&type=rss"
]

def get_image(entry):
    # media:content
    if hasattr(entry, "media_content"):
        return entry.media_content[0].get("url")

    # links с type=image
    if hasattr(entry, "links"):
        for l in entry.links:
            if "type" in l and l.type.startswith("image"):
                return l.href

    # попытка найти <img> в summary
    if hasattr(entry, "summary"):
        import re
        match = re.search(r'<img.*?src="(.*?)"', entry.summary)
        if match:
            return match.group(1)

    return None


items = []

for url in feeds:
    feed = feedparser.parse(url)

    for e in feed.entries[:5]:
        date = e.get("published_parsed") or e.get("updated_parsed")

        if date:
            date_str = datetime(*date[:6]).isoformat()
        else:
            date_str = ""

        items.append({
            "title": e.get("title", ""),
            "link": e.get("link", ""),
            "date": date_str,
            "image": get_image(e),
            "source": url
        })

# сортировка по дате
items = sorted(items, key=lambda x: x["date"], reverse=True)

# оставляем топ-30
items = items[:30]

with open("news.json", "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)