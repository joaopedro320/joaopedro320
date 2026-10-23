"""Card estilo neofetch com quem voce e. Edite a lista INFO e rode de novo.

Uso: python scripts/make_info_card.py        (STATIC=1 gera sem animacao)
Saida: info-card.svg
"""
import html
import os

USER = "malta@github"
INFO = [
    ("nome", "João Pedro (Malta)"),
    ("agora", "Designer Gráfico e Web Dev @ QH4 Growth"),
    ("foco", "Landing pages, sites e criativos"),
    ("antes", "dymus marketing, Tropeira Alimentos"),
    ("formação", "Design Gráfico, UNA (2026)"),
    ("stack", "HTML, CSS, JS, React, Next.js"),
    ("", "Supabase, Vercel, Cloudflare, WordPress"),
    ("design", "Figma, Affinity, foto e vídeo"),
    ("extra", "Fotografia @ Malta Business"),
    ("xp", "7 anos na área criativa"),
    ("base", "Minas Gerais, Brasil"),
]

W, PAD, LINE = 490, 22, 23
BG, BORDER = "#0d1117", "#30363d"
KEY, VAL, DIM, ACCENT = "#39d353", "#c9d1d9", "#8b949e", "#58a6ff"
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
STATIC = os.environ.get("STATIC") == "1"


def anim(i: int) -> str:
    if STATIC:
        return ""
    d = 0.6 + i * 0.12
    return (
        f'<animate attributeName="opacity" from="0" to="1" begin="{d:.2f}s" dur="0.35s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" from="-8 0" to="0 0" begin="{d:.2f}s" dur="0.35s" fill="freeze"/>'
    )


def main() -> None:
    top = PAD + 34
    rows_h = (len(INFO) + 3) * LINE
    h = top + rows_h + PAD
    op = "1" if STATIC else "0"
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}">',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{h-1}" rx="10" fill="{BG}" stroke="{BORDER}"/>',
        '<circle cx="18" cy="16" r="4.5" fill="#ff5f57"/><circle cx="32" cy="16" r="4.5" fill="#febc2e"/><circle cx="46" cy="16" r="4.5" fill="#28c840"/>',
        '<g font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="13">',
    ]
    y = top + 4
    p.append(f'<g opacity="{op}">{anim(0)}<text x="{PAD}" y="{y}" fill="{ACCENT}" font-weight="700">{USER}</text></g>')
    y += LINE * 0.75
    p.append(f'<g opacity="{op}">{anim(1)}<text x="{PAD}" y="{y}" fill="{DIM}">{"-" * len(USER)}</text></g>')
    y += LINE
    for i, (k, v) in enumerate(INFO, start=2):
        key = f"{k}:" if k else ""
        p.append(
            f'<g opacity="{op}">{anim(i)}<text x="{PAD}" y="{y}">'
            f'<tspan fill="{KEY}" font-weight="700">{html.escape(key)}</tspan>'
            f'<tspan x="{PAD + 96}" fill="{VAL}">{html.escape(v)}</tspan></text></g>'
        )
        y += LINE
    y += LINE * 0.4
    sw = "".join(
        f'<rect x="{PAD + j*30}" y="{y-12}" width="24" height="14" rx="3" fill="{c}"/>' for j, c in enumerate(PALETTE)
    )
    p.append(f'<g opacity="{op}">{anim(len(INFO) + 2)}{sw}</g>')
    p.append("</g></svg>")
    with open("info-card.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(p))
    print("ok: info-card.svg")


if __name__ == "__main__":
    main()
