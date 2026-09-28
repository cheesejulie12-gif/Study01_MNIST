"""학습: 손글씨 숫자(sklearn digits)를 굵기/기울기/크기를 바꿔 늘린 뒤 MLP로 학습하고 web_version/weights.json으로 내보낸다."""
import json, numpy as np
from scipy import ndimage as ndi
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from preprocess import preprocess
from strokes import draw_digit

rng = np.random.default_rng(0)
def stroke(img8):
    z = ndi.zoom(img8 / 16.0, 8, order=1)
    z = ndi.gaussian_filter(z, rng.uniform(1.5, 4))
    z = np.clip((z - rng.uniform(0.08, 0.45) * z.max()) / (0.15 * z.max()), 0, 1)
    ang = np.deg2rad(rng.uniform(-14, 14)); sh = rng.uniform(-0.25, 0.25); sc = rng.uniform(0.8, 1.15, 2)
    M = np.array([[np.cos(ang), -np.sin(ang) + sh], [np.sin(ang), np.cos(ang)]]) @ np.diag(1 / sc)
    z = ndi.affine_transform(z, M, offset=32 - M @ [32, 32], order=1)
    return ndi.gaussian_filter(z, 0.8)

def make(X, y, n):
    F, L = [], []
    for k in range(n):
        i = rng.integers(len(X)); f = preprocess(stroke(X[i]))
        if f is not None: F.append(f); L.append(y[i])
    return np.array(F), np.array(L)

def make_strokes(n):
    F, L = [], []
    for k in range(n):
        c = int(rng.integers(10)); f = preprocess(draw_digit(c, rng))
        if f is not None: F.append(f); L.append(c)
    return np.array(F), np.array(L)

d = load_digits(); Xtr, Xte, ytr, yte = train_test_split(d.images, d.target, test_size=0.25, random_state=1)
F, L = make(Xtr, ytr, 40000); Ft, Lt = make(Xte, yte, 3000)
F2, L2 = make_strokes(25000); F3, L3 = make_strokes(2000)
F, L = np.vstack([F, F2]), np.concatenate([L, L2])
clf = MLPClassifier((256, 128), max_iter=40, random_state=0).fit(F, L)
print("손글씨 데이터(검증용) 정확도", clf.score(Ft, Lt)); print("획 그림(검증용) 정확도", clf.score(F3, L3))
json.dump({"W": [np.round(w, 3).tolist() for w in clf.coefs_], "b": [np.round(b, 3).tolist() for b in clf.intercepts_]},
          open("../web_version/weights.json", "w"), separators=(",", ":"))
