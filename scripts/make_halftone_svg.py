"""Retrato em halftone animado: pontos que crescem com a luz, impressos linha a linha.

Uso: python scripts/make_halftone_svg.py [--image source-prepped.png]
Saida: malta-portrait.svg (mesma altura do info-card.svg ao lado)
"""
import argparse
import re

import cv2
import numpy as np
from PIL import Image

BG, BORDER = "#0d1117", "#30363d"
INK = "#e6edf3"
ACCENT = "#39d353"
STEP = 4.6  # distancia entre os pontos
PAD, TOP = 16, 34
PANEL_W = 370


def card_height(card: str = "info-card.svg", shown_w: int = 490) -> float:
    try:
        vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', open(card, encoding="utf-8").read())
        return float(vb.group(2)) * shown_w / float(vb.group(1))
    except (OSError, AttributeError):
        return 410.0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", default="source-prepped.png")
    ap.add_argument("--out", default="malta-portrait.svg")
    a = ap.parse_args()

    W, H = PANEL_W, card_height()
    area_w, area_h = W - PAD * 2, H - TOP - PAD

    g = np.asarray(Image.open(a.image).convert("L"), dtype=np.float32) / 255.0
    # leve nitidez pra marcar oculos, olhos e maos
    blur = cv2.GaussianBlur(g, (0, 0), 1.6)
    g = np.clip(g * 1.6 - blur * 0.6, 0, 1)

    # encaixa a imagem na area (contain), alinhada embaixo
    cols = int(area_w // STEP)
    rows = int(area_h // STEP)
    scale = min(cols / g.shape[1], rows / g.shape[0])
    iw, ih = max(1, int(g.shape[1] * scale)), max(1, int(g.shape[0] * scale))
    small = cv2.resize(g, (iw, ih), interpolation=cv2.INTER_AREA)
    ox = PAD + (area_w - iw * STEP) / 2 + STEP / 2
    oy = TOP + (area_h - ih * STEP) + STEP / 2

    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H:.0f}" width="{W}" height="{H:.0f}">',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1:.0f}" rx="10" fill="{BG}" stroke="{BORDER}"/>',
        '<circle cx="18" cy="16" r="4.5" fill="#ff5f57"/><circle cx="32" cy="16" r="4.5" fill="#febc2e"/><circle cx="46" cy="16" r="4.5" fill="#28c840"/>',
        '<text x="352" y="20" text-anchor="end" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
        'font-size="10" fill="#8b949e">malta.png</text>',
        "<defs>",
    ]
    body = []
    rmax = STEP * 0.56
    for y in range(ih):
        cy = oy + y * STEP
        d = []
        for x in range(iw):
            v = float(small[y, x])
            if v < 0.06:
                continue
            r = rmax * v**0.75
            cx = ox + x * STEP
            d.append(f"M{cx - r:.1f} {cy:.1f}a{r:.2f} {r:.2f} 0 1 0 {2*r:.2f} 0a{r:.2f} {r:.2f} 0 1 0 {-2*r:.2f} 0")
        if not d:
            continue
        begin = 0.25 + y * 0.028
        p.append(
            f'<clipPath id="h{y}"><rect x="0" y="{cy - STEP/2:.1f}" width="0" height="{STEP + 0.4:.1f}">'
            f'<animate attributeName="width" from="0" to="{W}" begin="{begin:.3f}s" dur=".35s" fill="freeze"/></rect></clipPath>'
        )
        body.append(f'<path clip-path="url(#h{y})" d="{"".join(d)}"/>')
        # linha de "impressao" verde que passa por cada fileira
        body.append(
            f'<rect x="0" y="{cy - 0.6:.1f}" width="{W}" height="1.2" fill="{ACCENT}" opacity="0">'
            f'<set attributeName="opacity" to=".55" begin="{begin:.3f}s"/>'
            f'<set attributeName="opacity" to="0" begin="{begin + 0.06:.3f}s"/></rect>'
        )
    p.append("</defs>")
    p.append(f'<g fill="{INK}">')
    p += body
    p.append("</g></svg>")
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("\n".join(p))
    print(f"ok: {a.out} ({iw}x{ih} pontos)")


if __name__ == "__main__":
    main()
