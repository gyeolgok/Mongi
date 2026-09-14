# 승인·반려 정책

## 상태값

- `NOT_STARTED`: 작업 전
- `IN_PROGRESS`: 담당자가 작업 중
- `PENDING_REVIEW`: 검수 대기
- `APPROVED`: 게이트 통과
- `REJECTED`: 수정 없이는 진행 불가
- `BLOCKED`: Owner 판단 또는 외부 입력 필요

## 필수 게이트

- Brief 작성 후 Owner의 `BRIEF_APPROVED`
- Script 작성 후 Continuity Supervisor의 `SCRIPT_APPROVED`
- Emotion Previz 작성 후 Continuity Supervisor의 `PREVIZ_APPROVED`
- 최종 자산 제작 후 Continuity Supervisor의 `ASSET_APPROVED`
- 게시 전 Owner 또는 위임 운영 담당의 `FINAL_APPROVED`

Renderer Preflight는 에피소드 ZIP 루트의 `approval.json`에서 다음 두 승인을 자동 검사한다.

- `approvals.script.status == APPROVED`
- `approvals.assets.status == APPROVED`

`PREVIZ_APPROVED`는 고비용 자산 제작을 막는 운영 게이트이며 Renderer의 기술 게이트를 대체하지 않는다. 각 승인에는 `reviewer`와 ISO 8601 형식의 `reviewed_at`이 있어야 한다. `episode_id`는 `edit.json`의 `project.id`와 일치해야 한다.

## 권한 분리

- Brief 작성: Story Writer
- Brief 승인: Owner
- Script 승인: Continuity Supervisor
- Emotion Previz 작성: Studio Producer
- Emotion Previz 승인: Continuity Supervisor
- Asset 승인: Continuity Supervisor
- Final 승인: Owner 또는 Owner가 명시적으로 위임한 운영 담당
- Canon 변경 승인과 override: Owner만 가능

모든 AI 역할은 동일한 GitHub 사용자 권한을 사용할 수 있으므로 Git 커밋 작성자만으로 역할을 증명하지 않는다. 검수 기록의 역할·근거·시간과 단계별 작업 규칙으로 운영하며, 보안 수준의 강제력이 필요한 Canon·운영 규칙은 `CODEOWNERS`와 `main` 브랜치 보호를 활성화해 Owner 리뷰를 요구한다.

`CODEOWNERS` 파일만 추가해서는 강제되지 않는다. GitHub 저장소 설정에서 `main` 브랜치에 Pull Request와 Code Owner review 요구를 켜야 한다.

## Override

예외는 구두 합의나 채팅 추정으로 처리하지 않는다. `approval.json.override`에 다음을 기록한다.

- `approved_by_owner: true`
- `reason`
- `approved_at`
- `scope`

Override는 지정한 범위에만 적용되며 Canon 자체를 변경하지 않는다.
