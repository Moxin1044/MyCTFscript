import requests
from bs4 import BeautifulSoup

url = "https://ai-bot.cn/daily-ai-news/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}


def fetch_ai_news(limit=5):
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    first_block = soup.find("div", class_="news-list")

    if not first_block:
        return []

    date_tag = first_block.find("div", class_="news-date")
    date = date_tag.text.strip() if date_tag else "未知日期"

    all_news = []

    for item in first_block.find_all("div", class_="news-item"):
        content_div = item.find("div", class_="news-content")
        if not content_div:
            continue

        title_tag = content_div.find("h2")
        a_tag = title_tag.find("a") if title_tag else None
        title = a_tag.text.strip() if a_tag else "无标题"
        link = a_tag['href'] if a_tag and a_tag.has_attr("href") else "无链接"

        p_tag = content_div.find("p")
        summary = p_tag.get_text(strip=True) if p_tag else "无摘要"

        source = "未知来源"
        source_span = p_tag.find("span", class_="news-time") if p_tag else None
        if source_span:
            source = source_span.text.replace("来源：", "").strip()

        all_news.append({
            "date": date,
            "title": title,
            "link": link,
            "summary": summary,
            "source": source
        })

        if len(all_news) >= limit:
            break

    return all_news


# 示例调用
if __name__ == "__main__":
    news_list = fetch_ai_news(limit=5)
    for news in news_list:
        print(f"📅 日期：{news['date']}")
        print(f"📰 标题：{news['title']}")
        print(f"🔗 链接：{news['link']}")
        print(f"📄 摘要：{news['summary']}")
        print(f"📌 来源：{news['source']}")
        print("-" * 80)
