# desktop_version

- `train.py`: 학습 데이터를 늘려(`strokes.py`의 획 그림 + 손글씨 숫자 변형) 학습하고 `../web_version/weights.json`을 만든다. 이 폴더 안에서 실행한다: `python3 train.py`
- `preprocess.py`: 전처리 (웹의 `preprocess.js`와 같은 계산)
- `strokes.py`: 직접 그린 것 같은 획 숫자를 만드는 학습용 도구
- `app.py`: Tkinter 데스크톱 앱. `python3 app.py`
- 필요한 패키지: numpy, scipy, scikit-learn, pillow
