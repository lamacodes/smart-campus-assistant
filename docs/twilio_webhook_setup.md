# Twilio Webhook 설정 가이드

Railway 배포가 완료되었습니다! 이제 Twilio에서 WhatsApp 메시지를 챗봇으로 연결하는 설정을 해야 합니다.

## Step 1: Twilio Console 접속
[Twilio Console](https://console.twilio.com/) 로그인

## Step 2: WhatsApp Sandbox 설정으로 이동
1. 왼쪽 메뉴에서 **Messaging** 클릭
2. **Try it out** 클릭
3. **Send a WhatsApp message** 클릭

## Step 3: Webhook URL 설정
Sandbox settings 페이지에서:

1. **"When a message comes in"** 섹션 찾기
2. URL 입력란에 다음을 입력:
   ```
   https://web-production-4871a.up.railway.app/webhook
   ```
3. Method: **POST** 선택
4. **Save** 버튼 클릭

## Step 4: WhatsApp에서 Sandbox 활성화
Twilio Sandbox 페이지 상단에 표시된 지시사항 따르기:

1. WhatsApp에서 표시된 번호로 메시지 보내기 (예: `+1 415 523 8886`)
2. 표시된 코드 전송 (예: `join [your-code]`)
3. Twilio로부터 확인 메시지 수신

## Step 5: 테스트!
WhatsApp에서 다음 메시지를 보내보세요:
- "When is the deadline?"
- "How much is the dorm?"
- "What documents do I need for visa?"

챗봇이 FAQ 답변을 보내야 합니다! 🎉

## 문제 해결
- **응답이 없는 경우**: Railway 로그 확인 (Deployments → Logs)
- **에러 메시지**: Twilio Console → Monitor → Logs에서 webhook 에러 확인
- **FAQ 매칭 안됨**: Google Sheets 데이터 확인

## 다음 단계
- Google Sheets에 더 많은 FAQ 추가
- 비용 모니터링 (OpenAI, Twilio 대시보드)
- 실제 사용자 테스트 및 피드백 수집
