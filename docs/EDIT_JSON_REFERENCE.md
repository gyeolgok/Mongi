# edit.json V1.9 Reference

최종 권위 문서는 `Mongi-Shorts-Edit-Lock-V1.9-Consolidated.md`다. 이 문서는 Renderer 입력 형식을 빠르게 확인하기 위한 요약이다.

## 패키지 승인

ZIP 루트에 `approval.json`이 필요하다. `episode_id`는 `edit.json`의 `project.id`와 일치해야 하며, 렌더 전 `script`와 `assets`가 승인되어야 한다. 전체 형식은 `episodes/_template/approval.json`을 사용한다.

## Project

```json
{
  "project": {
    "id": "E001",
    "title": "Episode title",
    "format": "shorts",
    "resolution": {"width": 1080, "height": 1920},
    "fps": 30
  }
}
```

## Cut

필수 필드는 `id`, `image`, `duration`이다.

```json
{
  "id": 1,
  "image": "images/cut01.png",
  "duration": 2.8,
  "camera": {"preset": "ZOOM_IN_SLOW"},
  "text": [],
  "actions": [],
  "sfx": [],
  "transition_out": {"type": "CUT"}
}
```

Camera: `STATIC`, `ZOOM_IN_SLOW`, `ZOOM_OUT_SLOW`, `PAN_LEFT`, `PAN_RIGHT`, `PAN_UP`, `PAN_DOWN`, `PUNCH_ZOOM`, `SHAKE_LIGHT`.

## Renderer 후합성 Text

허용 타입은 `situation_label`, `caption`, `ui`, `end_message`다.

`dialogue`와 `thought`는 이미지 안에 말풍선과 문구를 완성해야 하며 `text` 배열에 넣으면 Preflight가 거부한다. `TYPEWRITER`도 V1.9에서 거부한다.

## Actions

- `IMAGE_SWAP`
- `IMAGE_SEQUENCE`
- `CURSOR_MOVE`
- `CURSOR_CLICK`

이미지 액션끼리는 겹치지 않는다. Cursor 액션은 이미지 액션과 함께 사용할 수 있다.

## UI Click SFX

일반 UI 클릭의 공식 논리 키는 `light-click`이다. `CURSOR_CLICK`은 소리를 자동 생성하지 않으므로 필요한 경우 같은 시각에 SFX를 명시한다.

```json
{
  "actions": [{"type": "CURSOR_CLICK", "at": 0.95, "position": [710, 980], "duration": 0.16}],
  "sfx": [{"name": "light-click", "at": 0.95, "volume": 0.75}]
}
```

## End Card

마지막 컷이어야 하며 `STATIC` 카메라, 비어 있지 않은 `end_message`, 빈 `actions`가 필요하다.

```json
{
  "id": "end_card",
  "type": "end_card",
  "image": "images/end_card.png",
  "duration": 2.8,
  "camera": {"preset": "STATIC"},
  "text": [{"type": "end_message", "text": "오늘은 여기까지.", "appear_at": 0.2, "animation": "STATIC"}],
  "actions": [],
  "sfx": [],
  "transition_out": {"type": "FADE_OUT"}
}
```

## Cache

각 컷은 JSON, 프로젝트 설정과 참조 이미지 메타데이터로 해시된다. `--force`는 캐시를 무시한다.
