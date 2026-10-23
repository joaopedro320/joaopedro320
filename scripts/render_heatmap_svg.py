"""Desenha o heatmap de contribuicoes (53 semanas x 7 dias) com revelacao diagonal.

Uso: python scripts/render_heatmap_svg.py
Entrada: data/contributions.json  Saida: contrib-heatmap.svg
"""
import json
from datetime import date

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
BG, BORDER, TXT, DIM = "#0d1117", "#30363d", "#c9d1d9", "#8b949e"
W, LEFT, RIGHT, TOP = 860, 44, 24, 52
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]


def fmt(n: int) -> str:
    return f"{n:,}".replace(",", ".")


def main() -> None:
    data = json.load(open("data/contributions.json", encoding="utf-8"))
    days = data["days"]

    counts = sorted(x["count"] for x in days if x["count"] > 0)
    top = counts[int(len(counts) * 0.95)] if counts else 1 << 30

    first_wd = (date.fromisoformat(days[0]["date"]).weekday() + 1) % 7  # domingo = 0
    ncols = (len(days) + first_wd + 6) // 7
    step = (W - LEFT - RIGHT) / ncols
    CELL = round(step * 0.8, 2)
    h = TOP + 7 * step + 64

    css = (
        "@keyframes pop{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:none}}"
        ".c{opacity:0;animation:pop .45s ease-out forwards;transform-box:fill-box}"
        "text{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}"
    )
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h:.0f}" width="{W}" height="{h:.0f}">',
        f"<style>{css}</style>",
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{h-1:.0f}" rx="10" fill="{BG}" stroke="{BORDER}"/>',
        '<circle cx="18" cy="16" r="4.5" fill="#ff5f57"/><circle cx="32" cy="16" r="4.5" fill="#febc2e"/><circle cx="46" cy="16" r="4.5" fill="#28c840"/>',
    ]
    for i, lbl in ((1, "seg"), (3, "qua"), (5, "sex")):
        p.append(f'<text x="{LEFT-8}" y="{TOP + i*step + CELL-2:.1f}" font-size="10" fill="{DIM}" text-anchor="end">{lbl}</text>')

    last_month = None
    for i, d in enumerate(days):
        pos = i + first_wd
        col, row = divmod(pos, 7)
        x, y = LEFT + col * step, TOP + row * step
        lvl = d["level"]
        if lvl >= 4 and d["count"] >= top:
            lvl = 5
        delay = 0.25 + (col + row) * 0.022
        p.append(
            f'<rect class="c" x="{x:.1f}" y="{y:.1f}" width="{CELL}" height="{CELL}" rx="2.6" '
            f'fill="{PALETTE[lvl]}" style="animation-delay:{delay:.3f}s"><title>{d["date"]}: {d["count"]}</title></rect>'
        )
        m = int(d["date"][5:7])
        if row == 0 and m != last_month and col < ncols - 2:
            p.append(f'<text x="{x:.1f}" y="{TOP-8}" font-size="10" fill="{DIM}">{MESES[m-1]}</text>')
            last_month = m

    fy = TOP + 7 * step + 26
    best = data["best_day"]
    stats = (
        f'{fmt(data["total"])} contribuições no último ano  ·  sequência atual {data["current_streak"]}d  ·  '
        f'maior sequência {data["longest_streak"]}d  ·  melhor dia {best["count"]}'
    )
    p.append(f'<text x="{LEFT}" y="{fy:.1f}" font-size="12" fill="{TXT}">{stats}</text>')
    lx = W - 24 - 6 * 15 - 40
    p.append(f'<text x="{lx-6}" y="{fy+20:.1f}" font-size="10" fill="{DIM}" text-anchor="end">menos</text>')
    for j, c in enumerate(PALETTE):
        p.append(f'<rect x="{lx + j*15}" y="{fy+11:.1f}" width="11" height="11" rx="2.4" fill="{c}"/>')
    p.append(f'<text x="{lx + 6*15 + 4}" y="{fy+20:.1f}" font-size="10" fill="{DIM}">mais</text>')
    p.append(f'<text x="{LEFT}" y="{fy+20:.1f}" font-size="10" fill="{DIM}">atualizado em {data["updated"]}</text>')
    p.append("</svg>")

    with open("contrib-heatmap.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(p))
    print("ok: contrib-heatmap.svg")


if __name__ == "__main__":
    main()
