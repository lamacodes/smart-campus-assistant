# 시스템 아키텍처 (System Architecture)

## 개요 (Overview)
Smart Campus Assistant는 OpenAI의 지능형 기능과 Google Sheets의 간편한 데이터 관리를 활용하는 왓츠앱(WhatsApp) 기반 챗봇입니다.

## 아키텍처 모식도 (Architecture Diagram)

![Architecture Diagram](architecture_diagram.png)

## 데이터 흐름 (Data Flow)

```mermaid
sequenceDiagram
    participant User as 사용자
    participant WhatsApp
    participant Twilio
    participant FlaskApp as Flask 서버
    participant OpenAI
    participant GSheets as Google Sheets

    User->>WhatsApp: 메시지 전송
    WhatsApp->>Twilio: 메시지 전달
    Twilio->>FlaskApp: POST /webhook
    
    activate FlaskApp
    FlaskApp->>GSheets: FAQ 데이터 로드 (시작 시)
    
    alt FAQ 매칭 성공
        FlaskApp->>OpenAI: 임베딩 요청 (사용자 질문)
        FlaskApp->>FlaskApp: 코사인 유사도 계산
        FlaskApp-->>Twilio: FAQ 답변 반환
    else 매칭 실패
        FlaskApp->>OpenAI: 채팅 완성 요청 (Fallback)
        OpenAI-->>FlaskApp: 생성된 응답
        FlaskApp-->>Twilio: AI 응답 반환
    end
    deactivate FlaskApp

    Twilio->>WhatsApp: 답장 전송
    WhatsApp->>User: 메시지 표시
```

## 구성 요소 (Components)

1.  **사용자 인터페이스**: WhatsApp (Twilio API 경유).
2.  **백엔드**: Railway에 호스팅된 Flask 애플리케이션.
3.  **AI 엔진**: OpenAI GPT-3.5 (대체 응답) & Embeddings (검색).
4.  **데이터베이스**: Google Sheets (읽기 전용 FAQ 지식 베이스).
