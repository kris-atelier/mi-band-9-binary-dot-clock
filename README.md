# Mi Band 9 Minimal Binary Dot Clock

Mi Band 9의 192×490 화면을 기준으로 한 검은 배경의 미니멀 바이너리 시계 원본 패키지입니다.

## 화면 설계

```text
AM/PM 1bit
시 4bit
시와 분 사이의 넓은 간격
분 6bit
```

- 숫자, 영문, 날짜, 심박, 걸음 수, 날씨를 표시하지 않습니다.
- 왼쪽부터 `AM/PM 1bit`, 12시간제 시각의 4비트, 넓은 구분 간격, 분의 6비트입니다.
- 비트는 MSB→LSB 순서입니다. 예: 7시는 `0111`, 5분은 `000101`입니다.
- 켜진 비트는 흰색 꽉 찬 원, 꺼진 비트는 매우 어두운 회색 빈 원입니다.
- 12시는 `1100`으로 표현합니다. 오전/오후는 별도 점 하나로 구분합니다.
- AM/PM 점과 시 비트 사이에는 넓은 간격을 둡니다.
- 초는 원형 점과 별개인 얇은 세로 레일의 흰색 틱으로 표시합니다. 틱은 0초에서 위, 59초에서 아래에 옵니다.
- 배터리가 20% 이하이면 AM/PM 슬롯을 빨간색 점으로 바꿔 충전 필요를 표시합니다. 이때는 AM/PM보다 충전 경고를 우선합니다.

## 파일 구성

- `src/time-to-bits.js`: 실제 시간을 비트 배열로 바꾸는 순수 JavaScript 모듈
- `src/watchface-config.json`: 192×490 좌표와 색상 설정
- `src/preview.html`: 브라우저/에뮬레이터에서 현재 시간을 렌더링하는 독립 미리보기
- `assets/dot-on.png`, `assets/dot-off.png`: 워치페이스 엔진에 재사용할 PNG 원형 자산
- `assets/preview-192x490-elongated-90.png`, `assets/preview-192x490-elongated-270.png`: 긴 세로 배치와 초 틱 참고 이미지

## Mi Create로 가져가기

이 프로젝트는 [Mi Create](https://github.com/ooflet/Mi-Create)로 옮기기 전 단계의 소스·자산 패키지입니다. 원본 도구는 `vendor/Mi-Create` Git submodule로 연결합니다. Mi Create는 Mi Band 9, `.fprj` 프로젝트, AOD 편집과 미리보기를 지원합니다. 실제 `.face` 컴파일은 Mi Create에서 대상 기기를 선택한 뒤 이 프로젝트의 PNG와 `watchface-config.json` 좌표를 배치해 진행합니다.

macOS 쪽 파일 검증과 향후 BLE 연동은 [miband9-cli](https://github.com/kris-atelier/miband9-cli)를 `tools/miband9-cli` submodule로 연결합니다. 현재 CLI의 BLE 설치 명령은 안전한 placeholder이며, 검증되지 않은 Xiaomi 프로토콜을 임의로 전송하지 않습니다.

Submodule까지 받으려면 다음처럼 초기화합니다.

```text
git clone --recurse-submodules <repository-url>
```

Mi Create는 비공식 오픈소스 도구이며, 공식 Xiaomi 앱이나 Xiaomi SDK가 아닙니다. 현재 공개 패키지는 특정 도구의 내부 프로젝트 파일을 임의로 만들어 넣지 않고, 검증 가능한 자산과 매핑 정보를 보존하는 형태입니다.

## 에뮬레이터/시뮬레이터 시험

`src/preview.html`을 브라우저에서 열면 현재 시간이 자동으로 갱신됩니다. 워치페이스 엔진에서는 `time-to-bits.js`의 `getDisplayState(new Date())` 결과를 11개의 비트 슬롯에 연결하면 됩니다.

기본 방향은 90°이며, 270° 방향은 다음처럼 확인할 수 있습니다. 비트 행 전체를 192×490 화면의 긴 축에 맞춰 세로로 사용하며, 시와 분 사이의 큰 간격이 구분자 역할을 합니다.

```text
src/preview.html?rotation=270
```

배터리 경고 미리보기는 다음처럼 확인할 수 있습니다.

```text
src/preview.html?battery=18
```

두 방향 모두 화면 중심을 기준으로 회전하므로, 실제 밴드 포맷에서는 `orientation`을 `90` 또는 `270`으로 선택하면 됩니다.

```js
const state = getDisplayState(new Date());
// state.amPm: 0 또는 1
// state.hourBits: 길이 4, MSB→LSB
// state.minuteBits: 길이 6, MSB→LSB
// getDisplayState(date, batteryPercent)에서 batteryPercent <= 20이면
// state.amPmVisible=1, state.amPmColor='#FF3B30'이 됩니다.
```

## iPhone 사용과 설치 단계

일상적인 Mi Band 9 연결과 설정은 iPhone의 Mi Fitness에서 진행합니다. 이 저장소는 제작용 PC 프로젝트이며, Mi Fitness가 iPhone에서 외부 커스텀 워치페이스 파일을 직접 가져오는지는 지역·버전·지원 방식에 따라 별도 확인이 필요합니다.

1. 대상 Mi Band 9의 실제 커스텀 워치페이스 포맷과 해상도/좌표 규칙을 확인합니다.
2. `watchface-config.json`의 좌표와 자산을 해당 포맷의 JSON·이미지 리소스로 매핑합니다.
3. `src/time-to-bits.js`의 상태값을 엔진의 시간 변수/스크립트 문법으로 옮깁니다.
4. iPhone의 Mi Fitness에서 공식적으로 가져올 수 있는지 확인하고, 가능하지 않으면 파일 제작/검증과 밴드 전송 경로를 분리합니다.

공식 앱이 허용하지 않는 사이드로드나 비공식 BLE 도구를 사용할 때는 밴드와 계정의 안전성을 먼저 확인하세요.
