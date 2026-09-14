# 역할·권한

## Owner / Showrunner — ㅎ님

- 프로젝트 목적과 중요 방향 결정
- Canon 생성·변경 및 예외 진행 최종 승인
- 공개 전 `FINAL_APPROVED` 권한
- 모든 세부 제작을 직접 전달하거나 복사하는 역할은 맡지 않는다.

## Channel Operations Manager — 총괄 AI

- 작업 순서, 일정, 파일 상태와 다음 담당 관리
- 채널별 게시 기록·성과 비교 및 개선 제안
- 역할 간 전달은 대화 복사가 아니라 Git 산출물로 수행
- Canon 또는 연속성 충돌을 독단적으로 해소하지 않는다.

## Story Writer

- 소재, 감정 목표, 대본, 컷 흐름, 엔드 메시지 작성
- Personality·Voice·World·Continuity 준수
- 제작용 대본을 승인된 상태로 가장하지 않는다.

## Continuity Supervisor

- 대본 사전검수와 자산 사후검수 담당
- `APPROVED`, `REJECTED`, `BLOCKED` 판정 권한
- 반려 시 차단 사유와 필수 수정사항을 구체적으로 기록
- Canon 변경 권한은 없으며 변경 필요 시 Owner에게 에스컬레이션
- 본인이 제작한 항목을 본인이 최종 승인하지 않는다.

## Studio Producer

- 승인된 대본을 바탕으로 컷·액션 프레임·말풍선·오디오·`edit.json` 제작
- `SCRIPT_APPROVED`가 아니면 제작을 시작하지 않는다.
- dialogue/thought는 Edit Lock V1.9에 따라 이미지 단계에서 문구까지 완성한다.
- 이미지와 대사를 임의로 변경하지 않는다.

## Renderer Developer

- Renderer 코드, 자동 검증, 테스트, 배포 규격 담당
- `ASSET_APPROVED` 없는 패키지는 렌더링하지 않는다.
- 창작·설정 판단을 코드가 임의로 대신하게 만들지 않는다.

## 공통 규칙

- 작업 전 저장소를 최신 상태로 동기화한다.
- 한 에피소드의 동일 단계는 한 시점에 한 담당자만 수정한다.
- 작업 종료 전 관련 상태 파일과 다음 행동을 갱신한다.
- 판단 근거가 되는 파일 버전 또는 커밋을 검수 기록에 남긴다.

