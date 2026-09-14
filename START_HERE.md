# Mongi Project — START HERE

이 문서는 모든 Mongi AI 작업 채팅의 공통 진입점이다. 대화 기록을 프로젝트의 기억으로 사용하지 않는다. Git의 최신 파일과 ChatGPT Library의 공식 자산을 기준으로 작업한다.

## 1. 프로젝트 목적

2D 캐릭터 몽이의 일상과 스토리텔링을 통해 누군가에게는 깨달음과 전환점을, 누군가에게는 위로를 전달한다. 기본 숏폼 구조는 `일상 코미디 → 감정 인정 → 짧은 위로 또는 작은 전환`이다.

## 2. 확정 채널 운영

- 주력: YouTube Shorts
- 동시 게시: Instagram Reels, TikTok
- 초기 표현: 음성 없이 이미지 내 말풍선 + Renderer 후처리 텍스트 + BGM + SFX
- 주기: 주 2회
- 첫 4주: 출근 시간대 1편, 퇴근 시간대 1편을 나눠 게시하고 플랫폼별 지표로 조정
- 롱폼 제작 시 캐릭터 음성 도입을 재검토

## 3. 작업 시작 절차

1. 자신의 역할을 확인한다: `governance/ROLES.md`
2. 역할별 필수 파일만 읽는다: `governance/READ_MAP.md`
3. 현재 프로젝트 상태를 확인한다: `continuity/CURRENT_STATE.yaml`
4. 에피소드 작업이면 `episodes/<ID>/status.json`과 `approval.json`을 먼저 확인한다.
5. 반복 장소가 나오면 `continuity/sets/SET_REGISTRY.yaml`에서 Set/Camera/Prop ID를 확인한다.
6. 승인 게이트를 통과하지 못했다면 다음 단계 작업을 시작하지 않는다.
7. 완료 후 산출물, 상태, 검수 기록을 Git에 함께 갱신한다. 대화만 남기고 종료하지 않는다.

## 4. 권위와 충돌 해결

1. ㅎ님(Owner/Showrunner)의 명시적 결정
2. `canon/`과 `docs/Mongi-Shorts-Edit-Lock-V1.9-Consolidated.md`
3. `continuity/`의 최신 공식 상태와 Set Registry
4. 승인된 에피소드 문서
5. 채팅 중 임시 아이디어

Set Registry는 Canon Lock의 제작용 색인이며 Canon을 덮어쓰지 않는다. 충돌을 발견하면 임의로 설정을 바꾸지 말고 `REJECTED` 또는 `BLOCKED`로 기록한다. Canon 변경은 ㅎ님의 승인 없이는 확정할 수 없다.

## 5. 저장 위치

- GitHub: 코드, 규칙, 연속성, Set Registry, 대본, 승인·반려 상태, 변경 이력
- ChatGPT Library: 공식 레퍼런스 이미지, 생성 컷, 오디오 원본, 최종 영상 등 대용량 자산
- GPT 프로젝트 소스: START HERE와 자주 참조하는 고정 자료. 빈번한 작업 상태의 원본으로 사용하지 않는다.

Library는 ChatGPT의 파일 Library를 의미한다. 자세한 저장 기준은 `governance/STORAGE_POLICY.md`를 따른다.

## 6. 절대 게이트

- `SCRIPT_APPROVED` 전: Emotion Previz 시작 금지
- `PREVIZ_APPROVED` 전: 이미지·액션·오디오 등 제작 자산 생성 금지
- `ASSET_APPROVED` 전: Renderer 실행 금지
- `FINAL_APPROVED` 전: 게시 금지
- 예외 진행: `approval.json`에 ㅎ님의 명시적 override 기록 필요

## 7. 새 채팅용 최소 지시문

> Mongi 프로젝트의 `<역할>`이다. 저장소의 `START_HERE.md`를 먼저 읽고, `governance/READ_MAP.md`에서 내 역할에 지정된 최신 파일만 읽어라. 현재 작업은 `<작업/에피소드 ID>`다. 완료 후 산출물과 상태 파일을 함께 갱신하라.
