# 공식 자산 Manifest

이미지 원본은 ChatGPT Library의 `/Mongi`에 보관한다. 파일명이 일치하는 자산만 공식 레퍼런스로 사용한다.

## Character Lock V1.0

| 우선순위/역할 | Library 파일명 |
|---|---|
| 기본 외형·색상·정체성 | `01_Mongi_Master_Guide.png` |
| 귀 움직임 | `02_Ear_Guide.png` |
| 꼬리 움직임 | `03_Tail_Guide.png` |
| 귀 완전 상승 | `04_Ears_Up_Surprise.png` |
| 허탈·공허·체념 | `05_Resignation_Tear.png` |
| 신체 비율·각도 | `06_Turnaround_Reference.png` |
| 일반 표정·감정 | `07_Expression_and_ Emotion_Reference.png` |

충돌 시 각 요소를 전문적으로 정의한 자산이 우선하며 세부 우선순위는 Character Lock을 따른다.

## Home Lock V1.0

| Set/Camera | Library 파일명 | 역할 |
|---|---|---|
| `SET_HOME_001@1.0` | `Mongi-Home-Floorplan-V1.0-Final-v2.png` | 절대 평면 구조·방향 |
| `CAM_HOME_A` | `Mongi-Home-View-A-Final-v2.png` | 현관·주방 쪽에서 창문 방향 |
| `CAM_HOME_B` | `Mongi-Home-View-B-Final-v2.png` | 침대·창문 쪽에서 현관 방향 |
| `CAM_HOME_C` | `Mongi-Home-View-C-Final-v1.png` | 현관의 침대 쪽 3/4 변형 |

상세 위치·가시 요소·Prop ID는 `continuity/sets/SET_REGISTRY.yaml`을 따른다. 위 이미지는 서로 다른 방이 아니라 같은 Set의 시점별 레퍼런스이며 좌우 반전을 허용하지 않는다.

## Bubble

- `Mongi-Soft-Organic-Bubble-Visual-Reference-V1.0.png`

## 자산 변경 원칙

- 동일 이름의 비공식 시안을 공식 파일로 덮어쓰지 않는다.
- 공식 자산 교체와 Hard Lock 변경은 Owner 승인 및 `CHANGELOG.md` 기록이 필요하다.
- 공식 레퍼런스의 Set/Camera 역할을 바꾸지 않는다.
- 에피소드 제작 시 필요한 자산만 불러온다.
