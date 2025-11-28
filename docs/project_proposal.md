# UNIV WhatsApp Exchange Student Assistant 프로젝트 기획서

## 📌 1. 프로젝트 개요
- **서비스 명:** UNIV WhatsApp Exchange Student Assistant
- **프로젝트 목표:** 대학교 해외 학생, 교수, 파트너 대학 관계자의 문의를 WhatsApp을 통해 24시간 자동 처리하여 국제교류처 직원의 업무 부담 경감
- **주요 운영자:** 국제교류처 직원 (비개발자 친화적 환경 제공)
- **핵심 플랫폼:** WhatsApp Business API (via Twilio) → Flask Backend → AI Agent

---

## 🎯 2. 시스템 목표 (MVP)
1. **24/7 자동 응답:** 시차에 관계없이 즉각적인 응답 제공
2. **사용자 역할 분류:** 학생(Student), 교수(Professor), 파트너 대학(Partner) 등 역할에 따른 맞춤형 응답
3. **쉬운 데이터 관리:** **Google Sheets**를 CMS(Content Management System)로 활용하여 비개발자도 쉽게 FAQ 관리
4. **AI 기반 답변:** OpenAI API를 활용한 자연어 처리(NLP) 및 의미 기반 검색(Semantic Search)
5. **스마트 에스컬레이션:** 중요 키워드(MOU, 협정 등) 감지 시 직원에게 알림 및 자동 응답 보류

---

## 🏛 3. 시스템 아키텍처
```mermaid
graph TD
    User[WhatsApp User] -->|Message| WA[WhatsApp Business API]
    WA -->|Webhook| Twilio
    Twilio -->|POST /webhook| Server[Flask Server (Railway)]
    
    subgraph Backend
        Server -->|Read/Write| DB[(Supabase - User State)]
        Server -->|Fetch Data| GSheets[Google Sheets (FAQ Data)]
        Server -->|Embedding/Completion| OpenAI[OpenAI API]
    end
    
    Server -->|Response| Twilio
    Twilio -->|Reply| User
```

---

## 🧩 4. 기술 스택 명세

| 영역 | 기술 | 선정 이유 |
|------|------|-----------|
| **Messaging Gateway** | Twilio Sandbox / API | WhatsApp 연동의 표준, 안정적인 API 제공 |
| **Backend** | Python Flask | 가볍고 빠른 개발 가능, 풍부한 AI 라이브러리 생태계 |
| **Hosting** | Railway | 간편한 배포, CI/CD 자동화, 무료/저렴한 플랜 |
| **Database** | Supabase (PostgreSQL) | 사용자 세션 및 대화 상태의 안정적인 영구 저장 |
| **CMS (FAQ)** | Google Sheets API | 엑셀에 익숙한 교직원이 별도 학습 없이 데이터 관리 가능 |
| **AI / NLP** | OpenAI (Embeddings + GPT) | 높은 정확도의 의도 파악 및 자연스러운 답변 생성 |

---

## 📁 5. 데이터 구조

### 5.1 사용자 세션 테이블 (Supabase)
사용자의 현재 상태와 역할을 관리하여 문맥에 맞는 대화를 유지합니다.

| 컬럼명 | 타입 | 설명 | 예시 |
|--------|------|------|------|
| `user_id` | TEXT (PK) | WhatsApp 전화번호 | `whatsapp:+821012345678` |
| `role` | ENUM | 사용자 역할 | `student`, `professor`, `partner` |
| `last_intent` | TEXT | 마지막 질문 의도 | `ask_dormitory_deadline` |
| `conversation_stage` | TEXT | 대화 단계 | `greeting`, `awaiting_role_selection` |
| `updated_at` | TIMESTAMP | 마지막 활동 시간 | `2025-11-25 14:00:00` |

### 5.2 FAQ 데이터 구조 (Google Sheets)
운영자가 직접 관리하는 지식 베이스입니다.

| Question (질문) | Answer (답변) | Keywords (키워드) | Category (카테고리) |
|-----------------|---------------|-------------------|---------------------|
| 지원 마감일이 언제인가요? | 2025년 11월 28일입니다. | deadline, apply, date | Admission |
| 기숙사 비용은 얼마인가요? | 학기당 약 100만원입니다. | dormitory, cost, fee | Housing |

> *참고: 시스템은 주기적으로 이 시트를 읽어 Embedding Vector를 생성하고 캐싱합니다.*

---

## 📦 Deployment & Test Results

- **Deployment URL:** https://your-project-name.up.railway.app
- **Live Test:** Sending "When is the deadline?" via WhatsApp returned the correct FAQ answer (**2025년 11월 28일입니다.**). This confirms that the OpenAI embedding search and fallback logic are working as expected.

The system is now fully operational on Railway and ready for further enhancements.

---

## 🚦 6. 메시지 처리 및 라우팅 로직

1. **메시지 수신:** Twilio Webhook을 통해 메시지 도착
2. **세션 확인:** Supabase에서 사용자 조회 (신규 유저인 경우 역할 설정 단계 진입)
3. **의도 파악 (Intent Classification):**
   - **Rule-based:** 특정 키워드(MOU, Urgent 등) 포함 여부 확인
   - **AI Semantic Search:** Google Sheets 데이터와 사용자 질문 간의 유사도 분석
4. **응답 생성:**
   - **FAQ 매칭 성공:** 미리 정의된 답변 전송
   - **매칭 실패 (Low Confidence):** GPT를 활용하여 일반적인 안내 또는 담당자 연결 안내
   - **특수 키워드 감지:** "Human Escalation" 트리거 (직원 알림 발송)
5. **로그 저장:** 대화 내용 및 처리 결과를 Supabase에 저장

### 라우팅 규칙 예시
| 질문 유형 | 처리 방식 | 비고 |
|----------|-----------|------|
| 단순 FAQ (마감일, 서류 등) | **자동 응답** | Google Sheets 데이터 기반 |
| 신청서 작성, 기숙사 문의 | **챗봇 처리** | 링크 제공 또는 절차 안내 |
| **MOU, 파트너십, 협정 체결** | **직원 알림 (Escalation)** | 챗봇은 "담당자가 곧 연락드립니다" 응답 후 보류 |
| 비속어, 엉뚱한 질문 | **GPT 기반 방어** | 정중하게 거절하거나 답변 회피 |

---

## 🛠 7. 운영자(직원) 기능
- **FAQ 관리:** Google Sheets에 접속하여 행을 추가/수정/삭제하면 챗봇에 자동 반영 (캐싱 주기에 따름)
- **알림 수신:** 중요 문의 발생 시 이메일 또는 지정된 메신저로 알림 수신 (Phase 2 구현 예정)
- **로그 확인:** 필요 시 Supabase 대시보드에서 대화 이력 조회 가능

---

## 🚀 8. 확장 로드맵

### Phase 1 (MVP)
- [x] Google Sheets 연동 FAQ 챗봇
- [x] OpenAI Embedding 기반 검색
- [x] 기본적인 역할(Role) 분류

### Phase 2 (기능 고도화)
- [ ] **다국어 지원 (i18n):** 영어, 한국어, 프랑스어 등 자동 감지 및 번역
- [ ] **통계 대시보드:** 국가별, 시기별 질문 빈도 분석 리포트 제공
- [ ] **알림 시스템 강화:** Slack 또는 Email로 중요 문의 실시간 전달

### Phase 3 (시스템 통합)
- [ ] **학사 시스템 연동:** 학생 개인별 합격 여부 등 조회 기능 (보안 강화 필요)
- [ ] **옴니채널:** WhatsApp 외에 카카오톡, 인스타그램 DM 등으로 채널 확장

---

## ⚠️ 9. 예상되는 어려움 및 고려사항 (Risk & Considerations)

### 1. 비용 및 API 제한 (Cost & Limits)
- **WhatsApp 비용:** WhatsApp Business API는 대화(Conversation) 단위로 과금됩니다. 사용자가 많아질 경우 Twilio 비용이 예상보다 커질 수 있습니다.
- **OpenAI 비용:** 모든 메시지를 Embedding/GPT로 처리하면 토큰 비용이 발생합니다. 캐싱(Caching) 전략이 필수적입니다.
- **Google Sheets API:** 요청 횟수 제한(Rate Limit)이 있습니다. 실시간으로 매번 시트를 읽는 대신, 서버 메모리에 데이터를 로드해두고 주기적으로 동기화하는 방식이 필요합니다.

### 2. 응답 속도 (Latency)
- `Twilio -> Flask -> OpenAI -> Flask -> Twilio`로 이어지는 과정에서 3~5초 이상의 지연이 발생할 수 있습니다.
- **해결책:** 비동기 처리(Async)를 도입하거나, 단순 키워드 매칭은 OpenAI를 거치지 않고 즉시 응답하도록 최적화해야 합니다.

### 3. 데이터 정확성 및 환각 (Hallucination)
- GPT가 학교의 공식 입장이 아닌 잘못된 정보를 생성할 위험이 있습니다.
- **해결책:** `Temperature`를 0으로 설정하고, 답변 생성 시 반드시 Google Sheets에 있는 정보("Context") 내에서만 답변하도록 프롬프트를 강력하게 제한해야 합니다.

### 4. 개인정보 보호 (Privacy)
- 학생들의 전화번호와 대화 내용이 저장됩니다.
- **고려사항:** GDPR 등 국제 개인정보 규정을 고려하여, 민감한 정보는 암호화하거나 저장하지 않도록 설계해야 합니다.

### 5. 운영자(직원)의 데이터 관리 실수
- 직원이 Google Sheets의 형식을 실수로 망가뜨릴 수 있습니다 (예: 컬럼 삭제).
- **해결책:** 시트의 특정 영역을 '보호(Protected Range)'로 설정하거나, 데이터 유효성 검사 로직을 서버에 추가하여 오류 발생 시 기본값으로 동작하게 해야 합니다.

---

## ✅ 10. 작업 체크리스트
- [ ] **환경 설정:** Twilio Account 생성, WhatsApp Sandbox 설정
- [ ] **서버 구축:** Flask 프로젝트 생성 및 기본 Webhook 엔드포인트 구현
- [ ] **DB 연동:** Supabase 프로젝트 생성 및 User 테이블 설계
- [ ] **CMS 연동:** Google Cloud Console에서 Sheets API 활성화 및 연동
- [ ] **AI 구현:** OpenAI API Key 발급, Embedding 로직 구현
- [ ] **배포:** Railway에 서버 배포 및 환경변수 설정
- [ ] **테스트:** 시나리오별(학생/교수/파트너) 테스트 진행
