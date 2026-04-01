# 🚀 IT & AI Trend Telegram Bot

Google Gemini API와 GitHub Actions를 활용한 스마트 뉴스 브리핑 봇입니다.

## 📌 주요 기능
- **자동 스크래핑:** Google News RSS 기반 실시간 데이터 수집
- **AI 인사이트:** Gemini 1.5 Flash 모델의 3단 레이아웃 요약
- **정기 발송:** 매일 아침 오전 8시 20분경 텔레그램 전송
- **HTML 가독성:** 전문 뉴스레터 형식의 레이아웃 적용

## ⚙️ 설정 방법 (Secrets)
GitHub Settings -> Secrets -> Actions에 다음 항목을 등록하세요:
1. `TELEGRAM_TOKEN`: 봇 토큰
2. `TELEGRAM_CHAT_ID`: 수신자 ID
3. `GEMINI_API_KEY`: Gemini API 키

## 📂 파일 구조
- `main.py`: 메인 로직
- `.github/workflows/news_bot.yml`: 자동화 설정
- `requirements.txt`: 의존성 라이브러리
