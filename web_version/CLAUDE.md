# web_version

- 실행: 이 폴더에서 `python3 -m http.server` 후 http://localhost:8000 (`file://`로 열면 `weights.json`을 못 읽어 동작하지 않는다)
- 파일: `index.html`(화면), `style.css`, `app.js`(그림판과 결과 표시), `preprocess.js`(전처리), `model.js`(순전파), `weights.json`(가중치)
- `weights.json` 형식: `{"W": [층별 가중치 행렬 3개], "b": [층별 편향 3개]}`, 구조는 256 -> 256 -> 128 -> 10
- `preprocess.js`는 `desktop_version/preprocess.py`와 결과가 같아야 한다. 외부 라이브러리는 쓰지 않는다.
- 가중치를 바꾸려면 `desktop_version/train.py`를 다시 실행한다.
