"""Prepara a foto para virar ASCII.

1. Remove o fundo (rembg), se estiver instalado.
2. Aumenta o contraste local com CLAHE (OpenCV), pra dar luz e sombra ao rosto.
3. Compoe sobre branco puro, pra o fundo virar espaco vazio no ASCII.

Uso: python scripts/prep_photo.py minha-foto.jpg
Saida: source-prepped.png (escala de cinza)
"""
import sys

import cv2
import numpy as np
from PIL import Image


def main(path: str, out: str = "source-prepped.png") -> None:
    img = Image.open(path).convert("RGBA")

    try:
        from rembg import remove

        img = remove(img)
        print("fundo removido com rembg")
    except Exception as exc:  # rembg ausente ou sem modelo
        print(f"rembg indisponivel ({exc}); seguindo sem remover o fundo")

    white = Image.new("RGBA", img.size, (255, 255, 255, 255))
    white.alpha_composite(img)
    gray = np.array(white.convert("L"))

    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    gray = clahe.apply(gray)

    # mantem o fundo branco depois do CLAHE
    alpha = np.array(img.split()[-1])
    gray[alpha < 20] = 255

    Image.fromarray(gray).save(out)
    print(f"ok: {out}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("uso: python scripts/prep_photo.py <foto>")
    main(sys.argv[1])
