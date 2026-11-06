"""과제 갤러리용 커버 이미지 생성기.

covers.json의 각 항목으로 1500x600 PNG를 만듭니다.
  python3 covers/make_covers.py
"""
import json, math, random, pathlib
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
# 재원별 색 (배경, 강조)
PALETTE = {
    "IITP 주관": ("#1f2a44", "#8fb3ff"),
    "IITP 참여": ("#2b2a3d", "#c9b8ff"),
    "삼성전자":  ("#10304f", "#7cc4ff"),
    "LG전자":    ("#3a1d2a", "#ff9bb8"),
    "산학":      ("#1f3a33", "#86e0b8"),
    "기타":      ("#2a2a2a", "#d6d6d6"),
}

def lattice(seed, accent):
    """격자(lattice) 점과 몇 개의 기저 벡터 — 암호 연구실다운 은은한 패턴."""
    rnd = random.Random(seed)
    a = (rnd.uniform(70, 95), rnd.uniform(-18, 18))
    b = (rnd.uniform(-30, 30), rnd.uniform(70, 95))
    pts, out = [], []
    for i in range(-12, 26):
        for j in range(-8, 14):
            x, y = 900 + i * a[0] + j * b[0], -60 + i * a[1] + j * b[1]
            if 600 < x < 1560 and -40 < y < 640:
                pts.append((x, y))
                d = math.hypot(x - 1180, y - 300)
                op = max(0.05, 0.42 - d / 1500)
                out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="{accent}" opacity="{op:.2f}"/>')
    ox, oy = 1180, 300
    for v, w in ((a, 1.0), (b, 1.0)):
        out.append(f'<line x1="{ox}" y1="{oy}" x2="{ox+v[0]*2.2:.1f}" y2="{oy+v[1]*2.2:.1f}" stroke="{accent}" stroke-width="2.4" opacity=".55" stroke-linecap="round"/>')
    out.append(f'<circle cx="{ox}" cy="{oy}" r="5" fill="{accent}" opacity=".8"/>')
    return "".join(out)

def html(item):
    bg, ac = PALETTE.get(item.get("fund"), PALETTE["기타"])
    tag = item.get("tag", item.get("fund", ""))
    return f"""<!doctype html><meta charset="utf-8"><style>
body{{margin:0}} .c{{width:1500px;height:600px;position:relative;overflow:hidden;
background:radial-gradient(120% 140% at 85% 50%, {bg}cc 0%, {bg} 55%);background-color:{bg};
font-family:'Noto Sans CJK KR','Noto Sans KR',sans-serif;color:#fff}}
svg{{position:absolute;inset:0}}
.t{{position:absolute;left:300px;top:220px;}}
.tag{{font-size:26px;letter-spacing:.08em;color:{ac};font-weight:500;opacity:.95}}
.name{{font-size:84px;font-weight:700;letter-spacing:-.02em;margin-top:10px;line-height:1.05}}
.sub{{font-size:26px;opacity:.6;margin-top:14px;font-weight:400}}
</style><div class="c"><svg width="1500" height="600">{lattice(item['slug'], ac)}</svg>
<div class="t"><div class="tag">{tag}</div><div class="name">{item['short']}</div>
<div class="sub">{item.get('years','')}</div></div></div>"""

def main():
    items = json.loads((HERE / "covers.json").read_text())
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = b.new_page(viewport={"width": 1500, "height": 600})
        for it in items:
            pg.set_content(html(it)); pg.wait_for_timeout(150)
            pg.screenshot(path=str(HERE / f"{it['slug']}.png"))
            print("ok", it["slug"])
        b.close()

if __name__ == "__main__":
    main()
