"""전처리: 그림(잉크=1, 배경=0) -> 16x16 입력. 웹 버전 preprocess.js와 같은 계산을 한다."""
import numpy as np

def area_weights(n_in, n_out):
    W = np.zeros((n_out, n_in)); span = n_in / n_out
    for i in range(n_out):
        a, b = i * span, (i + 1) * span
        for j in range(int(a), min(n_in, int(np.ceil(b)))):
            W[i, j] = max(0.0, min(b, j + 1) - max(a, j)) / span
    return W

def preprocess(ink):
    ys, xs = np.where(ink > 0.1)
    if len(ys) == 0:
        return None
    crop = ink[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h, w = crop.shape; s = 14.0 / max(h, w)
    nh, nw = max(1, int(np.floor(h * s + 0.5))), max(1, int(np.floor(w * s + 0.5)))
    r = area_weights(h, nh) @ crop @ area_weights(w, nw).T
    tot = r.sum()
    cy = (r.sum(1) * np.arange(nh)).sum() / tot; cx = (r.sum(0) * np.arange(nw)).sum() / tot
    oy = int(min(max(np.floor(7.5 - cy + 0.5), 0), 16 - nh)); ox = int(min(max(np.floor(7.5 - cx + 0.5), 0), 16 - nw))
    out = np.zeros((16, 16)); out[oy:oy + nh, ox:ox + nw] = r
    return (out / out.max()).reshape(-1)
