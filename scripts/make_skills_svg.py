"""Painel de habilidades: um sistema solar animado + um terminal que escaneia os modulos.

Uso: python scripts/make_skills_svg.py
Saida: skills.svg
Edite RINGS (o que orbita) e MODULES (o que o terminal lista).
"""
import html

W, H = 860, 480
BG, BORDER, TXT, DIM = "#0d1117", "#30363d", "#c9d1d9", "#8b949e"
PINK, BLUE, GREEN, AMBER = "#f778ba", "#58a6ff", "#39d353", "#e3b341"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

CX, CY = 236, 248
# (nome, raio, cor, segundos por volta, sentido, itens)
RINGS = [
    ("design", 74, PINK, 28, 1, ["Figma", "Affinity", "Foto", "Vídeo"]),
    ("web", 130, BLUE, 42, -1, ["HTML", "CSS", "JavaScript", "React", "Next.js", "SEO"]),
    ("infra", 178, GREEN, 60, 1, ["Vercel", "Cloudflare", "Supabase", "Hostinger", "WordPress", "GitHub", "Claude"]),
]

MODULES = [
    ("design", PINK, "Figma · Affinity · Branding"),
    ("front-end", BLUE, "HTML · CSS · JS · React · Next.js"),
    ("back-end", BLUE, "Supabase · APIs · Auth"),
    ("cms", BLUE, "WordPress · JetEngine"),
    ("deploy", GREEN, "Vercel · Cloudflare · Hostinger"),
    ("growth", AMBER, "SEO · AEO · GEO · LPs de Ads"),
    ("conteúdo", PINK, "Foto · Vídeo · Criativos"),
    ("ia", AMBER, "Claude · agentes · skills"),
]


def circle_path(r: float, direction: int) -> str:
    sweep = 1 if direction > 0 else 0
    return (
        f"M {CX + r:.1f} {CY} "
        f"A {r} {r} 0 1 {sweep} {CX - r:.1f} {CY} "
        f"A {r} {r} 0 1 {sweep} {CX + r:.1f} {CY} Z"
    )


def orbit() -> list[str]:
    p = [
        "<defs>"
        f'<radialGradient id="core" cx="50%" cy="45%" r="60%"><stop offset="0" stop-color="#69f0a0"/>'
        f'<stop offset="0.55" stop-color="{GREEN}"/><stop offset="1" stop-color="#0e4429"/></radialGradient>'
        f'<radialGradient id="glow"><stop offset="0" stop-color="{GREEN}" stop-opacity=".35"/>'
        f'<stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></radialGradient>'
        "</defs>"
    ]
    # aneis
    for i, (_, r, color, *_rest) in enumerate(RINGS):
        p.append(
            f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="none" stroke="{color}" stroke-opacity=".28" '
            f'stroke-dasharray="2 6" opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" begin="{0.2 + i*0.25:.2f}s" dur=".6s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="rotate" from="0 {CX} {CY}" to="{360 if i % 2 == 0 else -360} {CX} {CY}" '
            f'dur="{90 + i*30}s" repeatCount="indefinite"/></circle>'
        )
    # nucleo pulsando
    p.append(
        f'<circle cx="{CX}" cy="{CY}" r="56" fill="url(#glow)">'
        f'<animate attributeName="r" values="48;62;48" dur="3.2s" repeatCount="indefinite"/></circle>'
        f'<circle cx="{CX}" cy="{CY}" r="34" fill="url(#core)"/>'
        f'<text x="{CX}" y="{CY + 5}" text-anchor="middle" font-family="{MONO}" font-size="14" '
        f'font-weight="700" fill="{BG}" letter-spacing="1">MALTA</text>'
    )
    # itens orbitando (animateMotion mantem o texto sempre de pe)
    for i, (_, r, color, dur, direction, items) in enumerate(RINGS):
        path = circle_path(r, direction)
        n = len(items)
        for j, item in enumerate(items):
            label = html.escape(item)
            pw = len(item) * 7.4 + 20
            offset = -dur * j / n - dur * i * 0.17
            p.append(
                f'<g opacity="0">'
                f'<animate attributeName="opacity" from="0" to="1" begin="{0.6 + i*0.35 + j*0.08:.2f}s" dur=".5s" fill="freeze"/>'
                f'<rect x="{-pw/2:.1f}" y="-11" width="{pw:.1f}" height="22" rx="11" fill="{BG}" stroke="{color}" stroke-opacity=".9"/>'
                f'<circle cx="{-pw/2 + 10:.1f}" cy="0" r="2.6" fill="{color}"/>'
                f'<text x="{5:.1f}" y="4" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="{TXT}">{label}</text>'
                f'<animateMotion dur="{dur}s" begin="{offset:.2f}s" repeatCount="indefinite" path="{path}"/>'
                "</g>"
            )
    # legenda
    lx = 30
    for name, _, color, *_ in RINGS:
        p.append(
            f'<circle cx="{lx}" cy="{H - 22}" r="4" fill="{color}"/>'
            f'<text x="{lx + 9}" y="{H - 18}" font-family="{MONO}" font-size="11" fill="{DIM}">{name}</text>'
        )
        lx += 30 + len(name) * 7.5
    return p


def terminal() -> list[str]:
    x0, y0 = 488, 70
    p = [
        f'<line x1="470" y1="44" x2="470" y2="{H - 24}" stroke="{BORDER}"/>',
    ]
    cmd = "$ ./habilidades.sh --scan"
    # comando digitado (revelado por clip)
    p.append(
        f'<clipPath id="cmd"><rect x="{x0}" y="{y0 - 14}" width="0" height="20">'
        f'<animate attributeName="width" from="0" to="{len(cmd) * 7.8 + 4:.0f}" begin=".3s" dur="1s" fill="freeze"/></rect></clipPath>'
        f'<text x="{x0}" y="{y0}" font-family="{MONO}" font-size="13" fill="{TXT}" clip-path="url(#cmd)">'
        f'<tspan fill="{GREEN}">$</tspan> ./habilidades.sh <tspan fill="{DIM}">--scan</tspan></text>'
    )
    y = y0 + 34
    t = 1.5
    for name, color, items in MODULES:
        p.append(
            f'<g opacity="0" font-family="{MONO}" font-size="12.5">'
            f'<animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur=".25s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="-6 0" to="0 0" begin="{t:.2f}s" dur=".25s" fill="freeze"/>'
            f'<text x="{x0}" y="{y}" fill="{GREEN}">✓</text>'
            f'<text x="{x0 + 18}" y="{y}" fill="{color}" font-weight="700">{html.escape(name)}</text>'
            f'<text x="{x0 + 104}" y="{y}" fill="{TXT}">{html.escape(items)}</text>'
            "</g>"
        )
        y += 27
        t += 0.32
    # barra de progresso
    y += 8
    bw = 250
    p.append(
        f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="1.4s" dur=".3s" fill="freeze"/>'
        f'<rect x="{x0}" y="{y - 10}" width="{bw}" height="10" rx="5" fill="#161b22" stroke="{BORDER}"/>'
        f'<rect x="{x0}" y="{y - 10}" width="0" height="10" rx="5" fill="{GREEN}">'
        f'<animate attributeName="width" from="0" to="{bw}" begin="1.5s" dur="{len(MODULES) * 0.32:.2f}s" fill="freeze"/></rect>'
        f'<text x="{x0 + bw + 12}" y="{y}" font-family="{MONO}" font-size="12" fill="{DIM}">{len(MODULES)}/{len(MODULES)} módulos</text></g>'
    )
    y += 32
    t += 0.2
    msg = "pronto pro próximo projeto"
    p.append(
        f'<g opacity="0" font-family="{MONO}" font-size="13">'
        f'<animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur=".3s" fill="freeze"/>'
        f'<text x="{x0}" y="{y}" fill="{TXT}"><tspan fill="{AMBER}">→</tspan> {msg}</text>'
        f'<rect x="{x0 + (len(msg) + 2) * 7.8 + 2:.1f}" y="{y - 12}" width="8" height="15" fill="{GREEN}">'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1s" repeatCount="indefinite"/></rect>'
        "</g>"
    )
    return p


def main() -> None:
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="{BG}" stroke="{BORDER}"/>',
        '<circle cx="18" cy="16" r="4.5" fill="#ff5f57"/><circle cx="32" cy="16" r="4.5" fill="#febc2e"/><circle cx="46" cy="16" r="4.5" fill="#28c840"/>',
        f'<text x="{W/2}" y="20" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{DIM}">skills.sys</text>',
    ]
    p += orbit()
    p += terminal()
    p.append("</svg>")
    with open("skills.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(p))
    print("ok: skills.svg")


if __name__ == "__main__":
    main()
