import os
import requests
import feedparser
from datetime import datetime

# 환경 변수 로드 (GitHub Secrets)
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def get_latest_news():
    # 구글 뉴스 RSS (AI/IT 관련 키워드 검색 결과)
    rss_url = "https://news.google.com/rss/search?q=AI+technology+when:1d&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(rss_url)
    
    news_items = []
    # 최신 뉴스 5개만 추출
    for entry in feed.entries[:5]:
        news_items.append({
            'title': entry.title,
            'link': entry.link,
            'source': entry.source.get('title', 'Unknown')
        })
    return news_items

def send_telegram_msg(items):
    if not items:
        return

    message = f"📢 *오늘의 IT/AI 주요 뉴스 ({datetime.now().strftime('%Y-%m-%d')})*\n\n"
    for i, item in enumerate(items, 1):
        # 텔레그램 MarkdownV2 스타일 적용 (특수문자 escape 처리 필요할 수 있음)
        message += f"{i}. [{item['title']}]({item['link']})\n(출처: {item['source']})\n\n"

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    
    requests.post(url, json=payload)

if __name__ == "__main__":
    news = get_latest_news()
    send_telegram_msg(news)