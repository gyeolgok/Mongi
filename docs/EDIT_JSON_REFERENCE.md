# edit.json V1 Reference

This renderer follows `Mongi Shorts Edit Lock V1.0`.

## Project

```json
{
  "project": {
    "id": "E03",
    "title": "Episode title",
    "format": "shorts",
    "resolution": {"width": 1080, "height": 1920},
    "fps": 30
  }
}
```

## Cut

Required: `id`, `image`, `duration`.

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

Camera presets: `STATIC`, `ZOOM_IN_SLOW`, `ZOOM_OUT_SLOW`, `PAN_LEFT`, `PAN_RIGHT`, `PAN_UP`, `PAN_DOWN`, `PUNCH_ZOOM`, `SHAKE_LIGHT`.

## Text

Types: `situation_label`, `dialogue`, `thought`, `caption`, `ui`.

```json
{
  "type": "dialogue",
  "text": "오늘은 진짜 하나라도 지원하자.",
  "position": "TOP_RIGHT",
  "x": 320,
  "y": 160,
  "width": 650,
  "appear_at": 0.3,
  "disappear_at": null,
  "animation": "POP_SOFT"
}
```

If `x/y` are omitted, semantic positions are used. Current semantic positions: `TOP_LEFT`, `TOP_RIGHT`, `BOTTOM_LEFT`, `BOTTOM_RIGHT`, `CENTER`, `ABOVE_CHARACTER`.

The renderer uses a project font from `assets/fonts/` first. The font file is not redistributed by this project. If no project font exists, a system Korean font is used as fallback.

## IMAGE_SWAP

```json
{
  "type": "IMAGE_SWAP",
  "at": 1.2,
  "image": "actions/cut05_blink.png",
  "duration": 0.18,
  "return_to_base": true,
  "transition": "CUT"
}
```

`transition` supports `CUT` and `CROSSFADE`.

## IMAGE_SEQUENCE

```json
{
  "type": "IMAGE_SEQUENCE",
  "at": 1.0,
  "frames": [
    {"image": "actions/tail_left.png", "duration": 0.12},
    {"image": "actions/tail_right.png", "duration": 0.12}
  ],
  "repeat": 2,
  "return_to_base": true
}
```

Overlapping actions are rejected in V1 so timing stays deterministic.

## SFX

Instant:

```json
{"name":"notification","at":1.2,"volume":1.0,"duck_bgm":true}
```

Interval:

```json
{"name":"heartbeat","start":0.8,"end":2.4,"volume":0.8}
```

Files are resolved from `assets/sfx/<name>.*`. Missing optional audio produces a warning and is skipped.

## BGM

```json
{
  "name":"daily",
  "start":0.0,
  "end":18.6,
  "volume":1.0,
  "fade_in":0.4,
  "fade_out":0.6
}
```

Files are resolved from `assets/bgm/<name>.*`. Short BGM files are looped to fill the requested interval.

## Transitions

`CUT`, `CROSSFADE`, `FADE_IN`, `FADE_OUT`, `FLASH`.

`CROSSFADE` preserves the sum of cut durations by padding the outgoing boundary before blending. This keeps the Edit Lock rule that total runtime is determined by cut durations.

## Cache

Each cut is hashed from its JSON, project render settings and referenced image metadata. Unchanged cuts reuse cached MP4s automatically. `--force` disables reuse for that run.
