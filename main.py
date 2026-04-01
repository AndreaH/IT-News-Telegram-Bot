import os
import requests
import feedparser
from datetime import datetime

# 환경 변수 (GitHub Secrets)
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

def get_summarized_content(news_list):
    """GPT를 사용하여 뉴스 리스트를 3단 레이아웃 형식으로 요약"""
    if not OPENAI_API_KEY:
        return "OpenAI API Key가 설정되지 않았습니다."

    # 뉴스 제목들을 하나로 합쳐서 전달
    titles = "\n".join([f"- {n['title']}" for n in news_list])
    
    prompt = f"""
    아래 뉴스 리스트를 바탕으로 텔레그램 뉴스 레터를 작성해줘.
    형식은 반드시 다음 3단 레이아웃을 지켜야 해:
    
    1. 글로벌 매크로 (Global Macro)
    2. 국내 주요 이슈 (Domestic Issues)
    3. 시장 테마 (Market Theme)
    
    각 섹션마다 2개씩 핵심 내용을 '• 제목 \n ㄴ 설명' 형식으로 요약해줘.
    마지막에는 '오늘의 핵심 용어' 2개를 선정해서 설명해줘.
    톤앤매너는 전문가적이면서도 희망차게 작성해줘.
    
    뉴스 리스트:
    {titles}
    """

    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "너는 금융 및 IT 전문 칼럼니스트야. HTML 태그(<b>, <code>)를 적절히 섞어서 가독성 좋게 작성해."},
            {"role": "user", "content": prompt}
        ]
    }
    res = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)
    return res.json()['choices'][0]['message']['content']

def send_telegram_layout():
    # 1. 뉴스 데이터 수집 (AI 및 경제 키워드 조합)
    rss_url = "https://news.google.com/rss/search?q=AI+경제+IT+when:1d&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(rss_url)
    news_list = [{"title": e.title, "link": e.link} for e in feed.entries[:10]]

    # 2. GPT 요약 (3단 레이아웃 적용)
    content = get_summarized_content(news_list)

    # 3. 최종 메시지 조립
    today = datetime.now().strftime('%Y년 %m월 %d일')
    header = f"📅 <b>{today} 주요 뉴스 브리핑</b>\n━━━━━━━━━━━━━━━━━━\n"
    footer = f"\n━━━━━━━━━━━━━━━━━━\n🍀 <i>활기찬 하루 보내시길 바랍니다!</i>"
    
    full_message = header + content + footer

    # 4. 전송
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": full_message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    
    response = requests.post(url, json=payload)
    print(f"전송 결과: {response.status_code}")

if __name__ == "__main__":
    send_telegram_layout()
