# Mongi Audio Library V1.4

## SFX
V1.3.1의 봉봉뮤직 Cute/Motion SFX 26종 + utility SFX 3종을 그대로 유지한다.
- `blink_bubble`: 강조된 꿈뻑 1회
- `blink_bubble_double`: 강조된 꿈뻑꿈뻑 2회
- 자연스러운 일반 blink는 무음

## BGM — Curated Palette
기존 합성 placeholder BGM은 V1.4에서 제거한다.

| Key | Track | Role |
|---|---|---|
| DAILY_MIZUTAMA | Mizutama | 대표 일상 |
| DAILY_PATCHWORK | Patchwork | 포근하고 장난스러운 일상 |
| DAILY_PRELUDE | Prelude | 맑고 차분한 일상/아침/작업 |
| CHILL_LINEN | Linen | 여유롭고 느긋한 일상 |
| EXCITED_APRICOT_COLOR | Apricot Color | 발견/쇼핑/들뜸 |
| HAPPY_PETIT_GIFT | Petit Gift | 작은 기쁨/외출/오프닝 |
| CITY_PARALLAX_CITY | Parallax City | 도시/카페/쇼핑/외출 |
| GLOOMY_VINYL_PIANO | Vinyl Piano | 현타/조용한 실망 |
| PLAYFUL_8WORLD | 8world | 게임/망상/계산 개그 전용 |
| INNER_MONOLOGUE_QUIET_NIGHT | 静かな夜長に | 조용한 독백/내면 |

`EMOTIONAL_PEAK`는 아직 곡을 Lock하지 않는다.

## Transition compatibility
- DAILY → DAILY: ◎
- DAILY → CHILL: ◎ soft crossfade
- DAILY → EXCITED/HAPPY: ◎ 사건/SFX 기준 CUT 또는 짧은 fade
- DAILY → INNER_MONOLOGUE: ◎
- CHILL → INNER_MONOLOGUE: ◎
- GLOOMY → INNER_MONOLOGUE: ◎◎ 대표 감정 전환 후보
- EXCITED/HAPPY → INNER_MONOLOGUE: △ 직접 crossfade 금지; 0.3~1.0초 정적/환경음/SFX bridge 권장
- CITY → INNER_MONOLOGUE: ○ 기존 음악을 먼저 정리
- PLAYFUL_8WORLD → INNER_MONOLOGUE: × 직접 연결 금지

실제 음원 확보 후 BPM/LUFS/인트로·아웃트로를 분석하여 곡별 최적 진입·퇴장 타임코드는 별도 QC한다.

## V1.5 source-segment rule
BGM does not default to the beginning of a song. `assets/bgm_segments.json` contains recommended source windows. `edit.json` may specify `source_start` (seconds) for each BGM event. Renderer V1.5 trims from that point before placing the BGM on the episode timeline.

Example: `{ "name":"DAILY_MIZUTAMA", "start":0, "end":18, "source_start":45, "volume":0.18, "fade_in":0.25, "fade_out":0.5 }`

The segment table is the audio-library V1 baseline. It can be refined after episode-level editorial use without renaming the logical BGM keys.

## V1.7.1 official UI click

- `light-click`: ordinary mouse click / UI button click.
- Local asset path: `assets/sfx/light-click.*`.
- Use with `CURSOR_CLICK` by placing it explicitly on the cut SFX timeline at the visible click moment.
- `CURSOR_CLICK` does not auto-play SFX.
- Do not alias this sound as `click`, `mouse-click`, `ui-click`, or `soft-click` in episode packages.
