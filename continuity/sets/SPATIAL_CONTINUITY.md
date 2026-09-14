# Spatial / Set Continuity

이 문서는 반복 장소의 구조를 에피소드마다 다시 해석하지 않도록 하는 제작 규칙이다. 공간의 창작 권위는 기존 Canon Lock에 있으며, 이 체계는 그 내용을 제작용 ID로 참조한다.

## 최소 단위

- **Set ID**: 반복 장소와 버전. 예: `SET_HOME_001@1.0`
- **Camera ID**: 확정된 카메라 위치와 방향. 예: `CAM_HOME_A`
- **Prop ID**: 반복되거나 식별성이 중요한 소품. 예: `PROP_HOME_BED_001`
- **TEMP**: 한 에피소드에서만 쓰는 소품. 예: `TEMP:E001_PHONE`

모든 사소한 물건에 ID를 부여하지 않는다. 두 컷 이상에서 위치·방향이 이어져야 하거나 다른 에피소드에 다시 등장할 물건만 Prop ID로 등록한다.

## 변경 등급

| 등급 | 의미 | 변경 권한 |
|---|---|---|
| HARD | 구조, 방향, 개수, 식별 디자인. 좌우 반전 포함 임의 변경 금지 | Owner가 Canon/Set 버전 개정 승인 |
| SOFT | 계절, 조명, 생활 흔적처럼 허용 범위 안에서 변형 가능 | Studio 제안, Continuity 검수 |
| FREE | 에피소드성 소품·일시적 배치 | Studio, 단 Hard 구조를 가리거나 모순시키지 않음 |

## 좌우 반전 금지

- Set이 포함된 생성 이미지와 재사용 배경에 horizontal flip, mirror, mirrored composition을 적용하지 않는다.
- 캐릭터 방향을 바꾸기 위해 배경을 뒤집지 않는다. 필요한 경우 몽이 레이어·포즈를 별도로 생성한다.
- 문·창문·침대·주방·책상 같은 방향성 앵커가 프레임에 보이면 Set Registry와 Camera ID로 검증한다.
- 새로운 카메라가 필요하면 기존 이미지를 뒤집지 말고 평면도 위에 위치와 시선을 먼저 정의한다.

## 제작 연결

1. Story Writer는 장소만 지정하고 Camera/Prop ID를 억지로 결정하지 않는다.
2. Studio Producer는 Emotion Previz의 모든 공간 컷에 Set ID와 Camera ID를 기록한다.
3. 등록 카메라로 표현하기 어려운 컷은 `CAM_CANDIDATE_<name>`으로 제안하고 자산 생성 전에 Continuity 승인을 받는다.
4. Continuity Supervisor는 Previz Review에서 구조·방향·가시 요소·좌우 반전을 검수한다.
5. `PREVIZ_APPROVED` 이후 Studio는 승인된 ID를 asset manifest와 이미지 생성 입력에 유지한다.
6. Asset Review는 생성 결과가 ID와 공식 시각 레퍼런스에 일치하는지 다시 확인한다.

## 시각 레퍼런스

Set Registry의 `visual_references`는 ChatGPT Library의 정확한 파일명을 기록한다. 텍스트와 이미지가 충돌하면 Owner 결정과 Canon Lock의 우선순위를 따르며 임의로 평균내지 않는다.

Environment Reference Sheet가 추가되면 기존 Set의 `visual_references`에 파일명과 역할을 추가한다. Hard 구조가 바뀌면 같은 버전을 덮어쓰지 않고 Set 버전을 올린다.
