"""Painel "especialista em Landing Pages & Sites": titulo digitado + um mini navegador
que monta uma landing page sozinho, ate o cursor clicar no botao e chegar um lead.

Uso: python scripts/make_specialist_svg.py
Saida: specialist.svg (mesma altura do info-card.svg ao lado)
"""
import re

BG, BORDER, TXT, DIM = "#0d1117", "#30363d", "#e6edf3", "#8b949e"
GREEN, GREEN2, PANEL, LINE = "#39d353", "#26a641", "#161b22", "#21262d"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
W = 370


def card_height(card: str = "info-card.svg", shown_w: int = 490) -> float:
    try:
        vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', open(card, encoding="utf-8").read())
        return float(vb.group(2)) * shown_w / float(vb.group(1))
    except (OSError, AttributeError):
        return 380.0


def appear(t: float, dy: float = 6, dur: float = 0.4) -> str:
    return (
        f'<animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur="{dur}s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" from="0 {dy}" to="0 0" '
        f'begin="{t:.2f}s" dur="{dur}s" fill="freeze"/>'
    )


def typed(x: float, y: float, w: float, h: float, t: float, dur: float, inner: str, cid: str) -> str:
    return (
        f'<clipPath id="{cid}"><rect x="{x}" y="{y - h}" width="0" height="{h + 8}">'
        f'<animate attributeName="width" from="0" to="{w}" begin="{t:.2f}s" dur="{dur}s" fill="freeze"/></rect></clipPath>'
        f'<g clip-path="url(#{cid})">{inner}</g>'
    )


def main() -> None:
    H = round(card_height())
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
        "<defs>"
        '<linearGradient id="stone" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#2d333b"/><stop offset=".5" stop-color="#444c56"/><stop offset="1" stop-color="#22272e"/>'
        "</linearGradient>"
        f'<linearGradient id="title" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{GREEN}"/>'
        '<stop offset="1" stop-color="#69f0a0"/></linearGradient>'
        "</defs>",
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="{BG}" stroke="{BORDER}"/>',
        '<circle cx="18" cy="16" r="4.5" fill="#ff5f57"/><circle cx="32" cy="16" r="4.5" fill="#febc2e"/><circle cx="46" cy="16" r="4.5" fill="#28c840"/>',
        f'<text x="352" y="20" text-anchor="end" font-family="{MONO}" font-size="10" fill="{DIM}">especialidade.html</text>',
    ]

    # titulo
    p.append(typed(22, 58, 200, 14, 0.2, 0.6,
                   f'<text x="22" y="58" font-family="{MONO}" font-size="12" fill="{DIM}">// especialista em</text>', "t1"))
    p.append(typed(22, 92, 330, 30, 0.8, 0.7,
                   f'<text x="22" y="92" font-family="{SANS}" font-size="30" font-weight="800" fill="url(#title)" '
                   f'letter-spacing="-.5">Landing Pages</text>', "t2"))
    p.append(typed(22, 126, 330, 30, 1.4, 0.5,
                   f'<text x="22" y="126" font-family="{SANS}" font-size="30" font-weight="800" fill="{TXT}" '
                   f'letter-spacing="-.5">&amp; Sites</text>', "t3"))
    p.append(
        f'<g opacity="0">{appear(1.9, 4)}<text x="24" y="148" font-family="{MONO}" font-size="10.5" fill="{DIM}">'
        "alta conversão · alto padrão · SEO</text></g>"
    )

    # navegador
    bx, by, bw = 18, 164, W - 36
    bh = H - by - 18
    p.append(
        f'<g opacity="0">{appear(2.1, 8)}'
        f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="8" fill="{PANEL}" stroke="{BORDER}"/>'
        f'<line x1="{bx}" y1="{by+22}" x2="{bx+bw}" y2="{by+22}" stroke="{BORDER}"/>'
        f'<circle cx="{bx+11}" cy="{by+11}" r="2.6" fill="#484f58"/><circle cx="{bx+19}" cy="{by+11}" r="2.6" fill="#484f58"/>'
        f'<circle cx="{bx+27}" cy="{by+11}" r="2.6" fill="#484f58"/>'
        f'<rect x="{bx+80}" y="{by+5}" width="{bw-160}" height="12" rx="6" fill="{BG}"/>'
        f'<text x="{bx+bw/2}" y="{by+14}" text-anchor="middle" font-family="{MONO}" font-size="8" fill="{DIM}">seucliente.com.br</text>'
        "</g>"
    )
    ix, iy = bx + 12, by + 32
    t = 2.6
    # menu
    p.append(
        f'<g opacity="0">{appear(t)}'
        f'<rect x="{ix}" y="{iy}" width="34" height="8" rx="2" fill="{TXT}" opacity=".85"/>'
        + "".join(f'<rect x="{bx+bw-110+i*28}" y="{iy+2}" width="20" height="4" rx="2" fill="#484f58"/>' for i in range(3))
        + f'<rect x="{bx+bw-26}" y="{iy}" width="14" height="8" rx="4" fill="{GREEN2}"/></g>'
    )
    t += 0.35
    # hero: texto
    hy = iy + 26
    p.append(
        f'<g opacity="0">{appear(t)}'
        f'<rect x="{ix}" y="{hy}" width="140" height="11" rx="3" fill="{TXT}"/>'
        f'<rect x="{ix}" y="{hy+16}" width="110" height="11" rx="3" fill="{TXT}"/>'
        f'<rect x="{ix}" y="{hy+36}" width="130" height="4" rx="2" fill="#484f58"/>'
        f'<rect x="{ix}" y="{hy+44}" width="100" height="4" rx="2" fill="#484f58"/></g>'
    )
    t += 0.35
    # hero: imagem de pedra
    imx, imw = bx + bw - 132, 120
    p.append(
        f'<g opacity="0">{appear(t)}'
        f'<rect x="{imx}" y="{hy-2}" width="{imw}" height="74" rx="6" fill="url(#stone)"/>'
        f'<path d="M{imx+10} {hy+60} C {imx+40} {hy+20}, {imx+70} {hy+70}, {imx+112} {hy+10}" '
        'stroke="#768390" stroke-width="1.2" fill="none" opacity=".7"/>'
        f'<path d="M{imx+4} {hy+30} C {imx+30} {hy+50}, {imx+60} {hy+6}, {imx+116} {hy+44}" '
        'stroke="#adbac7" stroke-width=".7" fill="none" opacity=".5"/></g>'
    )
    t += 0.35
    # botao CTA
    cx_, cy_, cw, ch = ix, hy + 56, 96, 18
    p.append(
        f'<g opacity="0">{appear(t)}'
        f'<rect x="{cx_}" y="{cy_}" width="{cw}" height="{ch}" rx="9" fill="{GREEN}">'
        f'<animate attributeName="fill" values="{GREEN};#69f0a0;{GREEN}" dur="2s" begin="{t+2.4:.2f}s" repeatCount="indefinite"/></rect>'
        f'<text x="{cx_+cw/2}" y="{cy_+12.5}" text-anchor="middle" font-family="{SANS}" font-size="8.5" '
        f'font-weight="700" fill="{BG}">Pedir orçamento</text></g>'
    )
    t += 0.35
    # cards
    ky = cy_ + 32
    kw = (bw - 24 - 16) / 3
    kh = max(20, by + bh - ky - 10)
    for i in range(3):
        kx = ix + i * (kw + 8)
        p.append(
            f'<g opacity="0">{appear(t + i * 0.12)}'
            f'<rect x="{kx:.1f}" y="{ky}" width="{kw:.1f}" height="{kh}" rx="5" fill="{BG}" stroke="{LINE}"/>'
            f'<rect x="{kx+8:.1f}" y="{ky+8}" width="{kw*0.45:.1f}" height="5" rx="2" fill="{TXT}" opacity=".7"/>'
            f'<rect x="{kx+8:.1f}" y="{ky+18}" width="{kw-16:.1f}" height="3" rx="1.5" fill="#484f58"/></g>'
        )
    t += 0.6
    # cursor vai ate o botao e clica
    tx, ty = cx_ + cw * 0.62, cy_ + ch * 0.6
    sx, sy = bx + bw - 30, by + bh - 12
    p.append(
        f'<g opacity="0" transform="translate({sx} {sy})">'
        f'<animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur=".2s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" from="{sx} {sy}" to="{tx:.1f} {ty:.1f}" '
        f'begin="{t:.2f}s" dur=".9s" fill="freeze" calcMode="spline" keySplines=".4 0 .2 1" keyTimes="0;1"/>'
        f'<path d="M0 0 L0 13 L3.5 10 L6 15.5 L8 14.6 L5.6 9.2 L10 9.2 Z" fill="{TXT}" stroke="{BG}" stroke-width="1"/></g>'
    )
    t += 1.0
    # onda do clique
    p.append(
        f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="0" fill="none" stroke="{GREEN}" stroke-width="1.5" opacity="0">'
        f'<animate attributeName="r" from="2" to="16" begin="{t:.2f}s" dur=".5s" fill="freeze"/>'
        f'<animate attributeName="opacity" values="0;1;0" begin="{t:.2f}s" dur=".5s" fill="freeze"/></circle>'
    )
    t += 0.3
    # notificacao de lead
    nx, nw = bx + bw - 108, 96
    ny = by + bh - 36
    p.append(
        f'<g opacity="0">{appear(t, -6, .35)}'
        f'<rect x="{nx}" y="{ny}" width="{nw}" height="24" rx="6" fill="{BG}" stroke="{GREEN}"/>'
        f'<circle cx="{nx+12}" cy="{ny+12}" r="4" fill="{GREEN}"/>'
        f'<text x="{nx+22}" y="{ny+15.5}" font-family="{MONO}" font-size="9.5" fill="{TXT}">+1 lead novo</text></g>'
    )
    p.append("</svg>")
    with open("specialist.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(p))
    print("ok: specialist.svg")


if __name__ == "__main__":
    main()
