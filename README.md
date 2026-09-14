# Mongi Renderer V1.6

최신 `Mongi Shorts Edit Lock V1.5`의 에피소드 ZIP 납품 방식을 따르는 로컬 Renderer.

## 일반 사용법

1. 제작실에서 `E01_assets.zip` 같은 완성 패키지를 받는다.
2. ZIP을 **풀지 말고** `inbox/`에 넣는다.
3. `render.bat`을 더블클릭한다.
4. Renderer가 자동으로 ZIP의 `edit.json`에서 `project.id`를 읽고 `projects/E01/`을 구성한다.
5. Preflight → Render → Validation을 거쳐 `output/E01.mp4`를 만든다.
6. 처리 완료 ZIP은 `inbox/processed/`로 이동한다.

사용자가 할 필요가 없는 것:
- E01/E02 폴더 수동 생성
- ChatGPT Image 파일명 변경
- images/actions 수동 분류
- new_project.bat 실행
- edit.json 경로를 render.bat에 드래그

## 에피소드 ZIP 규격

```text
E01_assets.zip
├─ images/
│  ├─ cut01.png
│  └─ ...
├─ actions/
│  └─ ...
└─ edit.json
```

`edit.json`은 ZIP 루트에 있어야 하며 내부의 파일 경로와 실제 ZIP 파일명이 일치해야 한다.

## 프로그램 / 사용자 데이터 분리

```text
MongiRenderer/
├─ app/          # 프로그램 코드
├─ assets/       # 폰트 / 공용 SFX / BGM
├─ inbox/        # 에피소드 ZIP 투입
├─ projects/     # 자동 구성된 에피소드
├─ cache/
├─ output/
├─ render.bat
└─ setup_windows.bat
```

향후 업데이트는 `app/`과 실행 스크립트를 중심으로 교체하며 `assets/`, `projects/`, `output/`을 보존하는 것을 원칙으로 한다.

## 기존 V1 폴더에서 데이터 가져오기

새 Renderer 버전을 별도 폴더에 설치했다면 `migrate_legacy.bat`을 한 번 실행하고 기존 MongiRenderer 폴더 경로를 입력하면 기존 `assets/`, `projects/`, `output/`의 파일을 새 구조에 복사한다. 이미 존재하는 파일은 덮어쓰지 않는다.

## 수정 패키지

같은 `project.id`의 새 ZIP이 들어오면 기존 `projects/<ID>/`는 `projects/_history/<ID>/<timestamp>/`에 백업한 후 새 패키지로 교체한다.

## 요구사항

- Python 3.10+
- Pillow
- FFmpeg / ffprobe

Windows에서는 최초 1회 `setup_windows.bat`을 실행한다.

## V1.2에서 유지되는 편집 기능

- 1080×1920 / 30fps 기본 출력
- Preflight
- Camera presets
- IMAGE_SWAP / IMAGE_SEQUENCE
- Text/Bubble
- CUT / CROSSFADE / FADE_IN / FADE_OUT / FLASH
- SFX / BGM / Ducking
- 컷 캐시
- 출력 버전 증가
- ffprobe 기술 검증



## Audio Library V1.5
- SFX: V1.3.1 통합 29종 유지
- BGM: 합성 placeholder 제거, 확정 실제 선곡 10곡을 공식 팔레트로 등록
- `assets/bgm_sources.json`: 곡별 공식 출처/논리 키
- `install_bgm.bat`: 공식 배포 페이지에서 원본을 설치하는 보조 기능
- 사이트 구조 변경 시 자동 설치가 실패할 수 있으며 그 경우 manifest의 공식 페이지에서 수동 다운로드한다.
- 기존 `assets/fonts/` 사용자 파일은 업데이트 시 보존한다.

전환 규칙은 `docs/AUDIO_LIBRARY.md` 참고.


### V1.5 BGM source offsets
BGM assets are integrated. Production should use the recommended windows in `assets/bgm_segments.json`; Renderer supports `source_start` so tracks are not forced to begin at 0:00.

## V1.6 안정성 변경

- `render.bat` 실행 시 `app/bootstrap.py`가 Pillow / FFmpeg / ffprobe / 로컬 Edit Lock / Audio V1 메타데이터를 먼저 점검한다.
- Pillow가 빠진 경우 가능한 환경에서는 `app/requirements.txt`를 자동 설치한다.
- 로컬 제작 규격 사본은 `docs/Mongi-Shorts-Edit-Lock-V1.5.md`다. Renderer 버전과 Edit Lock 버전은 서로 다른 버전 트랙이다.
- `scroll`, `discover`, `flop`, `success`, `pop_soft` 같은 구형 SFX 키가 현재 라이브러리에 없으면 `LEGACY SFX KEY`로 명시한다. Renderer가 임의의 다른 소리로 자동 치환하지 않는다.
- 카메라 프리셋의 시각 강도는 V1.5와 동일하다. 에피소드별 과도한 카메라 흔들림은 제작 패키지에서 수정한다.
