import { preprocess } from "./preprocess.js";
import { predict } from "./model.js";
const cv = document.getElementById("pad"), ctx = cv.getContext("2d"), out = document.getElementById("result");
let weights = null, drawing = false, last = null;
function clear() { ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, 280, 280); out.textContent = "숫자를 그려 보세요"; document.getElementById("top").innerHTML = ""; }
function pos(e) { const r = cv.getBoundingClientRect(); return [(e.clientX - r.left) * 280 / r.width, (e.clientY - r.top) * 280 / r.height]; }
function recognize() {
  if (!weights) { out.textContent = "모델을 불러오는 중입니다"; return; }
  const d = ctx.getImageData(0, 0, 280, 280).data, ink = new Float64Array(280 * 280);
  for (let i = 0; i < ink.length; i++) ink[i] = 1 - d[i * 4] / 255;
  const x = preprocess(ink, 280, 280);
  if (!x) { out.textContent = "숫자를 그려 보세요"; return; }
  const p = predict(weights, x), rank = p.map((v, i) => [v, i]).sort((a, b) => b[0] - a[0]);
  out.textContent = String(rank[0][1]);
  document.getElementById("top").innerHTML = rank.slice(0, 3).map(([v, i]) => `<li>${i} : ${(v * 100).toFixed(1)}%</li>`).join("");
}
cv.addEventListener("pointerdown", e => { drawing = true; last = pos(e); cv.setPointerCapture(e.pointerId); });
cv.addEventListener("pointermove", e => {
  if (!drawing) return; const p = pos(e);
  ctx.strokeStyle = "#000"; ctx.lineWidth = 20; ctx.lineCap = "round"; ctx.beginPath(); ctx.moveTo(...last); ctx.lineTo(...p); ctx.stroke(); last = p; recognize();
});
const stop = () => { drawing = false; };
cv.addEventListener("pointerup", stop); cv.addEventListener("pointercancel", stop);
document.getElementById("clear").addEventListener("click", clear);
clear();
fetch("weights.json").then(r => r.json()).then(w => { weights = w; out.textContent = "숫자를 그려 보세요"; })
  .catch(() => { out.textContent = "모델을 불러오지 못했습니다 (파일로 직접 열지 말고 웹 주소로 열어 주세요)"; });
