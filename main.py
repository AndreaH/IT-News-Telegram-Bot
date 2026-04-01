import os
import requests
import feedparser
from datetime import datetime

# 환경 변수 (GitHub Secrets에 등록 필수)
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY') # 요약용

def summarize_text(text):
    """GPT를 이용한 뉴스 3줄 요약 (OpenAI 미사용 시 원문 리턴)"""
    if not OPENAI_API_KEY:
        return text[:150] + "..."
        
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "너는 IT 전문 요약가야. 핵심 내용을 한국어 3줄 이내로 요약해줘."},
            {"role": "user", "content": text}
        ]
    }
    res = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)
    return res.json()['choices'][0]['message']['content']

def get_news_and_send():
    rss_url = "https://news.google.com/rss/search?q=AI+technology+when:1d&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(rss_url)
    
    if not feed.entries:
        print("수집된 뉴스가 없습니다.")
        return

    # 최신 뉴스 3개만 요약해서 전송
    for entry in feed.entries[:3]:
        summary = summarize_text(entry.title)
        
        # HTML 태그 제거 및 메시지 구성 (Markdown 대신 HTML 모드가 특수문자 에러에 더 강함)
        message = (
            f"🚀 <b>AI/IT 뉴스 요약</b>\n\n"
            f"📌 <b>{entry.title}</b>\n"
            f"📝 {summary}\n\n"
            f"<a href='{entry.link}'>👉 기사 원문 보기</a>"
        )

        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML", # Markdown보다 특수문자 충돌이 적음
            "disable_web_page_preview": False
        }
        
        response = requests.post(url, json=payload)
        print(f"전송 결과: {response.status_code}, {response.text}")

if __name__ == "__main__":
    get_news_and_send()
