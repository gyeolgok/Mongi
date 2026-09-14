# 제작 워크플로

| 단계 | 담당 | 입력 | 산출물 | 통과 조건 |
|---|---|---|---|---|
| 1. Brief | 운영/Owner | 아이디어·목표 | `brief.md` | Owner 방향 확인 |
| 2. Script | Story Writer | 승인 Brief·필수 Canon | `script.md` | 작성 완료 |
| 3. Script Review | Continuity | Script·관련 Canon | `reviews/script-review.md` | `SCRIPT_APPROVED` |
| 4. Studio | Studio | 승인 Script | 컷·액션·`edit.json` | 제작 완료 |
| 5. Asset Review | Continuity | 전체 자산·Edit Lock | `reviews/asset-review.md` | `ASSET_APPROVED` |
| 6. Render | Renderer | 승인 패키지 | MP4·기술검증 결과 | Renderer validation 통과 |
| 7. Final Review | Owner/운영 | MP4·검수 결과 | 최종 판정 | `FINAL_APPROVED` |
| 8. Publish | 운영 | 승인본 | 플랫폼 게시·성과 원장 | 게시 정보 기록 |

## 반려 흐름

- 검수자는 `approval.json`의 해당 상태를 `REJECTED`로 변경한다.
- `blocking_issues`에는 위치, 충돌한 규칙, 필수 수정 결과를 기록한다.
- 담당자는 수정 후 상태를 `PENDING_REVIEW`로 되돌리고 재검수를 요청한다.
- 반려된 단계 이후의 결과물은 공식 산출물로 취급하지 않는다.

## 채팅 종료 조건

- 산출물이 영구 저장소에 존재한다.
- `status.json`의 `current_stage`, `next_role`, `next_action`, `updated_at`이 최신이다.
- 변경 내용이 커밋되어 있다.
- 대화에만 존재하는 공식 결정이 없다.

