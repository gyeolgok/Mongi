# Mongi Production + Renderer

Mongi 숏폼의 Canon, 연속성, 에피소드 승인 상태와 로컬 Renderer를 함께 관리하는 저장소입니다.

모든 AI 작업 채팅과 사람 작업자는 먼저 [`START_HERE.md`](START_HERE.md)를 읽습니다.

## 현재 기준

- Renderer: V1.7.0
- Mongi Shorts Edit Lock: V1.9 Consolidated Standalone
- 출력 기본값: 1080×1920 / 30fps
- 입력: 승인 정보가 포함된 에피소드 ZIP

## 저장소 구조

```text
Mongi/
├─ START_HERE.md
├─ governance/         # 역할, 읽기 범위, 승인·반려, 저장 정책
├─ canon/              # 공식 텍스트 Lock과 Library 자산 manifest
├─ continuity/         # 현재 상태, 연대기, 공개 사실, 미회수 서사
├─ channel/            # 게시 실험과 성과 원장
├─ episodes/           # 에피소드별 brief/script/review/status
├─ schemas/            # 기계 검증용 계약
├─ app/                # Renderer 프로그램
├─ docs/               # Edit Lock과 edit.json 규격
├─ assets/             # 공용 폰트/SFX/BGM
├─ inbox/              # 에피소드 ZIP 투입
├─ projects/           # 자동 구성된 에피소드 작업 데이터
├─ cache/              # 재생성 가능한 캐시
└─ output/             # 최종 MP4
```

공식 레퍼런스 이미지와 최종 영상 등 대용량 자산은 ChatGPT Library에 보관하고, Git에는 [`canon/ASSET_MANIFEST.md`](canon/ASSET_MANIFEST.md)로 정확한 파일명을 기록합니다.

## 에피소드 ZIP 규격

```text
E001_assets.zip
├─ images/
├─ actions/
├─ edit.json
└─ approval.json
```

`approval.json`에는 최소한 다음 두 게이트가 승인되어 있어야 합니다.

- `approvals.script.status`: `APPROVED`
- `approvals.assets.status`: `APPROVED`

승인되지 않은 패키지는 Renderer Preflight에서 중단됩니다. `FINAL_APPROVED`는 렌더 후 게시 단계에서 별도로 확인합니다.

## 일반 사용법

1. 승인된 `E001_assets.zip`을 압축 해제하지 않고 `inbox/`에 넣습니다.
2. Windows에서 `render.bat`을 실행합니다.
3. Renderer가 패키지를 `projects/E001/`에 구성합니다.
4. Approval Gate → Preflight → Render → Validation을 실행합니다.
5. 결과는 `output/E001.mp4`에 생성되고, 처리한 ZIP은 `inbox/processed/`로 이동합니다.

## Edit Lock V1.9 핵심 호환성

- `dialogue`와 `thought`는 이미지 생성 단계에서 말풍선과 실제 문구까지 완성합니다.
- Renderer는 `dialogue`/`thought`를 새로 생성하거나 후합성하지 않습니다.
- `TYPEWRITER`는 공식 계약에서 폐기되어 Preflight에서 거부됩니다.
- Renderer 후합성 텍스트는 `situation_label`, `caption`, `ui`, `end_message`입니다.
- 마지막 컷은 `type: end_card`, `STATIC` 카메라와 비어 있지 않은 `end_message`가 필요합니다.

전체 계약은 [`docs/Mongi-Shorts-Edit-Lock-V1.9-Consolidated.md`](docs/Mongi-Shorts-Edit-Lock-V1.9-Consolidated.md)와 [`docs/EDIT_JSON_REFERENCE.md`](docs/EDIT_JSON_REFERENCE.md)를 따릅니다.

## 요구사항

- Python 3.10+
- Pillow
- FFmpeg / ffprobe

Windows 최초 실행 시 `setup_windows.bat`을 사용합니다.

## 기존 프로젝트 보호

- 같은 `project.id`의 새 패키지는 기존 작업을 `projects/_history/`에 백업합니다.
- `assets/`, `projects/`, `output/`은 프로그램 업데이트 시 보존합니다.
- 캐시와 출력물은 Git에서 제외합니다.
