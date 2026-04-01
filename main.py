import os
import requests
import feedparser
import google.generativeai as genai
from datetime import datetime

# 환경 변수 설정
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# Gemini API 설정
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def get_summarized_content_with_gemini(news_list):
    """Gemini를 사용하여 뉴스 리스트를 3단 레이아웃 형식으로 요약"""
    if not GEMINI_API_KEY:
        return "Gemini API Key가 설정되지 않았습니다."

    titles = "\n".join([f"- {n['title']}" for n in news_list])
    
    prompt = f"""
    당신은 IT 및 금융 전문 칼럼니스트입니다. 아래 제공된 뉴스 리스트를 바탕으로 텔레그램 뉴스 레터를 작성하세요.
    
    [반드시 준수해야 할 형식]:
    1. 🌏 글로벌 매크로 (Global Macro)
    2. 🇰🇷 국내 주요 이슈 (Domestic Issues)
    3. 💡 시장 테마 (Market Theme)
    
    [작성 규칙]:
    - 각 섹션마다 2개씩 핵심 내용을 선정하여 '• 제목 \n ㄴ 설명' 형식으로 요약하세요.
    - 설명은 한국어로 2줄 이내로 간결하고 전문적으로 작성하세요.
    - 마지막에는 '🔍 오늘의 핵심 용어' 2개를 선정해서 <code>태그로 감싸 설명하세요.
    - 텔레그램 HTML 파싱을 위해 중요 키워드는 <b>태그를 사용하세요.
    
    뉴스 리스트:
    {titles}
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"요약 도중 오류가 발생했습니다: {str(e)}"

def send_telegram_layout():
    # 1. 뉴스 데이터 수집
    rss_url = "https://news.google.com/rss/search?q=AI+경제+IT+when:1d&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(rss_url)
    news_list = [{"title": e.title, "link": e.link} for e in feed.entries[:10]]

    if not news_list:
        print("수집된 뉴스가 없습니다.")
        return

    # 2. Gemini 요약 수행
    content = get_summarized_content_with_gemini(news_list)

    # 3. 최종 메시지 구성
    today_str = datetime.now().strftime('%Y년 %m월 %d일')
    header = f"📅 <b>{today_str} 주요 뉴스 브리핑</b>\n━━━━━━━━━━━━━━━━━━\n"
    footer = f"\n━━━━━━━━━━━━━━━━━━\n🍀 <i>활기찬 하루 보내시길 바랍니다!</i>"
    
    full_message = header + content + footer

    # 4. 텔레그램 전송
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": full_message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    
    res = requests.post(url, json=payload)
    print(f"전송 상태: {res.status_code}")

if __name__ == "__main__":
    send_telegram_layout()
