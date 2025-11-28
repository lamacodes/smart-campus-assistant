# 배포 가이드 (Deployment Guide)

## Railway 배포

1. **Git 저장소 초기화**
   ```bash
   cd chatbot-wechat
   git init
   git add .
   git commit -m "Initial commit: UNIV WhatsApp Chatbot"
   ```

2. **GitHub 저장소 생성**
   - https://github.com/new 로 이동합니다.
   - 새 저장소를 생성합니다 (예: `univ-whatsapp-chatbot`). **README로 초기화하지 마세요.**
   - 저장소 URL을 복사합니다.

3. **GitHub에 푸시**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/univ-whatsapp-chatbot.git
   git branch -M main
   git push -u origin main
   ```

4. **Railway에 배포**
   - Railway 대시보드(https://railway.app/dashboard)를 엽니다.
   - **New Project** → **Deploy from GitHub repo**를 클릭합니다.
   - `univ-whatsapp-chatbot` 저장소를 선택합니다.
   - Railway가 `Procfile`을 감지하고 배포를 시작합니다.

## 환경 변수 설정 (Railway)

Railway 프로젝트의 **Variables** 탭에서 다음 변수들을 추가하세요:

- **OpenAI**
  ```
  OPENAI_API_KEY=sk-...
  ```
- **Twilio** (API Key 모드)
  ```
  TWILIO_ACCOUNT_SID=AC...
  TWILIO_API_KEY_SID=SK...
  TWILIO_API_KEY_SECRET=...
  TWILIO_WHATSAPP_NUMBER=whatsapp:+1234567890
  ```
- **Google Sheets**
  ```
  GOOGLE_SHEET_ID=...
  ```
- **Google Credentials** (전체 JSON을 한 줄로)
  ```
  GOOGLE_CREDENTIALS_JSON={"type":"service_account",...}
  ```

> **중요:** `credentials.json`의 전체 JSON 내용을 줄바꿈 없이 한 줄로 붙여넣으세요.

변수를 저장하면 Railway가 자동으로 서비스를 재배포합니다.

## Twilio 웹훅 설정

1. Twilio Console (https://console.twilio.com/)에 로그인합니다.
2. **Messaging** → **Try it out** → **Send a WhatsApp message**로 이동합니다.
3. **Sandbox settings**에서 **"When a message comes in"** 섹션을 찾습니다.
4. 웹훅 URL을 다음과 같이 설정합니다:
   ```
   https://your-project-name.up.railway.app/webhook
   ```
5. 방식을 **POST**로 선택하고 **Save**를 클릭합니다.

## 테스트

- Twilio Sandbox 번호(예: `whatsapp:+14155238886`)로 왓츠앱 메시지를 보냅니다.
- 시도해볼 질문: "When is the deadline?"
- 봇이 올바른 FAQ 답변(**2025년 11월 28일입니다.**)으로 응답해야 합니다.

## 문제 해결 (Troubleshooting)

- **Railway 로그:** Project → Deployments → View logs.
- **Twilio 로그:** Console → Monitor → Logs.
- 모든 환경 변수가 올바르게 설정되었는지, 공백이나 줄바꿈이 포함되지 않았는지 확인하세요.

---

*이 가이드는 이전의 Railway 배포, 환경 변수, Twilio 웹훅 문서를 하나의 참조로 통합한 것입니다.*
