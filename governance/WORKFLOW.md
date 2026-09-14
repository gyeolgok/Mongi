# 제작 워크플로

| 단계 | 담당 | 입력 | 산출물 | 통과 조건 |
|---|---|---|---|---|
| 1. 소재 선택 | Story Writer → Owner | 채널 방향·Canon | 후보안·선택 기록 | Owner 소재 선택 |
| 2. Brief Draft | Story Writer | 선택된 소재 | `brief.md` | `PENDING_REVIEW` |
| 3. Brief Review | Owner | Brief 초안 | `approval.json` | `BRIEF_APPROVED` |
| 4. Script | Story Writer | 승인 Brief·필수 Canon | `script.md` | 작성 완료 |
| 5. Script Review | Continuity | Script·관련 Canon | `reviews/script-review.md` | `SCRIPT_APPROVED` |
| 6. Emotion Previz | Studio | 승인 Script·Character Lock | `emotion-previz.md` | 연기 설계 완료 |
| 7. Previz Review | Continuity | Emotion Previz·관련 Canon | `reviews/previz-review.md` | `PREVIZ_APPROVED` |
| 8. Asset Production | Studio | 승인 Previz | 컷·액션·말풍선·오디오·`edit.json` | 제작 완료 |
| 9. Asset Review | Continuity | 전체 자산·Edit Lock | `reviews/asset-review.md` | `ASSET_APPROVED` |
| 10. Render | Renderer | 승인 패키지 | MP4·기술검증 결과 | Renderer validation 통과 |
| 11. Final Review | Owner/운영 | MP4·검수 결과 | 최종 판정 | `FINAL_APPROVED` |
| 12. Publish | 운영 | 승인본 | 플랫폼 게시·성과 원장 | 게시 정보 기록 |

## Emotion Previz 원칙

- 목적은 3D 영상 제작이 아니라 이미지 생성 전에 감정 연기와 화면 리듬을 고정하는 것이다.
- 각 컷의 실루엣, 머리·몸 자세, 귀, 꼬리, 시선, 표정, 감정 강도, 정지 시간, 말풍선 등장 시점과 오디오 의도를 기록한다.
- 감정 신호 우선순위는 `몸의 실루엣 → 귀 → 꼬리 → 눈과 입 → 말풍선 → BGM·SFX`다.
- 전환은 결과만 지정하지 않고 최소한 `이전 감정 → 중간 반응 → 도착 감정`으로 설계한다.
- 위로 장면에서도 직전 감정의 잔여감을 유지하며 갑작스러운 행복·성공 표현을 금지한다.
- `PREVIZ_APPROVED` 전에는 비용이 드는 최종 이미지·액션 자산 제작을 시작하지 않는다.

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
