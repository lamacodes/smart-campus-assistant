# Railway 환경 변수 설정 가이드

코드가 GitHub에 성공적으로 푸시되었습니다! 이제 Railway에서 다음 환경 변수들을 설정해야 합니다.

## 필수 환경 변수

Railway 프로젝트 → **Variables** 탭에서 아래 변수들을 추가하세요:

### 1. OpenAI
```
OPENAI_API_KEY=sk-...
```
`.env` 파일에서 복사

### 2. Twilio
```
TWILIO_ACCOUNT_SID=AC...
TWILIO_API_KEY_SID=SK...
TWILIO_API_KEY_SECRET=...
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```
`.env` 파일에서 복사

### 3. Google Sheets
```
GOOGLE_SHEET_ID=...
```
`.env` 파일에서 복사

### 4. Google Credentials (중요!)
```
GOOGLE_CREDENTIALS_JSON=
```

**값 설정 방법:**
1. 로컬의 `credentials.json` 파일을 텍스트 에디터로 열기
2. **전체 JSON 내용**을 복사 (예: `{"type":"service_account","project_id":"...","private_key":"..."}`)
3. Railway Variables에 붙여넣기
4. ⚠️ 줄바꿈이나 공백 없이 **한 줄로** 붙여넣어야 합니다

## 설정 완료 후
Railway가 자동으로 재배포됩니다. 배포가 완료되면 URL이 생성됩니다 (예: `https://jbnu-whatsapp-chatbot-production.up.railway.app`).
