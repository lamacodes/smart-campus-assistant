# Smart Campus Assistant

UNIV 국제교류처를 위한 AI 기반 왓츠앱 챗봇으로, 학생들의 문의에 자동으로 답변해줍니다. 이 프로젝트는 OpenAI의 GPT와 임베딩(Embeddings)을 활용하여 Google Sheets FAQ 데이터베이스를 기반으로 정확하고 문맥에 맞는 답변을 제공합니다.

## 📚 문서 (Documentation)
- **[프로젝트 기획서](docs/project_proposal.md)**: 상세한 프로젝트 목표, 아키텍처 및 로드맵.
- **[사전 준비 사항](docs/prerequisites.md)**: 필요한 계정 및 API 키 (OpenAI, Twilio, Google Cloud).
- **[배포 가이드](docs/deployment_guide.md)**: Railway 배포를 위한 단계별 가이드.

## ✨ 주요 기능 (Features)
- **24/7 자동 응답**: 교환 학생 프로그램, 기숙사, 비자 등에 대한 일반적인 질문에 즉시 답변합니다.
- **AI 기반 검색**: OpenAI 임베딩을 사용하여 키워드가 정확히 일치하지 않아도 가장 관련성 높은 FAQ 항목을 찾습니다.
- **스마트 대체 응답 (Fallback)**: 일치하는 FAQ가 없을 경우, GPT-3.5가 정중한 대체 응답을 생성합니다.
- **쉬운 관리**: FAQ 데이터는 Google Sheets에서 관리되므로 비개발자 직원도 쉽게 수정할 수 있습니다.
- **설정 가능**: `config.py`에서 설정을 중앙 집중식으로 관리합니다.

## 🚀 빠른 시작 (로컬 실행)

### 1. 복제 및 설치
```bash
git clone https://github.com/lamacodes/smart-campus-assistant.git
cd smart-campus-assistant
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 환경 설정
1. **환경 변수**: `.env.example`을 `.env`로 복사하고 API 키를 입력합니다.
   ```bash
   cp .env.example .env
   ```
   *키 발급 방법은 [사전 준비 사항](docs/prerequisites.md)을 참고하세요.*

2. **Google 자격 증명**: `credentials.json` 파일을 프로젝트 루트에 위치시킵니다.

3. **앱 설정**: `config.py`를 열어 다음을 사용자 정의합니다:
   - 대학 이름 및 이메일
   - OpenAI 모델 설정
   - FAQ 매칭 임계값

### 3. 로컬 실행
```bash
python app.py
```
서버는 `http://localhost:5002` (또는 설정된 PORT)에서 시작됩니다.

## ☁️ 배포 (Deployment)

상세한 과정은 **[배포 가이드](docs/deployment_guide.md)**를 참고하세요.

### 옵션 1: Railway 대시보드 (간편함)
GitHub 저장소를 Railway에 연결하고 대시보드에서 환경 변수를 추가합니다.

### 옵션 2: Railway CLI (고급)
커맨드 라인을 선호한다면, 프로젝트 설정과 변수를 직접 설정할 수 있습니다:

1. **로그인 및 초기화**
   ```bash
   railway login
   railway init
   ```

2. **변수 설정** (값을 본인의 것으로 변경하세요)
   ```bash
   railway variables --set "OPENAI_API_KEY=sk-..."
   railway variables --set "TWILIO_ACCOUNT_SID=AC..."
   railway variables --set "TWILIO_API_KEY_SID=SK..."
   railway variables --set "TWILIO_API_KEY_SECRET=..."
   railway variables --set "TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886"
   railway variables --set "GOOGLE_SHEET_ID=..."
   # Google 자격 증명의 경우, 전체 JSON 문자열을 사용합니다 (먼저 줄바꿈을 제거하세요)
   railway variables --set "GOOGLE_CREDENTIALS_JSON=$(cat credentials.json | tr -d '\n')"
   ```

3. **배포**
   ```bash
   railway up
   ```

## 🧪 테스트 (Testing)

포함된 테스트 스크립트를 실행하여 연결을 확인하세요:

```bash
# Google Sheets 연결 테스트
python tests/test_sheets.py

# OpenAI 임베딩 및 검색 테스트
python tests/test_openai.py
```

## 📂 프로젝트 구조
```
chatbot-wechat/
├── app.py                      # 메인 Flask 애플리케이션
├── config.py                   # 중앙 설정 파일
├── services/                   # 비즈니스 로직 모듈
│   ├── twilio_service.py       # 왓츠앱 메시징
│   ├── gsheets_service.py      # FAQ 데이터 로더
│   ├── openai_service.py       # AI 임베딩 및 검색
│   └── session_service.py      # 사용자 세션 관리
├── docs/                       # 문서 파일
├── tests/                      # 테스트 스크립트
├── requirements.txt            # Python 의존성
└── Procfile                    # 배포 설정
```

## 라이선스 (License)
MIT

