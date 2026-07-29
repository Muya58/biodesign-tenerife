"""Extraer el fondo del hero (destellos + banda dorada) de la portada del catálogo.

La página 1 del PDF es el pliego completo de cubierta, así que la imagen contiene la
misma composición dos veces apiladas. Nos quedamos con la inferior, que llega hasta la
banda de purpurina dorada del borde.

Medido por filas sobre el original de 1657x2343:
  - y ~1080  costura oscura entre las dos mitades del pliego
  - y ~1100-2190  campo de bokeh azul/turquesa
  - y ~2190-2343  banda dorada (calidez R-B pasa de -60 a +39)

Uso:  python scripts/extract-hero-bg.py
Salida: assets/img/hero-bg.jpg
"""

from PIL import Image
from pathlib import Path

SRC = Path('assets/img/catalogo-raw/p01_0_1657x2343.png')
OUT = Path('assets/img/hero-bg.jpg')

CROP_TOP = 1100      # justo debajo de la costura del pliego
TARGET_WIDTH = 1600  # el bokeh es suave, así que no necesita más resolución


def main():
    im = Image.open(SRC).convert('RGB')
    w, h = im.size

    crop = im.crop((0, CROP_TOP, w, h))
    scale = TARGET_WIDTH / crop.width
    crop = crop.resize(
        (TARGET_WIDTH, int(round(crop.height * scale))), Image.LANCZOS
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    crop.save(OUT, 'JPEG', quality=78, optimize=True, progressive=True)

    kb = OUT.stat().st_size // 1024
    print(f'{OUT}: {crop.width}x{crop.height} ratio {crop.width/crop.height:.3f} — {kb} KB')


if __name__ == '__main__':
    main()
