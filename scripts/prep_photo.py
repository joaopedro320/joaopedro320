"""Prepara a foto para virar ASCII.

1. Remove o fundo (rembg) e guarda o recorte em data/portrait-cutout.png.
   Se a imagem de entrada ja tiver fundo transparente, pula essa etapa.
2. Corta no contorno da pessoa, pra ela ocupar o painel.
3. Estica o contraste so dentro da silhueta e clareia os meios-tons.
4. CLAHE (OpenCV) pra dar luz e sombra ao rosto.
5. Fundo preto puro, que vira espaco vazio no ASCII.

Uso: python scripts/prep_photo.py minha-foto.jpg
Saida: source-prepped.png (escala de cinza, fundo preto)
"""
import os
import sys

import cv2
import numpy as np
from PIL import Image

GAMMA = 0.62  # < 1 clareia os meios-tons
CUTOUT = "data/portrait-cutout.png"


def cutout(img: Image.Image) -> Image.Image:
    alpha = np.array(img.split()[-1])
    if (alpha < 250).mean() > 0.05:  # ja vem recortada
        return img
    try:
        from rembg import remove

        img = remove(img)
        os.makedirs("data", exist_ok=True)
        img.save(CUTOUT)
        print(f"fundo removido com rembg ({CUTOUT})")
    except Exception as exc:  # rembg ausente ou sem modelo
        print(f"rembg indisponivel ({exc}); seguindo sem remover o fundo")
    return img


def tone(img: Image.Image) -> np.ndarray:
    alpha = np.array(img.split()[-1]).astype(float) / 255.0
    mask = alpha > 0.5

    # corta no contorno da pessoa (com uma margem)
    ys, xs = np.where(mask)
    if len(xs):
        m = int(0.04 * max(img.size))
        x0, x1 = max(0, xs.min() - m), min(img.width, xs.max() + m)
        y0, y1 = max(0, ys.min() - m), min(img.height, ys.max() + 1)
        img = img.crop((x0, y0, x1, y1))
        alpha = alpha[y0:y1, x0:x1]
        mask = mask[y0:y1, x0:x1]

    gray = np.array(img.convert("L")).astype(float)
    if mask.any():
        lo, hi = np.percentile(gray[mask], (2, 98))
        gray = np.clip((gray - lo) / max(hi - lo, 1), 0, 1)
    else:
        gray = gray / 255.0
    gray = gray**GAMMA

    g8 = (gray * 255).astype(np.uint8)
    g8 = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(6, 6)).apply(g8)
    out = g8.astype(float) * alpha  # borda suave, fundo preto
    out[~(alpha > 0.15)] = 0
    return out.astype(np.uint8)


def main(path: str, out: str = "source-prepped.png") -> None:
    img = cutout(Image.open(path).convert("RGBA"))
    Image.fromarray(tone(img)).save(out)
    print(f"ok: {out}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("uso: python scripts/prep_photo.py <foto>")
    main(sys.argv[1])
