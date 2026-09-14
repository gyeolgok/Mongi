# Mongi Shorts Edit Lock V1.5 — Audio Library V1

V1.5 extends V1.4 with source-segment-aware BGM playback.

## BGM source segment rule
- A BGM track MUST NOT be assumed to start at 0:00.
- Production selects a suitable recommended segment for the episode/cut and writes `source_start` in seconds.
- Renderer places that source segment at the episode timeline `start`.
- Exact recommended windows live in `assets/bgm_segments.json` and are part of the Renderer audio library.
- Fade and bridge rules from V1.4 remain active.

### Locked roles
- DAILY: Mizutama / Patchwork / Prelude
- CHILL: Linen
- EXCITED: Apricot Color
- HAPPY_EVENT: Petit Gift
- CITY: Parallax City
- GLOOMY: Vinyl Piano
- PLAYFUL_GAME: 8world (special-use only)
- INNER_MONOLOGUE: 静かな夜長に
- EMOTIONAL_PEAK: not locked; longing remains a candidate only.

### Transition principles
- DAILY↔DAILY: compatible; generally do not change tracks inside one short without a narrative reason.
- DAILY→CHILL: soft crossfade allowed.
- DAILY→INNER_MONOLOGUE: compatible; lower/clear DAILY first when dialogue needs space.
- GLOOMY→INNER_MONOLOGUE: preferred Mongi reflective transition.
- EXCITED/HAPPY→INNER_MONOLOGUE: no direct emotional crossfade; insert ~0.3–1.0 s reset using silence/room tone/SFX.
- PLAYFUL_GAME→INNER_MONOLOGUE: direct transition prohibited; reset first.
- EMOTIONAL_PEAK must be rare and cannot be used as a generic quote/lesson cue.

## edit.json BGM example
```json
{
  "name": "DAILY_MIZUTAMA",
  "start": 0.0,
  "end": 18.0,
  "source_start": 45.0,
  "volume": 0.18,
  "fade_in": 0.25,
  "fade_out": 0.5
}
```

All other production/package/rendering rules remain as defined by the preceding Edit Lock unless superseded here.

---

# Mongi Shorts Edit Lock V1.6 — Fixed End Card System

V1.6 extends V1.5 with a mandatory fixed End Card system. All V1.5 audio-library rules, including `source_start`, locked BGM roles, transition principles, and preceding Edit Lock rules remain active unless explicitly superseded below.

## End Card mandatory structure

Every Mongi Shorts episode MUST end with:

`본편 마지막 행동/대사 → 짧은 호흡 → 엔드카드 → 종료`

The final in-story line and the End Card message have different roles.

- **본편 마지막 대사:** 현재 상황에서 몽이가 실제로 할 법한 말이나 생각
- **엔드카드 메시지:** 그날의 에피소드를 한 걸음 떨어져 바라보는 짧은 여운

The End Card MUST be a real renderable final cut, not a README note or production reminder.

## Fixed End Card design

Use the E01-approved design language as the baseline.

- warm cream/ivory solid background or extremely subtle texture
- a mini Mongi illustration lying down and resting
- a small paw symbol MAY be used
- episode-specific End Card message placed for easy reading
- minimal screen elements and generous negative space
- Character Lock appearance MUST be preserved; End Card-specific simplification is allowed
- no excessive decoration, glitter, flashy motion, or meme elements

The mini Mongi SHOULD use the same fixed reusable asset whenever possible. Do not regenerate it for every episode by default.

## Prohibited viewer-facing metadata

The End Card MUST NOT display production metadata such as:

- `E01`, `E02`, etc.
- `V1`, `V2`, `Final`, etc.
- Renderer information
- production date
- internal project name

`Mongi Shorts` or other channel branding is not mandatory in the default End Card. If channel branding is later required, define it in a separate rule.

## Episode-specific message ownership

The End Card design/layout is fixed, but the message changes every episode.

**The writer room owns and approves the End Card message.**

Production MUST use the approved message as-is and MUST NOT:

- rewrite it
- add a new lesson
- exaggerate it to sound more inspirational
- replace it with a generic quote

The message MUST follow Personality Lock and Voice Lock. Prefer a short natural aftertaste that grows out of that episode rather than a grand quote, self-help slogan, or forced positivity. Do not demean Mongi.

## End Card direction

Treat the End Card as a short readable static closing section, not as another fast story cut.

- default camera: `STATIC`
- `SHAKE`, `PAN`, and excessive `ZOOM` are prohibited
- no character animation by default
- only very subtle fade-family entry/exit is allowed when useful
- display long enough for the approved message to be read

Exact default duration and fade values are intentionally NOT hard-locked in V1.6. They may be locked later after reviewing actual Renderer output and overall Shorts pacing.

### End Card audio

- Do not automatically switch to a new BGM track at End Card entry.
- Normally continue/fade out the existing episode BGM according to the active audio rules.
- Do not automatically apply a sentimental track or `EMOTIONAL_PEAK` merely because the End Card has begun.
- All V1.5 BGM source-segment and transition rules remain active.

## Renderer package requirements

Every episode package MUST contain enough information/assets to render the End Card as the final cut.

Required:

- fixed End Card background / mini Mongi asset
- writer-room-approved episode End Card message
- final End Card cut in `edit.json`
- valid display duration
- valid transition/fade information

A shared Renderer asset may be referenced rather than physically duplicated into every episode package.

### edit.json End Card identification

The final cut SHOULD be explicitly identifiable as:

```json
{
  "id": "end_card",
  "type": "end_card",
  "image": "assets/endcard/mongi_rest.png",
  "duration": 2.8,
  "camera": {
    "preset": "STATIC"
  },
  "text": [
    {
      "type": "end_message",
      "text": "같은 하루가, 언젠가는 달라질 거니까.",
      "appear_at": 0.2,
      "disappear_at": null,
      "animation": "STATIC"
    }
  ],
  "actions": [],
  "sfx": [],
  "transition_in": {
    "type": "CROSSFADE"
  },
  "transition_out": {
    "type": "FADE_OUT"
  }
}
```

The numeric values above are schema examples only; they do NOT establish mandatory End Card duration or fade timing.

`end_message` is a dedicated text role. Renderer MUST apply the locked End Card typography/layout rather than treating it as a normal dialogue bubble.

## Preflight

Preflight MUST verify before rendering:

- the final cut is an End Card
- the required fixed End Card asset exists
- an `end_message` exists
- the message is not empty
- End Card duration is valid
- requested transition/fade values are supported

Missing End Card or missing/empty End Card message is a **fatal Preflight error** and rendering MUST stop.

## E01 official reference case

E01 is the official structural reference.

**본편 마지막:**

`일단 하나는 했다.`

**엔드카드:**

`같은 하루가, 언젠가는 달라질 거니까.`

Future episodes preserve this structure and design grammar, but MUST NOT mechanically repeat the E01 message.

## Compatibility

All V1.5 rules remain active. V1.6 only adds/supersedes rules where the End Card system explicitly requires it.


---

# Mongi Shorts Edit Lock V1.7 — Renderer Interaction Actions

V1.7 extends V1.6 with official Renderer interaction actions and dialogue/thought typewriter text animation. All V1.6 End Card rules, V1.5 Audio Library rules, and preceding Edit Lock rules remain active unless explicitly superseded below.

## Official cursor actions

`CURSOR_MOVE` and `CURSOR_CLICK` are official Mongi Renderer Action Types. Production MUST use these actions for render-time mouse-pointer interaction instead of inventing episode-specific action names or baking multiple cursor positions into the base image.

### CURSOR_MOVE

`CURSOR_MOVE` renders one cursor as an overlay and moves it from a start coordinate to a target coordinate.

Required fields:
- `type`: `CURSOR_MOVE`
- `from`: `[x, y]`
- `to`: `[x, y]`

Optional fields:
- `at`: action start time within the cut
- `duration`: movement duration
- `easing`: `linear`, `ease_in`, `ease_out`, or `ease_in_out`

Example:
```json
{
  "type": "CURSOR_MOVE",
  "at": 0.50,
  "from": [820, 1320],
  "to": [710, 980],
  "duration": 0.45,
  "easing": "ease_out"
}
```

### CURSOR_CLICK

`CURSOR_CLICK` renders the click-state visual feedback at the intended pointer position. Click SFX remains a timeline SFX responsibility and MUST be synchronized to the visual click moment rather than assumed by the cursor action itself.

Production MUST NOT bake multiple cursor copies into the base image to simulate motion. Unless multiple pointers are explicitly part of the story, only one visible cursor may exist at a time.

`CURSOR_MOVE` / `CURSOR_CLICK` may coexist with `IMAGE_SWAP` / `IMAGE_SEQUENCE` because cursor actions are Renderer overlays rather than replacement image frames.

## Typewriter text animation

`TYPEWRITER` is an official Renderer text animation for Mongi dialogue and thought text when progressive reading improves pacing.

Example:
```json
{
  "type": "dialogue",
  "text": "아... 이거 괜찮은데?",
  "animation": "TYPEWRITER",
  "chars_per_second": 12
}
```

Rules:
- Primary use: Mongi `dialogue` and `thought` text.
- Default production baseline: approximately 10–15 Korean characters per second; `12` is the normal starting value.
- Production may adjust speed to the line and cut, but MUST preserve comfortable reading time.
- Situation labels, UI text, and End Card messages remain static by default. Do not apply TYPEWRITER mechanically to every text element.
- Per-character typing SFX is OFF by default. Add typing SFX only when specifically motivated by the scene.
- TYPEWRITER does not justify shortening the cut below readable duration. Cut timing must still allow the viewer to finish reading the completed line.

## Interaction timing and preflight

Production MUST author actions only from the official action types defined by the active Edit Lock / Renderer contract. Renderer Preflight MUST reject unknown action types rather than silently ignoring them.

For click scenes, the intended order should be legible in the rendered result:

`cursor movement → target acquisition → click visual → synchronized click SFX / UI response`

When a UI exists on a tilted or perspective display surface, the UI composition remains subject to the existing visual continuity rules; cursor support does not excuse mismatched screen perspective.

## Compatibility

V1.7 adds the official `CURSOR_MOVE`, `CURSOR_CLICK`, and `TYPEWRITER` contracts. Existing `IMAGE_SWAP` / `IMAGE_SEQUENCE`, camera, transition, Audio V1, and End Card rules remain active.


---

# Mongi Shorts Edit Lock V1.7.1 — Official UI Click SFX

V1.7.1 extends V1.7 by locking the official Audio V1 key used for ordinary mouse/UI click feedback. All V1.7 interaction-action rules and preceding Edit Lock rules remain active unless explicitly superseded below.

## Official click SFX key

`light-click` is the official Audio V1 SFX key for ordinary mouse clicks and UI button clicks.

Renderer asset resolution:

`assets/sfx/light-click.*`

The file extension is not part of the logical key. Production MUST reference the logical key exactly as `light-click` in `edit.json`.

### Intended use

Use `light-click` for:
- mouse-pointer clicks
- ordinary UI button presses
- `CURSOR_CLICK` scenes where an audible click is editorially appropriate

Do not automatically use it for physical switches, object impacts, mechanical buttons, or unrelated `click`-like sounds. Those require their own approved Audio V1 key when needed.

## CURSOR_CLICK synchronization

`CURSOR_CLICK` remains a visual Renderer action. It MUST NOT automatically inject audio.

When a click sound is required, Production MUST add `light-click` to the cut's timeline SFX and synchronize its `at` time to the visible click moment.

Example:

```json
{
  "actions": [
    {
      "type": "CURSOR_CLICK",
      "at": 0.95,
      "position": [710, 980],
      "duration": 0.16
    }
  ],
  "sfx": [
    {
      "name": "light-click",
      "at": 0.95,
      "volume": 0.75
    }
  ]
}
```

The values above are examples only. The actual click time MUST follow the final visual action timing.

## Production rule

Production MUST NOT invent `click`, `mouse-click`, `ui-click`, `soft-click`, or other aliases when the intended sound is the approved ordinary UI click. Use `light-click`.

If `assets/sfx/light-click.*` is missing from the local Renderer Audio V1 library, Preflight may warn and the production package MUST NOT silently substitute a different SFX.

---

# Mongi Shorts Edit Lock V1.7.2 — Soft Organic Dialogue / Thought Bubble

V1.7.2 supersedes the previous geometric dialogue/thought bubble treatment. All preceding V1.7.1 rules remain active unless explicitly superseded below.

## Official dialogue / thought bubble appearance

`dialogue` and `thought` MUST use the Mongi Soft Organic Bubble treatment by default.

- Shape: softly irregular, asymmetric cloud-like organic silhouette. Perfect ellipses, capsules, rounded rectangles, and PowerPoint-like geometric boxes are prohibited as the default character bubble.
- Border: no black/dark outline. Default is no visible stroke; an extremely subtle edge caused by alpha feathering is acceptable.
- Fill: warm ivory / warm white, semi-transparent, allowing the illustration to blend naturally around the bubble.
- Edge: softly feathered rather than a hard vector cutout.
- Variation: the silhouette may vary slightly by aspect ratio/text length, but must remain deterministic within Renderer output and must not become noisy or spiky.
- Readability: text contrast and completed-line reading time remain higher priority than decorative irregularity.

`thought` should feel slightly airier/rounder than `dialogue`. A conventional chain of small thought dots is optional and is NOT automatically required by Renderer.

This rule applies to character `dialogue` and `thought` only. `situation_label`, `caption`, `ui`, and `end_message` retain their own existing roles and MUST NOT automatically inherit the cloud bubble.

## Renderer contract

Renderer V1.6.9+ implements the default soft organic bubble procedurally and deterministically. Production should not bake a separate black-outlined speech bubble into source artwork when Renderer text is used.

TYPEWRITER remains compatible: the final bubble geometry is established first and the text reveals inside it without resizing the bubble each character.
