# Study01_MNIST

손글씨 숫자(0~9) 인식 프로그램을 두 가지 버전으로 나누어 관리한다.

- `web_version/`: 순수 자바스크립트, GitHub Pages 배포용 (루트 `index.html`은 이쪽으로 이동시킴)
- `desktop_version/`: 파이썬. 학습(`train.py`)과 데스크톱 앱(`app.py`)

## 공통 규칙
- 전처리는 두 버전이 같아야 한다: 여백 자르기 -> 긴 변을 14칸으로 축소 -> 무게중심을 16x16 중앙으로 이동. 고칠 때는 `preprocess.py`와 `preprocess.js`를 함께 고친다.
- 가중치는 `web_version/weights.json` 하나를 두 버전이 공유한다.
- 페이지 맨 위 학번/이름 표시(`index.html`의 `#student`)는 지우지 않는다.
