// 전처리: desktop_version/preprocess.py와 같은 계산 (여백 자르기 -> 14칸으로 축소 -> 무게중심을 16x16 중앙으로)
function areaWeights(nIn, nOut) {
  const W = Array.from({ length: nOut }, () => new Array(nIn).fill(0)), span = nIn / nOut;
  for (let i = 0; i < nOut; i++) {
    const a = i * span, b = (i + 1) * span;
    for (let j = Math.floor(a); j < Math.min(nIn, Math.ceil(b)); j++)
      W[i][j] = Math.max(0, Math.min(b, j + 1) - Math.max(a, j)) / span;
  }
  return W;
}
export function preprocess(ink, H, Wd) { // ink: 길이 H*Wd, 잉크=1
  let y0 = H, y1 = -1, x0 = Wd, x1 = -1;
  for (let y = 0; y < H; y++) for (let x = 0; x < Wd; x++) if (ink[y * Wd + x] > 0.1) {
    y0 = Math.min(y0, y); y1 = Math.max(y1, y); x0 = Math.min(x0, x); x1 = Math.max(x1, x);
  }
  if (y1 < 0) return null;
  const h = y1 - y0 + 1, w = x1 - x0 + 1, s = 14 / Math.max(h, w);
  const nh = Math.max(1, Math.floor(h * s + 0.5)), nw = Math.max(1, Math.floor(w * s + 0.5));
  const Wy = areaWeights(h, nh), Wx = areaWeights(w, nw);
  const r = Array.from({ length: nh }, (_, i) => Array.from({ length: nw }, (_, k) => {
    let v = 0;
    for (let y = 0; y < h; y++) { const wy = Wy[i][y]; if (!wy) continue;
      for (let x = 0; x < w; x++) { const wx = Wx[k][x]; if (wx) v += wy * wx * ink[(y0 + y) * Wd + x0 + x]; } }
    return v;
  }));
  let tot = 0, cy = 0, cx = 0;
  for (let i = 0; i < nh; i++) for (let k = 0; k < nw; k++) { tot += r[i][k]; cy += r[i][k] * i; cx += r[i][k] * k; }
  cy /= tot; cx /= tot;
  const oy = Math.min(Math.max(Math.floor(7.5 - cy + 0.5), 0), 16 - nh), ox = Math.min(Math.max(Math.floor(7.5 - cx + 0.5), 0), 16 - nw);
  const out = new Float64Array(256); let mx = 0;
  for (let i = 0; i < nh; i++) for (let k = 0; k < nw; k++) { out[(oy + i) * 16 + ox + k] = r[i][k]; mx = Math.max(mx, r[i][k]); }
  return out.map(v => v / mx);
}
