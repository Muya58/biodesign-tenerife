"""Generar las cabeceras a sangre de las páginas interiores.

Bio.design abre cada sección con una banda fotográfica ancha y el titular encima.
Este script recorta las fotos elegidas del catálogo a una banda panorámica.

Uso:  python scripts/optimize-page-heros.py
Salida: assets/img/heros/*.jpg
"""

from PIL import Image
from pathlib import Path

RAW = Path('assets/img/catalogo-raw')
OUT = Path('assets/img/heros')

TARGET_WIDTH = 1600
TARGET_RATIO = 2.6   # banda panorámica; el CSS recorta más en móvil con background-size:cover

# (origen, salida, punto de interés vertical 0=arriba 1=abajo)
SELECTION = [
    ('p15_1_1357x524.png', 'quienes-somos.jpg', 0.50),  # resort con palmeras, terreno tipo Canarias
    ('p13_0_1357x696.png', 'tecnologia.jpg',    0.55),  # orilla de arena y transparencia del agua
    ('p08_0_1360x650.png', 'realizaciones.jpg', 0.45),  # atardecer con iluminación, mucho impacto
    ('p19_0_1357x650.png', 'contacto.jpg',      0.50),  # villa mediterránea, cercana
]


def crop_to_band(img, ratio, focus):
    """Recorta a la proporción pedida conservando el ancho y centrando en `focus`."""
    target_h = img.width / ratio
    if target_h <= img.height:
        top = (img.height - target_h) * focus
        return img.crop((0, int(top), img.width, int(top + target_h)))
    # La foto es más panorámica que el objetivo: recortar por los lados.
    target_w = img.height * ratio
    left = (img.width - target_w) / 2
    return img.crop((int(left), 0, int(left + target_w), img.height))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    total = 0
    for src_name, out_name, focus in SELECTION:
        src = RAW / src_name
        if not src.exists():
            raise SystemExit(f'falta la imagen de origen: {src}')
        img = Image.open(src).convert('RGB')
        img = crop_to_band(img, TARGET_RATIO, focus)
        scale = TARGET_WIDTH / img.width
        img = img.resize((TARGET_WIDTH, int(round(img.height * scale))), Image.LANCZOS)

        dest = OUT / out_name
        img.save(dest, 'JPEG', quality=78, optimize=True, progressive=True)
        kb = dest.stat().st_size // 1024
        total += kb
        print(f'{out_name:24} {img.width}x{img.height}  {kb} KB')
    print(f'\n{len(SELECTION)} cabeceras, {total} KB en total')


if __name__ == '__main__':
    main()
