"""Converte uma imagem em ASCII monocromatico que se "digita" sozinho (SVG animado).

Uso:
  python scripts/make_ascii_svg.py                      # usa source-prepped.png
  python scripts/make_ascii_svg.py --image outra.png
  python scripts/make_ascii_svg.py --text MALTA         # placeholder sem foto
Saida: malta-ascii.svg
"""
import argparse
import html

import numpy as np
from PIL import Image, ImageDraw, ImageFont

RAMP = " .`:-=+*cs#%@"  # vazio -> denso (denso = claro na tela escura)

CHAR_W, LINE_H = 6.0, 10.0  # grade do SVG
PAD = 18
BG, BORDER, FG, CURSOR = "#0d1117", "#30363d", "#c9d1d9", "#39d353"
ROW_DUR, ROW_STEP, START = 0.28, 0.045, 0.3


def text_image(text: str) -> Image.Image:
    """Desenha um texto grande em branco no preto, para virar ASCII."""
    font = None
    for name in ("DejaVuSans-Bold.ttf", "Poppins-Bold.ttf", "Arial Bold.ttf", "arialbd.ttf"):
        try:
            font = ImageFont.truetype(name, 220)
            break
        except OSError:
            continue
    font = font or ImageFont.load_default()
    text = text.replace(" ", "\n")  # "MAL TA" vira duas linhas
    probe = ImageDraw.Draw(Image.new("L", (10, 10)))
    x0, y0, x1, y1 = probe.multiline_textbbox((0, 0), text, font=font, align="center", spacing=40)
    x0, y0, x1, y1 = (int(v) for v in (x0, y0, x1, y1))
    img = Image.new("L", (x1 - x0 + 60, int((y1 - y0) * 1.9) + 60), 0)
    ImageDraw.Draw(img).multiline_text(
        (30 - x0, (img.height - (y1 - y0)) // 2 - y0), text, fill=255, font=font, align="center", spacing=40
    )
    return img


def to_rows(img: Image.Image, cols: int) -> list[str]:
    img = img.convert("L")
    rows = max(1, round(cols * img.height / img.width * (CHAR_W / LINE_H)))
    small = np.asarray(img.resize((cols, rows), Image.LANCZOS), dtype=float) / 255.0
    idx = (small ** 0.8 * (len(RAMP) - 1)).round().astype(int)  # claro -> denso
    lines = ["".join(RAMP[i] for i in row).rstrip() for row in idx]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def match_height(lines: list[str], cols: int, card: str = "info-card.svg", shown: tuple = (370, 490)) -> list[str]:
    """Completa com linhas vazias pra o painel ficar da mesma altura do card ao lado."""
    try:
        import re
        vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', open(card, encoding="utf-8").read())
        card_h = float(vb.group(2)) * shown[1] / float(vb.group(1))
    except (OSError, AttributeError):
        return lines
    w = cols * CHAR_W + PAD * 2
    target_h = card_h * w / shown[0]
    total = int((target_h - PAD * 2 - 24) // LINE_H)
    extra = max(0, total - len(lines))
    return [""] * (extra // 2) + lines + [""] * (extra - extra // 2)


def dots(k: float) -> str:
    """Bolinhas da janela no mesmo tamanho visual do card ao lado."""
    return "".join(
        f'<circle cx="{(18 + i*14) * k:.1f}" cy="{16 * k:.1f}" r="{4.5 * k:.1f}" fill="{c}"/>'
        for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840"))
    )


def build_svg(lines: list[str], cols: int) -> str:
    w = cols * CHAR_W + PAD * 2
    h = len(lines) * LINE_H + PAD * 2 + 24
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}">',
        f'<rect x="0.5" y="0.5" width="{w-1:.0f}" height="{h-1:.0f}" rx="10" fill="{BG}" stroke="{BORDER}"/>',
        dots(w / 370),
        "<defs>",
    ]
    top = PAD + 24
    for i, line in enumerate(lines):
        y = top + i * LINE_H - LINE_H + 2
        begin = START + i * ROW_STEP
        width = len(line) * CHAR_W + 2
        parts.append(
            f'<clipPath id="r{i}"><rect x="{PAD}" y="{y:.1f}" width="0" height="{LINE_H}">'
            f'<animate attributeName="width" from="0" to="{width:.1f}" begin="{begin:.3f}s" dur="{ROW_DUR}s" fill="freeze"/>'
            "</rect></clipPath>"
        )
    parts.append("</defs>")
    parts.append(
        f'<g font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="9.6" fill="{FG}" xml:space="preserve">'
    )
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        y = top + i * LINE_H
        begin = START + i * ROW_STEP
        width = len(line) * CHAR_W
        parts.append(
            f'<text x="{PAD}" y="{y:.1f}" textLength="{width:.1f}" lengthAdjust="spacingAndGlyphs" '
            f'clip-path="url(#r{i})">{html.escape(line)}</text>'
        )
        # cursor que acompanha a borda da linha
        parts.append(
            f'<rect x="{PAD}" y="{y-LINE_H+2:.1f}" width="5" height="{LINE_H-1}" fill="{CURSOR}" opacity="0">'
            f'<animate attributeName="x" from="{PAD}" to="{PAD+width:.1f}" begin="{begin:.3f}s" dur="{ROW_DUR}s" fill="freeze"/>'
            f'<set attributeName="opacity" to="1" begin="{begin:.3f}s"/>'
            f'<set attributeName="opacity" to="0" begin="{begin+ROW_DUR:.3f}s"/>'
            "</rect>"
        )
    parts.append("</g></svg>")
    return "\n".join(parts)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", default="source-prepped.png")
    ap.add_argument("--text", help="gera um placeholder a partir de um texto")
    ap.add_argument("--cols", type=int, default=100)
    ap.add_argument("--out", default="malta-ascii.svg")
    a = ap.parse_args()

    img = text_image(a.text) if a.text else Image.open(a.image)
    lines = match_height(to_rows(img, a.cols), a.cols)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(build_svg(lines, a.cols))
    print(f"ok: {a.out} ({len(lines)} linhas)")


if __name__ == "__main__":
    main()
