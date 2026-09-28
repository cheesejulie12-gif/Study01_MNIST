"""데스크톱 손글씨 인식 앱 (Tkinter). 웹 버전과 같은 weights.json, 같은 전처리를 쓴다. 실행: python3 app.py"""
import json, os, tkinter as tk
import numpy as np
from PIL import Image, ImageDraw
from preprocess import preprocess

w = json.load(open(os.path.join(os.path.dirname(__file__), "..", "web_version", "weights.json")))
W = [np.array(m) for m in w["W"]]; B = [np.array(b) for b in w["b"]]

def predict(x):
    for l in range(len(W)):
        x = x @ W[l] + B[l]
        if l < len(W) - 1: x = np.maximum(x, 0)
    e = np.exp(x - x.max()); return e / e.sum()

root = tk.Tk(); root.title("손글씨 숫자 인식")
cv = tk.Canvas(root, width=280, height=280, bg="white"); cv.pack()
img = Image.new("L", (280, 280), 0); dr = ImageDraw.Draw(img); label = tk.Label(root, text="숫자를 그려 보세요", font=("", 20)); label.pack()
last = [None]
def move(e):
    if last[0]:
        cv.create_line(*last[0], e.x, e.y, width=20, capstyle="round", fill="black"); dr.line([*last[0], e.x, e.y], fill=255, width=20)
        x = preprocess(np.asarray(img, dtype=float) / 255)
        if x is not None: p = predict(x); label.config(text=f"인식 결과: {p.argmax()} ({p.max()*100:.0f}%)")
    last[0] = (e.x, e.y)
def clear():
    cv.delete("all"); dr.rectangle([0, 0, 280, 280], fill=0); label.config(text="숫자를 그려 보세요")
cv.bind("<B1-Motion>", move); cv.bind("<ButtonRelease-1>", lambda e: last.__setitem__(0, None))
tk.Button(root, text="지우기", command=clear).pack(); root.mainloop()
