# Mongi Renderer V1.7.0

Edit Lock V1.9와 장기 프로젝트 운영 구조를 반영한 버전이다.

## 주요 변경

- `approval.json`을 에피소드 ZIP 필수 파일로 지정
- `SCRIPT_APPROVED`, `ASSET_APPROVED`가 없으면 Preflight 중단
- `dialogue`/`thought` Renderer 후합성 차단
- `TYPEWRITER` 차단
- End Card의 `STATIC` 카메라·빈 액션 계약 강제
- `-Consolidated` 접미사가 있는 Edit Lock을 최신 버전으로 인식
- START HERE, 역할, 최소 열람표, 연속성 및 에피소드 템플릿 추가

## 호환성 주의

기존 ZIP에는 `approval.json`이 없으므로 그대로는 V1.7.0에서 렌더링되지 않는다. 실제 검수 후 `episodes/_template/approval.json` 형식의 승인 파일을 추가해야 한다. 과거 패키지에 승인을 자동 부여하지 않는다.

