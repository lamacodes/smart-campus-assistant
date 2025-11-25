# JBNU WhatsApp Exchange Student Assistant  
_자동화된 WhatsApp 챗봇 시스템 사양서 (AI-Agent 실행 기반)_

---

## 📌 0. 프로젝트 개요

- **서비스 이름:** JBNU WhatsApp Exchange Student Assistant
- **목표:** 해외 학생/교수/파트너 대학의 문의를 WhatsApp에서 자동 처리
- **운영자:** 전북대학교 국제교류처 직원 (비개발자)
- **사용 플랫폼:** WhatsApp Business → Twilio → Flask Backend

---

## 🎯 1. 시스템 목표 (MVP 기준)

- 24/7 WhatsApp 자동응답 챗봇 구축
- 역할 기반 사용자 분류 (Student / Professor / Partner University)
- 질문에 대해 자동 FAQ 응답
- FAQ는 **Google Sheets에서 관리**
- OpenAI API를 활용한 **NLP 기반 의미 검색 및 답변 생성**
- Webhook 기반 메시지 처리

---

## 🏛 2. 시스템 아키텍처

WhatsApp User
     ↓
WhatsApp Business (Meta)
     ↓
Twilio Webhook → POST /webhook
     ↓
Flask Server (Railway Hosting)
     ↓
User State Manager (Supabase)
     ↓
FAQ Handler
   ├─ Google Sheets API (FAQ Data)
   ├─ OpenAI Embedding Similarity Search (fallback)
   └─ Rule-based Matching backup
     ↓
Response Decision Engine
     ↓
Twilio API → WhatsApp User 응답

---

## 🧩 3. 기술 스택 명세

| 영역 | 기술 | 설명 |
|------|------|------|
| Messaging Gateway | Twilio Sandbox | WhatsApp과 서버 연결 |
| Backend | Python Flask | 간단·유지보수 쉬움 |
| Hosting | Railway Free Plan | 자동 빌드/배포 |
| State DB | Supabase (Postgres) | 사용자 상태 영구 저장 |
| FAQ Store | Google Sheets API | 비개발자 수정 가능 |
| NLP 처리 | OpenAI Embedding + GPT | 의미 기반 질문 매칭 |
| 로그∙통계 | Supabase Events Table | 향후 대시보드 활용 |

---

## 📁 4. 데이터 구조

### 4.1 사용자 세션 테이블 (Supabase)

| Column | Type | Example |
|--------|------|---------|
| user_id | TEXT (PK) | whatsapp:+8210xxxxxxx |
| role | ENUM | student/professor/partner |
| last_intent | TEXT | "ask_dormitory" |
| updated_at | TIMESTAMP | 자동갱신 |

---

### 4.2 FAQ 데이터 구조 (Google Sheets)

| Column | Example |
|--------|---------|
| question | "What is the application deadline?" |
| answer | "November 28, 2025" |
| keywords | "deadline, apply, date" |
| embedding_vector | (자동 생성, DB 저장) |

> FAQ가 변경되면 Embedding 재생성 수행.

---

## 🔧 5. 처리 로직 (AI Agent 실행 순서)

WhatsApp 메시지 수신

Twilio → Flask webhook POST

Supabase에서 user session 조회

사용자 역할 미지정이면 역할 분류 질문 유도

FAQ Matching Algorithm:

5.1 Google Sheets keyword match
5.2 Embedding similarity ≥ threshold → NLP answer
5.3 Fallback → GPT generated answer

응답 타입 결정

Twilio → WhatsApp 자동응답

로그 및 세션 업데이트 (Supabase)


---

## 🚦 6. 메시지 라우팅 규칙

| 질문 유형 | 처리 방식 |
|----------|-----------|
| 단순 FAQ | 자동응답 |
| Application 작성 요청, Dormitory 문의 | 챗봇 처리 |
| MoU, Course Mapping, 교환학생 협의 | **직원 알림 + 챗봇 회신 보류** |
| 비정형 질문 | GPT 기반 답변 생성 |
| 응답 실패 | “Human escalation” 처리 후 통보 |

알림 키워드 예시:

MoU, partnership, urgent, agreement, signing, course mapping

---

## 🛠 7. 운영자 기능 (비개발자 전용)

| 기능 | 방법 |
|------|------|
| FAQ 수정 | Google Sheets에서 직접 수정 |
| 알림 설정 | Sheets의 alert_rules 탭 |
| 서버 재시작 | Railway Dashboard |
| 로그 확인 | Supabase Dashboard |

---

## 🚀 8. 확장 로드맵

### Phase 1 (이미 적용되는 MVP 기능)
- Google Sheets 기반 FAQ 관리
- OpenAI Embedding 기반 의미 매칭
- 역할 기반 자동응답

### Phase 2 (단기 확장)
- 질문 통계 리포트 (시간대, 언어, 빈도)
- 웹 기반 대시보드
- 언어선택 자동화 (i18n) → EN/KR/FR

### Phase 3 (고도화)
- intent clustering → 자동 FAQ 생성 추천
- human-priority routing (교수/파트너 메시지 우선)
- WhatsApp → Discord/Email Notification pipeline

---

## 📌 9. KPI 지표

| 지표 | 목표 |
|------|------|
| 자동응답 처리율 | ≥ 70% |
| 평균 응답 속도 | ≤ 2초 |
| 직원 대응 필요 빈도 | ≤ 5% |
| FAQ 수정 소요 | ≤ 2분 |

---

## 🔁 10. AI Agent 작업 체크리스트

[ ] Twilio Sandbox 설정 및 Webhook 주소 연결
[ ] Flask 서버 구축 및 Railway에 배포
[ ] Supabase DB 초기화 및 테이블 생성
[ ] Google Sheets API 연결 설정
[ ] FAQ Embedding 생성 및 저장
[ ] OpenAI 기반 NLP 매칭 구현
[ ] Escalation rule 세팅
[ ] 테스트 및 운영자 가이드 전달


---

## 🧪 테스트 메시지 예시

"Hi, I want to apply. How do I start?"
→ NLP → FAQ 매칭 → 자동응답

"I represent University of Sydney. We want MoU update."
→ escalation → 직원 알림 → 챗봇 확인 메시지 전송


---

## 📚 문서 버전

- Version: `v1.0`
- Format: `Deployment-ready spec`

---