# Mongi Shorts Edit Lock V1.9 — Consolidated Standalone

작성일: 2026-09-14  
상태: V1.4.1 본체 + V1.5~V1.9 변경사항을 모두 반영한 독립 실행형 최신 규격  
적용 범위: 몽이 쇼츠/릴스 기본 제작. 향후 롱폼에서도 동일 철학과 구조를 확장 사용한다.



> **Standalone 원칙:** 이 파일 하나만으로 현재 Mongi Shorts 제작 규격을 확인할 수 있어야 한다.  
> V1.0~V1.7.2의 별도 문서를 참조해야만 성립하는 규칙을 두지 않는다.  
> 아래 후속 버전 섹션은 앞선 본체 규칙을 **추가하거나 명시적으로 대체**하며, 충돌 시 더 최신 섹션이 우선한다.

---

## 1. 목적

이 문서는 몽이 콘텐츠의 **컷 설계 → 이미지 생성 → 액션 프레임 생성 → 편집 JSON 작성 → Renderer 합성 → 최종 검수** 전 과정에서 사용하는 공통 제작 규격이다.

제작실은 영상 편집 단계에서만 이 문서를 참고하는 것이 아니라, **컷 설계 및 이미지 생성 이전부터 최신 「Mongi Shorts Edit Lock」을 필수 제작 규격으로 참고한다.**

본 문서는 Character Lock, Personality Lock, World Lock, Voice Lock, Home Lock의 설정을 변경하지 않는다. 외형·공간·말투·세계관은 각 Lock을 우선한다.

---

## 2. 기본 제작 원칙

1. **효과를 넣기 위해 효과를 넣지 않는다.**
   - 카메라 모션
   - 캐릭터 미세 움직임
   - SFX
   - BGM 변화
   - Transition
   모두 이야기·감정·행동 전달에 도움이 될 때만 사용한다.

2. 영상 전체 길이를 15초·20초처럼 고정하지 않는다.
   - 각 컷의 텍스트 읽기 시간
   - 장면 이해 시간
   - 감정의 중요도
   - 개그/여운 타이밍
   을 기준으로 제작실이 컷별 시간을 계산한다.

3. 영상 전체 길이는 각 컷 duration의 합으로 자연스럽게 결정된다.

4. 마지막 컷은 필요할 경우 약 0.7초 내외의 여운을 추가할 수 있으나 하드 규칙으로 강제하지 않는다.

5. 기본 스토리 컷과 액션 프레임을 구분한다.
   - 기본 컷: 이야기 진행 단위
   - 액션 프레임: 눈·귀·꼬리·표정 등 한 컷 내부의 변화용 보조 이미지
   액션 프레임은 별도의 스토리 컷으로 계산하지 않는다.

---

# 3. 컷 타이밍 Lock

각 컷의 `duration`은 제작실이 장면별로 계산하여 `edit.json`에 기록한다.

판단 기준:

- 대사/생각을 읽는 시간
- 화면의 핵심 정보를 인지하는 시간
- 감정 변화가 읽히는 시간
- 개그 타이밍
- 다음 컷으로 넘어가기 전 필요한 여운

사람이 읽는 이유 설명이 필요한 경우 선택 필드 `note`를 사용한다.

예:

```json
{
  "id": 4,
  "note": "탈락 문자 확인 후 표정 변화와 현타 여운을 위해 길게 유지",
  "duration": 3.4
}
```

Renderer는 `note`를 무시한다.

---

# 4. Camera Motion Lock

## 기본 프리셋

- `STATIC`
- `ZOOM_IN_SLOW`
- `ZOOM_OUT_SLOW`
- `PAN_LEFT`
- `PAN_RIGHT`
- `PAN_UP`
- `PAN_DOWN`
- `PUNCH_ZOOM`
- `SHAKE_LIGHT`

카메라 움직임은 매 컷 자동 적용하지 않는다.

### 사용 원칙

- 감정이나 정보 강조가 필요하지 않으면 `STATIC`
- 발견·집중·현타 강조에는 필요 시 느린 줌
- 강한 발견·충격·개그 포인트에는 제한적으로 `PUNCH_ZOOM`
- 흔들림은 상황상 필요한 경우에만 `SHAKE_LIGHT`
- 모든 카메라 효과는 기본 이미지 전체에 적용한다.

V1에서는 몽이 캐릭터만 따로 위치 이동시키는 `BOUNCE/JOLT/SINK` 등의 레이어 애니메이션을 사용하지 않는다.

---

# 5. Text / Bubble Lock

## 5.1 제작 주체 분리

캐릭터의 `dialogue` / `thought`는 **말풍선 형태와 실제 대사·생각 텍스트까지 이미지 생성 단계에서 직접 완성**한다.

Renderer는 `dialogue` / `thought` 말풍선이나 그 내부 텍스트를 새로 생성·합성하지 않는다.

Renderer 후합성 대상으로 유지하는 텍스트는 다음과 같다.

- `situation_label`
- `caption`
- 후처리 자막
- Renderer용 `ui`
- Fixed End Card의 `end_message`

스토리상 화면 속 기기·간판·문서 등에 실제로 존재해야 하는 텍스트는 장면 요구에 따라 이미지 자체에 포함할 수 있다.

---

## 5.2 Dialogue / Thought — Mongi Soft Organic Bubble

`dialogue`와 `thought`는 공식 **Mongi Soft Organic Bubble** 규격을 사용한다.

공식 Visual Style Reference:

`Mongi-Soft-Organic-Bubble-Visual-Reference-V1.0.png`

Reference에서 고정하는 것은 실제 문구가 아니라 다음 시각 특성이다.

- 흰색~웜아이보리 계열의 반투명 채움
- 구름형/솜뭉치형의 부드럽고 불규칙한 유기적 실루엣
- 외곽선 없음 또는 거의 인지되지 않는 매우 흐린 경계
- 딱딱한 벡터 절단면이 아닌 부드럽게 번지는 가장자리
- 배경과 자연스럽게 섞이는 가볍고 포근한 질감
- 진한 웜브라운 계열의 글자
- 모바일에서 즉시 읽히는 충분한 명도 대비와 내부 여백

`thought`는 `dialogue`보다 약간 더 가볍고 둥근 인상을 줄 수 있다. 일반적인 만화식 생각 말풍선 점 사슬은 자동 필수 요소가 아니다.

### 금지

- 완전한 원/타원
- 둥근 사각형 또는 캡슐형 기하학 말풍선
- 검은색 또는 진한 외곽선
- 일반적인 만화식 speech balloon
- 뾰족하고 명확한 말풍선 꼬리
- 딱딱한 벡터 UI 박스
- 불투명한 새하얀 판 형태

---

## 5.3 Dialogue / Thought Composition Area

대사/생각이 있는 컷은 이미지 생성 전에 **Dialogue / Thought Composition Area**를 결정한다.

이는 Renderer 후합성을 위한 빈 `Text Safe Area`가 아니라, **이미지 생성 단계에서 실제 말풍선과 텍스트를 배치하기 위한 구도 영역**이다.

해당 영역에는 다음 핵심 요소가 겹치지 않도록 한다.

- 몽이 얼굴 및 신체 핵심부
- 핵심 행동
- 이야기 전달에 필요한 주요 소품
- 반드시 보여야 하는 UI/시각 정보

우선 위치:

- 몽이 머리 위
- 시선 반대쪽의 비교적 단순한 공간
- 화면 가장자리에서 충분히 떨어진 영역

충돌 시 글자를 과도하게 줄이지 말고 말풍선 위치 또는 이미지 구도를 수정한다.

---

## 5.4 Dialogue / Thought Text Rule

- 실제 확정 대사/생각 문구를 이미지 생성 프롬프트에 정확히 제공한다.
- 기본 최대 3줄을 목표로 한다.
- 길 경우 우선 문장을 자연스럽게 축약하거나 컷/대사를 분리한다.
- 폰트 축소는 마지막 수단이다.
- 생성 후 오탈자, 누락, 중복 글자, 잘못된 줄바꿈을 반드시 검수한다.
- 대사/생각 문구가 바뀌면 해당 이미지도 수정 또는 재생성한다.
- 말풍선과 텍스트는 캐릭터·표정·행동을 가리지 않아야 한다.

---

## 5.5 Action Frame Continuity with Baked Dialogue / Thought

같은 컷에서 `IMAGE_SWAP` / `IMAGE_SEQUENCE`용 액션 프레임을 생성할 때, 이미 대사/생각 말풍선이 존재한다면 **모든 프레임에서 말풍선의 문구·위치·크기·실루엣이 동일하게 유지**되어야 한다.

액션 프레임마다 말풍선이 흔들리거나 다시 그려져 보이면 FAIL이다.

말풍선 고정이 안정적으로 재현되지 않는 컷은 액션 프레임 구조를 단순화하거나, 말풍선이 없는 구간과 있는 구간을 별도 스토리 컷으로 설계한다.

---

## 5.6 Renderer Post Text

Renderer가 후합성하는 `situation_label`, `caption`, 후처리 자막, Renderer용 `ui`, `end_message`는 기존 Renderer 텍스트 시스템을 사용한다.

이 후처리 텍스트는 Mongi Soft Organic Bubble을 자동 상속하지 않는다.

Renderer 후처리 텍스트가 예정된 컷은 이미지 생성 전에 해당 영역을 확보하고, 완성 이미지 기준으로 최종 좌표를 `edit.json`에 기록한다.

기본 텍스트 톤은 따뜻하고 둥근 손글씨 계열이며, 순수 검정보다는 짙은 웜브라운 계열을 우선한다. 실제 폰트 자산과 대체 폰트 운용은 Renderer `assets/fonts/` 규격을 따른다.

---

## 5.7 Dialogue / Thought Animation

이미지에 직접 완성된 `dialogue` / `thought`에는 Renderer의 `POP_SOFT`, `FADE_OUT`, `TYPEWRITER` 등 **텍스트/말풍선 자체 애니메이션을 적용하지 않는다.**

말풍선의 등장 또는 교체가 이야기상 필요하면 이미지가 다른 스토리 컷 또는 승인된 이미지 전환 구조로 설계한다.

카메라 모션은 말풍선이 포함된 완성 이미지 전체에 적용된다.

---

# 6. Character Micro Animation Lock

## 6.1 기본 원칙

**움직이게 만들기 위해 움직이지 않는다.**

캐릭터 움직임은 감정·주의·행동 변화가 발생하는 순간에만 사용한다.

V1에서는 Live2D나 파츠 리깅을 사용하지 않는다.

캐릭터 형태 변화가 필요한 경우 제작실에서 **필요한 액션 프레임 이미지를 추가 생성**하고, Renderer는 이미지 교체와 타이밍만 담당한다.

---

## 6.2 눈

- 자동 주기적 blink 없음
- 장면별로 필요할 때만 지정
- 현타/피로/긴장 등 감정에 맞춰 속도를 다르게 설계 가능

예:

`base → blink → base`

---

## 6.3 귀

귀 상태를 몇 개의 고정 각도로 제한하지 않는다.

장면에 따라:

- 한쪽만 살짝 들림
- 양쪽 비대칭
- 반쯤 들림
- 완전히 올라감
- 축 처짐
- 뒤로 젖힘

등 필요한 상태를 액션 프레임으로 생성한다.

귀는 Character Lock을 절대 준수하며, 특히 완전히 올라간 상태에서도 전체 귀는 정확히 2개여야 한다.

---

## 6.4 꼬리

꼬리는 강아지다운 핵심 행동 표현으로 적극 사용할 수 있다.

### 상태 변화

- 내려감
- 높게 듦
- 굳음
- 몸 가까이 축 처짐

등은 액션 프레임 교체로 처리한다.

### 좌우 흔들기

필요한 경우 최소 2개 이상의 액션 프레임을 생성한다.

예:

`LEFT → RIGHT → LEFT → RIGHT`

또는 더 부드럽게:

`LEFT → CENTER → RIGHT → CENTER`

흔드는 속도와 횟수는 고정하지 않고 장면 감정에 따라 제작실이 결정한다.

---

## 6.5 표정

`HAPPY`, `SAD` 등 몇 개의 Renderer 프리셋으로 제한하지 않는다.

Character Lock의 감정 기준에 따라 장면별로 필요한 표정 액션 프레임을 생성한다.

예:

- 평범 → 기대
- 기대 → 당황
- 당황 → 현타
- 평범 → 허탈·체념

---

## 6.6 몸/자세

앉기, 엎드리기, 네발, 고개 숙임 등 실제 자세가 바뀌는 경우 액션 프레임을 생성한다.

V1에서는 몽이만 따로 상하 이동시키는 캐릭터 레이어 애니메이션은 사용하지 않는다.

---

## 6.7 액션 프레임 전환

- 눈 깜빡임, 꼬리 흔들기 등 빠른 반응: 즉시 교체 우선
- 귀/표정/자세 변화: 장면에 따라 즉시 교체 또는 짧은 `CROSSFADE`
- 모든 액션 프레임은 같은 컷의 기본 구도를 유지한다. 대사/생각 말풍선이 이미지에 포함된 컷은 Section 5.5의 말풍선 픽셀 연속성 규칙을 추가로 준수한다.

---

# 7. SFX Lock

## 7.1 기본 운영

**고정 SFX 라이브러리 + 필요 시 확장** 방식으로 운영한다.

기본 라이브러리는 **현실계 유틸리티 SFX + 봉봉뮤직 Cute/Motion SFX** 조합으로 운영한다.

유틸리티:
- `click`
- `notification`
- `heartbeat`

Cute/Motion 핵심:
- `blink_bubble` — 봉봉뮤직 원본 `2.buble`; 연출상 강조된 **꿈뻑 1회**
- `blink_bubble_double` — 봉봉뮤직 원본 `3.buble move`; 연출상 강조된 **꿈뻑꿈뻑 2회**
- `cute_move`
- `cartoon_move`
- `cartoon_boing`
- `cartoon_wild_move`
- `cartoon_down_move`
- `cartoon_up_move`
- `rolling`
- `anim_move_01~02`
- `anim_action_01~07`
- 그 외 설치된 봉봉뮤직 모션 키

**자연스러운 일반 눈 깜빡임은 무음**으로 처리한다. `blink_bubble` 계열은 깜빡임 자체가 감정·개그 포인트일 때만 사용한다.

기존 V1.2의 합성형 pop/whoosh/chime/impact 계열은 몽이의 기본 모션 SFX에서 제외한다.

새로운 장면에서 기존 효과음으로 표현하기 어렵다면 억지 재사용하지 않고 새 SFX를 추가한다.

사용자는 선정된 파일을 `assets/sfx/`에 보관한다.

가능하면 `LICENSES.json` 등에 원본 이름·출처·라이선스를 기록한다.

### 봉봉뮤직 소스 사용 조건
- 원본 영상: `https://youtu.be/BlmezHTpyfA`
- 제작자 설명 기준, 필요한 부분을 개인 영상의 BGM/효과음으로 사용하는 것은 허용된다.
- 무료 사용 시 게시글/영상 설명에 저작권자 정보와 원본 영상 링크를 표기한다.
- 현재 개인 제작용 Renderer 통합본에는 사용자가 제공한 봉봉뮤직 Cute/Motion SFX 26종을 직접 포함한다.
- 별도 설치 없이 논리 키(`blink_bubble`, `blink_bubble_double`, `cute_move`, `cartoon_*` 등)로 바로 사용한다.
- Renderer 자체를 제3자에게 판매·재배포하는 경우 원 제작자의 재배포 조건을 다시 확인한다.

---

## 7.2 사용 원칙

- 행동·감정 변화·정보 등장·개그 타이밍을 강화할 때만 사용
- 한 컷에 개수 제한을 기계적으로 두지 않는다.
- 여러 SFX 중첩 허용
- 의미 없이 동시에 많이 겹치는 것은 피한다.

---

## 7.3 볼륨

- Renderer에서 SFX의 기준 음량을 정규화한다.
- 장면별로 필요한 경우 상대 볼륨을 조절한다.
- 개별 원본 음원의 음량 차이를 그대로 사용하지 않는다.

---

## 7.4 타이밍

화면 이벤트가 존재하는 SFX는 해당 사건과 정확히 동기화한다.

예:

- 알림 등장 + `notification`
- 강조된 꿈뻑 1회 + `blink_bubble`
- 강조된 꿈뻑꿈뻑 2회 + `blink_bubble_double`
- 귀 쫑긋/캐릭터 모션 + 상황에 맞는 `cute_move`/`cartoon_*` 계열
- 클릭 시점 + `click`

분위기형 SFX는 구간 재생을 허용한다.

JSON은 순간형과 구간형 모두 지원한다.

---

# 8. BGM Lock

## 8.1 기본 원칙

- BGM은 기본적으로 사용하되, 무음이 더 효과적인 장면에서는 감쇠하거나 잠시 끊는다.
- 특별한 이유가 없다면 한 에피소드의 주된 생활 구간에는 한 곡을 유지한다.
- 감정/장소/사건의 명확한 변화가 있을 때만 곡을 교체한다.
- BGM은 아래 공식 팔레트에서 장면 성격에 따라 선택한다. 무작위 로테이션을 기본값으로 사용하지 않는다.

### 공식 BGM 팔레트 V1.4

- `DAILY_MIZUTAMA` — Mizutama: 대표 일상
- `DAILY_PATCHWORK` — Patchwork: 포근하고 장난스러운 일상
- `DAILY_PRELUDE` — Prelude: 맑고 차분한 일상/아침/작업
- `CHILL_LINEN` — Linen: 여유롭고 느긋한 일상. 게으름 전용 아님
- `EXCITED_APRICOT_COLOR` — Apricot Color: 발견/쇼핑/들뜸
- `HAPPY_PETIT_GIFT` — Petit Gift: 작은 기쁨/외출/오프닝
- `CITY_PARALLAX_CITY` — Parallax City: 도시/카페/쇼핑/외출
- `GLOOMY_VINYL_PIANO` — Vinyl Piano: 현타/조용한 실망
- `PLAYFUL_8WORLD` — 8world: 게임/망상/계산 개그 등 특수 연출 전용
- `INNER_MONOLOGUE_QUIET_NIGHT` — 静かな夜長に: 조용한 독백/내면 정리
- `EMOTIONAL_PEAK` — 예약 키. 아직 곡을 Lock하지 않는다.

DAILY 3곡은 서로 다른 세계관의 곡이 아니라 **같은 몽이 일상 음악 세계 안의 로테이션 풀**로 취급한다.

`INNER_MONOLOGUE`는 명언·교훈을 강조하기 위한 음악이 아니다. 몽이가 자신의 상황을 혼잣말하듯 받아들이거나 정리하는 장면의 배경이다.

## 8.2 감정 전환

곡 교체보다 먼저 볼륨 감소, 짧은 무음, 페이드, 환경음/SFX bridge를 활용한다.

권장 호환성:

- DAILY → DAILY: `◎`
- DAILY → CHILL: `◎`
- DAILY → EXCITED/HAPPY: `◎`
- DAILY → INNER_MONOLOGUE: `◎`
- CHILL → INNER_MONOLOGUE: `◎`
- GLOOMY → INNER_MONOLOGUE: `◎◎` — 대표 감정 전환 후보
- EXCITED/HAPPY → INNER_MONOLOGUE: `△` — 직접 CROSSFADE 금지. 0.3~1.0초 정적/환경음/SFX bridge 권장
- CITY → INNER_MONOLOGUE: `○` — 기존 음악을 먼저 정리
- PLAYFUL_8WORLD → INNER_MONOLOGUE: `×` — 직접 연결 금지

실제 음원 분석 후 BPM/LUFS/인트로·아웃트로를 기준으로 곡별 최적 진입·퇴장 타임코드를 추가 Lock할 수 있다.

## 8.3 Ducking

중요한 SFX가 있을 때 BGM을 잠시 낮추는 `DUCKING`을 지원한다. 모든 SFX에 자동 적용하지 않고 제작실이 필요할 때만 지정한다.

# 9. Transition Lock

기본 전환은 `CUT`이다.

지원 프리셋:

- `CUT`
- `CROSSFADE`
- `FADE_IN`
- `FADE_OUT`
- `FLASH`

`FADE_OUT + BLACK + FADE_IN` 조합으로 검정 전환을 만들 수 있으며 별도의 `FADE_BLACK` 프리셋은 필수로 두지 않는다.

### 사용 원칙

- BGM 박자와 장면 흐름을 고려한다.
- 기본은 즉시 컷 전환
- 시간 경과/감정 연결은 필요 시 `CROSSFADE`
- 시작/종료 또는 큰 단절은 필요 시 `FADE_IN/OUT`
- 충격·발견 강조는 제한적으로 `FLASH`
- 좌우 슬라이드·회전·과도한 와이프는 V1에서 제외

액션 프레임 내부의 `CROSSFADE`와 스토리 컷 간 Transition은 별개로 관리한다.

---

# 10. edit.json V1 구조

에피소드마다 **하나의 `edit.json`**을 사용한다.

영상 전체 정보, 컷, 액션 프레임, 텍스트, SFX, BGM, Transition을 모두 포함한다.

사람이 직접 수정할 수 있도록 의미가 명확한 필드명을 사용한다.

## 예시

```json
{
  "project": {
    "id": "E03",
    "title": "에피소드 제목",
    "format": "shorts",
    "resolution": {
      "width": 1080,
      "height": 1920
    },
    "fps": 30
  },

  "bgm": [
    {
      "name": "daily",
      "start": 0.0,
      "end": 18.6,
      "volume": 1.0,
      "fade_in": 0.4,
      "fade_out": 0.6
    }
  ],

  "cuts": [
    {
      "id": 1,
      "note": "장면 설명 또는 사람이 읽는 편집 메모",
      "image": "images/cut01.png",
      "duration": 2.8,

      "camera": {
        "preset": "ZOOM_IN_SLOW"
      },

      "text": [
        {
          "type": "situation_label",
          "text": "아침",
          "position": "TOP_LEFT",
          "x": 110,
          "y": 160,
          "width": 210,
          "appear_at": 0.0,
          "disappear_at": null,
          "animation": "STATIC"
        }
      ],

      "actions": [],
      "sfx": [],

      "transition_out": {
        "type": "CUT"
      }
    }
  ]
}
```

---

## 10.1 Text Type

Renderer 후합성 기본 허용 타입:

- `situation_label`
- `caption`
- `ui`
- `end_message` — Fixed End Card 전용

`dialogue`와 `thought`는 Renderer Text Type이 아니다. 두 타입은 이미지 생성 단계에서 말풍선과 실제 문구까지 완성한다.

Renderer는 허용된 후처리 `type`에 따라 Edit Lock에 정의된 고정 스타일을 적용한다.

폰트·배경색·padding·둥근 정도 등 디자인 수치를 매 컷 JSON에 반복 기록하지 않는다.

---

## 10.2 Action Type

### IMAGE_SWAP

한 번의 상태 변화 또는 blink 등에 사용한다.

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

### IMAGE_SEQUENCE

꼬리 흔들기 등 여러 프레임 반복에 사용한다.

```json
{
  "type": "IMAGE_SEQUENCE",
  "at": 1.0,
  "frames": [
    { "image": "actions/tail_left.png", "duration": 0.12 },
    { "image": "actions/tail_right.png", "duration": 0.12 }
  ],
  "repeat": 2,
  "return_to_base": true
}
```

---

## 10.3 SFX

순간형 예:

```json
{
  "name": "notification",
  "at": 1.2,
  "volume": 1.0,
  "duck_bgm": true
}
```

구간형 예:

```json
{
  "name": "heartbeat",
  "start": 0.8,
  "end": 2.4,
  "volume": 0.8
}
```

---

## 10.4 사람이 직접 수정 가능한 항목

사용자는 필요할 경우 `edit.json`을 직접 수정할 수 있다.

예:

- 컷 길이
- SFX 타이밍/볼륨
- BGM 볼륨
- Camera preset
- Transition
- Action timing

Renderer 후처리 요소처럼 이미지 자체를 다시 만들 필요가 없는 수정은 JSON 변경 후 재렌더링으로 처리한다. 이미지에 직접 포함된 `dialogue` / `thought`의 문구·위치·말풍선 수정은 이미지 수정 또는 재생성이 필요하다.

---

# 10.5 에피소드 ZIP 패키지 Lock

제작실은 한 에피소드의 기본 컷, 액션 프레임, `edit.json`을 최종 검수 가능한 상태로 정리한 뒤 **에피소드 단위 ZIP 하나**로 제공한다.

기본 구조:

```text
E01_assets.zip
├─ images/
│  ├─ cut01.png
│  ├─ cut02.png
│  └─ ...
├─ actions/
│  ├─ cut02_ears_up.png
│  ├─ cut05_tail_left.png
│  └─ ...
└─ edit.json
```

규칙:

1. `edit.json`은 ZIP 루트에 둔다.
2. `edit.json.project.id`는 해당 에피소드 ID와 일치해야 한다.
3. `edit.json`이 참조하는 모든 기본 이미지와 액션 이미지는 ZIP 안에 실제 존재해야 한다.
4. 정식 파일명은 제작실이 패키징 전에 확정한다. 사용자가 `ChatGPT Image ...` 임시 파일명을 직접 변경하지 않는다.
5. 공용 SFX/BGM/폰트처럼 Renderer `assets/`에서 관리하는 자산은 에피소드 ZIP에 중복 포함하지 않는다.
6. 수정본을 다시 납품할 때도 변경 파일만 따로 보내는 것을 기본으로 하지 않고, **정합성이 보장된 전체 에피소드 ZIP을 다시 제공**한다.
7. Renderer는 동일 project.id의 새 패키지를 가져올 때 기존 프로젝트를 보존 가능한 방식으로 교체할 수 있다.

제작실별 지침에는 이 구조를 중복 기재하지 않고, 항상 최신 Edit Lock을 참조한다.

---

# 11. Renderer Lock

## 11.1 역할

Mongi Renderer는 생성형 AI가 아니다.

역할:

- `edit.json` 읽기
- 기본 이미지 및 액션 이미지 합성
- 카메라 모션 적용
- 후처리 텍스트/라벨 및 Fixed End Card 텍스트 합성
- SFX 삽입
- BGM 삽입 및 Ducking
- Transition 적용
- 최종 MP4 인코딩

Renderer는 Character Lock이나 감정 연출을 스스로 해석해 새 이미지를 만들지 않는다.

---

## 11.2 기본 출력 규격

숏폼 기본:

- 1080 × 1920
- 30fps
- 세로형 MP4

향후 롱폼은 프로젝트 설정으로 별도 해상도/포맷 지정 가능하도록 확장한다.

---

## 11.3 Preflight

렌더링 전에 전체 사전검사를 수행한다.

검사 예:

- `edit.json` 존재 및 파싱 가능 여부
- 기본 컷 이미지 존재
- 액션 프레임 존재
- SFX/BGM asset 존재
- 타이밍 값 유효성
- 컷 duration보다 뒤에 이벤트가 존재하지 않는지
- 지원되지 않는 preset/type 여부

### 오류 처리

- 치명적 오류: 렌더링 중단
- 비치명적 문제: WARNING 출력 후 계속

---

## 11.4 기술적 자동 검증

MP4 생성 후 자동 확인:

- 해상도
- FPS
- 예상 영상 길이
- 오디오 존재 여부
- 파일 손상 여부

이미지에 직접 생성된 말풍선의 미적 품질·가독성·캐릭터 가림 여부와 영상 템포 등 **미적/연출 검수는 Renderer가 자동 판정하지 않는다.**

---

## 11.5 실행 흐름

```text
Preflight
→ Render
→ Technical Validation
→ MP4 Output
→ 사람의 최종 시각/연출 검수
```

최종 V1에서는 `render.bat` 등으로 **원클릭 실행**할 수 있도록 한다.

GUI 편집기는 V1에서 필수로 만들지 않는다.

---

## 11.6 원본 보호

Renderer는 다음 원본을 수정하지 않는다.

- 기본 이미지
- 액션 이미지
- `edit.json`
- SFX/BGM 원본

Renderer는 출력물과 캐시만 생성한다.

---

## 11.7 출력 버전

같은 에피소드를 다시 렌더링할 경우 기존 결과를 덮어쓰기보다 자동 버전 증가를 기본으로 한다.

예:

```text
E03.mp4
E03_v2.mp4
E03_v3.mp4
```

---

## 11.8 컷 단위 캐시

변경되지 않은 컷은 기존 렌더 결과를 재사용한다.

- cut05만 변경 → cut05만 재렌더
- 나머지 컷 → cache 재사용
- 마지막 전체 합성 및 필요 오디오 합성만 다시 실행

향후 롱폼에서도 효율적으로 재렌더링할 수 있도록 V1부터 구조를 고려한다.

---

## 11.9 에피소드 패키지 입력 방식

GPT에서 개별 이미지를 다운로드할 때 `ChatGPT Image + 날짜시간` 형태의 임시 파일명이 생기더라도, **최종 사용자에게 개별 파일명을 수동으로 변경하거나 컷/액션 이미지를 직접 분류시키지 않는다.**

제작실은 제작 완료 시 각 이미지의 역할을 확정하고 정식 파일명으로 정리한 뒤, Renderer에 바로 투입 가능한 **에피소드 단위 ZIP 패키지**로 납품한다.

기본 사용 흐름:

```text
제작실 완성 패키지(E01_assets.zip)
→ 사용자가 Renderer의 inbox/에 ZIP 1개를 넣음
→ render.bat 실행
→ Renderer가 project.id를 읽고 projects/E01을 자동 구성
→ Preflight / Render / Validation
→ output/E01.mp4
```

따라서 일반 사용자 흐름에서는 다음 작업을 요구하지 않는다.

- `E01`, `E02` 등의 프로젝트 폴더 수동 생성
- `new_project.bat` 실행
- ChatGPT 임시 파일명의 수동 변경
- 기본 컷과 액션 프레임의 수동 분류
- 개별 이미지의 순서 추측 Import

핵심 요구사항:

> 사용자는 제작실에서 받은 에피소드 ZIP을 `inbox/`에 넣고 `render.bat`을 실행하는 것만으로 렌더링을 시작할 수 있어야 한다.

---

## 11.10 성공/실패 표시

콘솔형 진행 표시 예:

```text
Mongi Renderer V1

[E03]

✓ edit.json
✓ Assets
✓ Preflight

Rendering...
✓ Cut 01 [cached]
✓ Cut 02 [cached]
→ Cut 03 [rendered]
✓ Audio mix
✓ Final encode
✓ Validation

DONE
output/E03_v2.mp4
```

실패 시 원인을 구체적으로 표시한다.

성공 시 `output` 폴더를 자동으로 열 수 있도록 한다.

---

# 12. Renderer 폴더 구조 Lock

프로그램 코드와 사용자 데이터를 분리한다.

```text
MongiRenderer/
├─ app/                 # Renderer 프로그램 코드. 업데이트 대상
├─ assets/              # 공용 사용자 자산. 업데이트 시 보존
│  ├─ fonts/
│  ├─ sfx/
│  ├─ bgm/
│  └─ LICENSES.json
│
├─ inbox/               # 제작실에서 받은 에피소드 ZIP 투입 위치
├─ projects/            # Renderer가 자동 구성하는 에피소드 데이터
│  ├─ E01/
│  ├─ E02/
│  └─ _history/         # 동일 에피소드 패키지 교체 시 이전본 보관 가능
│
├─ cache/               # 재생성 가능한 렌더 캐시
├─ output/              # 최종 MP4
├─ render.bat
└─ setup_windows.bat
```

업데이트 시 `assets/`, `projects/`, `output/` 등 사용자 데이터 영역을 반복적으로 옮기거나 다시 구성하지 않는 것을 원칙으로 한다.

`app/`은 프로그램 영역이며, 향후 Renderer 업데이트는 가능한 한 프로그램 영역만 교체하도록 설계한다.

---

# 13. 제작 및 납품 순서

```text
작가실 승인 에피소드
→ 제작실이 최신 Character / Personality / World / Voice / Home Lock 확인
→ 제작실이 최신 Mongi Shorts Edit Lock 확인
→ 숏폼 대본 및 컷 설계
→ 대사/생각 Composition Area 및 Renderer 후처리 텍스트 영역을 포함한 화면 구성 설계
→ dialogue/thought가 있는 컷은 Soft Organic Bubble + 실제 문구까지 포함해 기본 컷 이미지 일괄 생성
→ 필요한 액션 프레임 일괄 생성
→ 이미지/연속성 검수
→ 최종 edit.json 작성
→ 정식 파일명 및 폴더 구조 정리
→ 에피소드 ZIP 패키지 생성
→ 사용자 전체 검토
→ Renderer inbox/ 투입
→ Mongi Renderer Preflight
→ 렌더링
→ 기술적 자동 검증
→ MP4 출력
→ 최종 시각/연출 검수
```

제작실은 원칙적으로 각 컷마다 사용자의 승인을 기다리지 않고, 승인된 기획과 최신 Lock을 기준으로 가능한 범위까지 일괄 제작한다. 중요한 설정 충돌이나 사용자 판단 없이는 결정하기 어려운 연출이 있는 경우에만 중간 확인한다.

---

# 14. V1에서 의도적으로 제외하는 것

현재 결과물 품질을 먼저 확인하기 위해 다음 기능은 V1에서 제외한다.

- Live2D
- 몽이 캐릭터 파츠 리깅
- 몽이만 별도 레이어로 움직이는 물리/위치 애니메이션
- 자동 호흡 루프
- 과도한 예능식 Transition
- 복잡한 GUI 편집기
- 생성형 AI를 Renderer 내부에 직접 통합

필요성이 실제 결과물에서 확인되면 V1.2 이상에서 검토한다.

---

# 15. 최종 한 문장

> **몽이 쇼츠는 제작실이 최신 Lock에 따라 이야기·구도·기본 컷·액션 프레임·edit.json을 하나의 에피소드 패키지로 완성하고, 사용자는 그 ZIP을 Renderer에 전달하여 동일한 스타일의 최종 영상을 기계적으로 재현하는 구조로 제작한다.**


---

# 16. Audio Library V1.2

Renderer의 공용 `assets/sfx/`, `assets/bgm/` 라이브러리는 제작실이 임의 파일을 에피소드 ZIP에 중복 포함하는 방식이 아니라 Renderer 공용 자산으로 관리한다.

기본 SFX 키: `click`, `notification`, `pop_soft`, `whoosh_soft`, `ding_soft`, `impact_soft`, `flop`, `sparkle`, `awkward`, `heartbeat`, `success`, `scroll`, `discover`.

기본 BGM 키는 8장의 공식 BGM 팔레트 V1.4를 따른다. `EMOTIONAL_PEAK`는 아직 미지정이다.

제작실은 실제 파일명/확장자를 하드코딩하지 않고 위 논리 키를 `edit.json`에서 사용한다. Renderer는 지원 확장자를 탐색하여 공용 자산을 해석한다.

음향 연출은 짧고 친숙한 숏폼 편집 문법을 따르되 특정 유명 콘텐츠·밈·게임·애니메이션의 음원을 복제하지 않는다. SFX는 사건과 감정 포인트에만 사용하며, 효과음을 넣기 위한 효과음 사용을 금지한다. BGM은 기본적으로 에피소드당 한 트랙을 사용하고 필요 시 Ducking/Fade/Mute로 조절한다.

Audio Library의 실제 음원 교체·확장은 Renderer 자산 업데이트로 처리하며, 논리 키나 JSON 계약이 바뀌지 않는 한 제작실 지침을 수정하지 않는다. JSON 계약이 바뀌는 경우에만 최신 Edit Lock을 함께 갱신한다.

---

# 17. V1.5~V1.7.2 누적 변경사항

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

이 섹션에서 변경하지 않은 제작·패키지·Renderer 규칙은 이 문서 앞부분의 본체 규칙을 그대로 따른다.

---

# Mongi Shorts Edit Lock V1.6 — Fixed End Card System

V1.6에서 고정 End Card 시스템을 추가한다. 이 문서의 기존 Audio Library, `source_start`, BGM 역할군, 전환 원칙 및 본체 규칙은 아래에서 명시적으로 변경하는 경우를 제외하고 그대로 유지한다.

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
- 이 문서의 V1.5 BGM source-segment 및 transition 규칙을 그대로 적용한다.

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

이 문서의 기존 규칙은 계속 유효하며, V1.6은 End Card 시스템이 명시적으로 요구하는 부분만 추가·대체한다.


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

## Typewriter text animation — Retired for dialogue / thought

V1.9부터 `dialogue` / `thought`는 이미지 생성 단계에서 완성되므로 Renderer `TYPEWRITER`를 사용하지 않는다.

`TYPEWRITER`는 Mongi dialogue/thought 공식 계약에서 제외한다. 향후 다른 Renderer 후처리 텍스트에 필요할 경우 별도 승인 규격으로 다시 정의한다.


## Interaction timing and preflight

Production MUST author actions only from the official action types defined by the active Edit Lock / Renderer contract. Renderer Preflight MUST reject unknown action types rather than silently ignoring them.

For click scenes, the intended order should be legible in the rendered result:

`cursor movement → target acquisition → click visual → synchronized click SFX / UI response`

When a UI exists on a tilted or perspective display surface, the UI composition remains subject to the existing visual continuity rules; cursor support does not excuse mismatched screen perspective.

## Compatibility

V1.7에서 추가된 `CURSOR_MOVE` / `CURSOR_CLICK` 계약은 유지한다. `TYPEWRITER`의 dialogue/thought 적용은 V1.9에서 폐기한다. Existing `IMAGE_SWAP` / `IMAGE_SEQUENCE`, camera, transition, Audio V1, and End Card rules remain active.


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

V1.7.2에서 도입된 Soft Organic Bubble의 **시각 방향은 V1.9 Section 5.2로 승계**한다.

V1.7.2의 Renderer procedural bubble 생성, Renderer dialogue/thought 합성, TYPEWRITER 호환 계약은 V1.9에서 폐기되었다.

현재 유효한 규칙은 다음과 같다.

- `dialogue` / `thought` = 이미지 생성 단계에서 말풍선 + 실제 문구까지 완성
- 공식 Visual Style Reference = `Mongi-Soft-Organic-Bubble-Visual-Reference-V1.0.png`
- Renderer = dialogue/thought 말풍선 및 내부 텍스트를 생성하거나 후합성하지 않음


---

# 18. 버전 관리 Lock

앞으로 Edit Lock 업데이트는 **패치 문서만 단독 최신본으로 만들지 않는다.**

새 버전은 반드시 직전 최신 **전체 누적본(standalone)** 을 기준으로 수정하며,
배포되는 최신 Edit Lock 파일 하나에 현재 유효한 모든 규칙이 실제로 포함되어 있어야 한다.

- `extends Vx.x` 문장만으로 이전 파일의 규칙을 외부 의존하지 않는다.
- 과거 파일은 변경 이력/감사용으로만 보관할 수 있다.
- 제작실과 Renderer는 항상 최신 standalone Edit Lock 하나를 기준으로 동작한다.
- 규칙이 충돌하면 문서 내 더 최신 버전 섹션이 우선한다.
