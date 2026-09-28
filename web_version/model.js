// 순전파: 입력 256 -> 256 -> 128 -> 10 (ReLU, 소프트맥스). 외부 라이브러리 없음.
export function predict(weights, x) {
  let a = Array.from(x);
  for (let l = 0; l < weights.W.length; l++) {
    const W = weights.W[l], b = weights.b[l], out = b.slice();
    for (let i = 0; i < a.length; i++) if (a[i] !== 0) for (let j = 0; j < out.length; j++) out[j] += a[i] * W[i][j];
    a = l < weights.W.length - 1 ? out.map(v => Math.max(0, v)) : out;
  }
  const m = Math.max(...a), e = a.map(v => Math.exp(v - m)), s = e.reduce((p, q) => p + q, 0);
  return e.map(v => v / s);
}
