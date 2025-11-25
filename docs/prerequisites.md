# 📋 사전 준비 사항 (Prerequisites)

프로젝트를 시작하기 위해 다음의 계정 생성 및 API Key 발급이 필요합니다.

## 1. OpenAI API Key (필수)
AI 답변 생성 및 의미 검색(Embedding)을 위해 필요합니다.
- **사이트:** [OpenAI Platform](https://platform.openai.com/)
- **준비물:** 결제 카드가 등록된 OpenAI 계정
- **할 일:**
    1. 로그인 후 Dashboard → API Keys 이동
    2. `Create new secret key` 클릭
    3. 생성된 키(`sk-...`)를 복사하여 메모장에 저장 (한 번만 보여짐)
- **예상 비용:** 초기 개발 및 테스트 시 $5 미만 예상

## 2. Twilio 계정 (필수)
WhatsApp 메시지를 주고받기 위한 게이트웨이입니다.
- **사이트:** [Twilio](https://www.twilio.com/)
- **할 일:**
    1. 회원가입 (무료 Trial 계정으로 시작 가능)
    2. Console 대시보드에서 `Account SID` 확인 및 저장
    3. **Settings > API Keys & Tokens > API Keys** 로 이동
    4. `Create API Key` 클릭 (Standard 타입) → **API Key SID**와 **API Key Secret**를 안전한 곳에 저장 (Secret은 다시 볼 수 없음)
    5. **Messaging > Try it out > Send a WhatsApp message** 메뉴로 이동
    6. Sandbox 활성화 (화면에 보이는 코드를 WhatsApp으로 전송하여 테스트)

## 3. Google Cloud Platform (GCP) & Sheets API (필수)
FAQ 데이터를 Google Sheets에서 불러오기 위해 필요합니다.
- **사이트:** [Google Cloud Console](https://console.cloud.google.com/)
- **할 일:**
    1. 새 프로젝트 생성 (예: `jbnu-chatbot`)
    2. **API 및 서비스 > 라이브러리** 이동 → `Google Sheets API` 사용(Enable) 클릭
    3. **API 및 서비스 > 사용자 인증 정보(Credentials)** 이동 → **서비스 계정(Service Account)** 만들기
    4. 생성된 서비스 계정 이메일(`...iam.gserviceaccount.com`) 복사
    5. **키(Keys)** 탭에서 `키 추가` > `새 키 만들기` > `JSON` 선택하여 다운로드
    6. 다운로드된 JSON 파일 이름을 `credentials.json`으로 변경하고 프로젝트 루트에 저장
    7. `.env` 파일에 `GOOGLE_CREDENTIALS_JSON=credentials.json` 설정

## 4. Google Sheet 생성 (데이터)
- **할 일:**
    1. 구글 스프레드시트 새 문서 생성
    2. 위에서 복사한 **서비스 계정 이메일**(`...iam.gserviceaccount.com`)을 해당 시트의 **공유(Share)** 멤버로 추가 (편집자 권한 필수)
    3. 시트의 URL에서 `/d/`와 `/edit` 사이의 ID 값을 복사
    4. `.env` 파일에 `GOOGLE_SHEET_ID=...` 설정

## 5. Railway 계정 (배포용)
서버를 무료로 호스팅하기 위해 사용합니다.
- **사이트:** [Railway](https://railway.app/)
- **할 일:**
    1. GitHub 계정으로 로그인
    2. (선택사항) 결제 수단 등록 없이도 Trial 사용 가능하나, 안정적인 사용을 위해 확인 필요

---

## 💰 비용 모니터링 및 주의사항 (Cost & Limits)

API 사용에 따른 예상 비용과 한도를 미리 확인하세요.

### 1. OpenAI (AI 모델)
- **비용 구조:** 사용한 토큰(Token) 단위로 과금
    - GPT-3.5-turbo: 입력 $0.50 / 1M 토큰, 출력 $1.50 / 1M 토큰 (매우 저렴)
    - Embedding (text-embedding-3-small): $0.02 / 1M 토큰 (거의 무료 수준)
- **확인 방법:** [OpenAI Usage Dashboard](https://platform.openai.com/usage)
- **주의사항:**
    - `Hard Limit`을 설정하여 예산 초과 방지 (예: 월 $10)
    - 무한 루프에 빠지지 않도록 코드 작성 시 주의

### 2. Twilio (WhatsApp)
- **비용 구조:** 대화(Conversation) 단위 과금 (24시간 창)
    - **Service Conversation (유저가 먼저 말검):** 약 $0.03 ~ $0.05 (국가별 상이)
    - **Sandbox:** 무료 (테스트용)
- **확인 방법:** [Twilio Console](https://console.twilio.com/) > Billing > Usage
- **주의사항:**
    - Sandbox 환경에서는 비용이 들지 않으나, 정식 번호 사용 시 비용 발생
    - 메시지를 너무 많이 보내지 않도록 로직 점검

### 3. Google Sheets API
- **비용:** 무료 (개인/소규모 프로젝트 기준)
- **제한(Quota):** 분당 60회 읽기/쓰기 제한
- **주의사항:**
    - 챗봇이 매번 시트를 읽으면 제한에 걸릴 수 있음
    - **해결책:** 서버 시작 시 한 번 읽어서 메모리에 저장(Caching)하는 방식 사용 (이미 설계에 반영됨)

---

## 🔑 키/ID 정리표
아래 내용을 채워두시면 개발 설정이 매우 빨라집니다.

| 항목 | 값 (Value) | 비고 |
|------|------------|------|
| **OpenAI API Key** | `sk-...` | |
| **Twilio Account SID** | `AC...` | |
| **Twilio API Key SID** | `SK...` | Auth Token 대신 사용 권장 |
| **Twilio API Key Secret** | `...` | |
| **Google Service Account JSON** | `파일 보유` | 프로젝트 폴더에 저장 예정 |
| **Google Sheet ID** | `...` | URL의 `/d/` 와 `/edit` 사이 문자열 |
