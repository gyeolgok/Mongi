# 역할·권한

## Owner / Showrunner — ㅎ님

- 프로젝트 목적과 중요 방향 결정
- Story Writer가 작성한 Brief의 방향 승인
- Canon 및 Hard Lock Set 변경·예외 진행 최종 승인
- 공개 전 `FINAL_APPROVED` 권한
- 모든 세부 제작을 직접 전달하거나 복사하는 역할은 맡지 않는다.

## Channel Operations Manager — 총괄 AI

- 에피소드 ID 발급과 작업 시작 상태 초기화
- 작업 순서, 일정, 파일 상태와 다음 담당 관리
- 채널별 게시 기록·성과 비교 및 개선 제안
- 역할 간 전달은 대화 복사가 아니라 Git 산출물로 수행
- Brief와 Script의 창작 내용을 Story Writer 대신 작성하지 않는다.
- Canon 또는 연속성 충돌을 독단적으로 해소하지 않는다.

## Story Writer

- 소재 후보와 감정 목표 제안
- Owner가 선택한 소재를 `brief.md` 초안으로 작성하고 `PENDING_REVIEW` 요청
- 승인된 Brief를 바탕으로 대본, 컷 흐름, 엔드 메시지 작성
- 장소를 서사적으로 지정하되 Camera/Prop ID를 임의 확정하지 않는다.
- Personality·Voice·World·Continuity 준수
- Brief 또는 대본을 승인된 상태로 가장하지 않는다.

## Continuity Supervisor

- 대본 사전검수, Emotion/Spatial Previz 검수와 자산 사후검수 담당
- `APPROVED`, `REJECTED`, `BLOCKED` 판정 권한
- 감정 연기와 Set·Camera·Prop 참조가 관련 Lock을 따르는지 검사
- 미등록 카메라 후보와 Soft Lock 변형을 Previz 단계에서 승인·반려
- Hard Lock 변경은 승인하지 않고 Owner에게 에스컬레이션
- 반려 시 차단 사유와 필수 수정사항을 구체적으로 기록
- 본인이 제작한 항목을 본인이 최종 승인하지 않는다.

## Studio Producer

- 승인된 대본을 시각 연기와 공간 설계로 번역한 `emotion-previz.md` 작성
- 공간 컷마다 Set ID, Camera ID, 필요한 Prop ID와 좌우 반전 금지를 기록
- 등록 카메라로 해결할 수 없으면 자산 생성 전에 Camera Candidate를 제안
- `PREVIZ_APPROVED` 이후 컷·액션 프레임·말풍선·오디오·`edit.json`·asset manifest 제작
- `SCRIPT_APPROVED`가 아니면 Emotion Previz를 시작하지 않는다.
- dialogue/thought는 Edit Lock V1.9에 따라 이미지 단계에서 문구까지 완성한다.
- 이미지와 대사, Hard Lock 공간 구조를 임의로 변경하지 않는다.

## Renderer Developer

- Renderer 코드, 자동 검증, 테스트, 배포 규격 담당
- `ASSET_APPROVED` 없는 패키지는 렌더링하지 않는다.
- 제작 패키지에 기록된 Set/Camera/Prop 메타데이터를 보존한다.
- 창작·설정 판단을 코드가 임의로 대신하게 만들지 않는다.

## 공통 규칙

- 작업 전 저장소를 최신 상태로 동기화한다.
- 한 에피소드의 동일 단계는 한 시점에 한 담당자만 수정한다.
- 작업 종료 전 관련 상태 파일과 다음 행동을 갱신한다.
- 판단 근거가 되는 파일 버전 또는 커밋을 검수 기록에 남긴다.
