"""Componer una imagen fija de cómo queda el hero, replicando lo que hace el navegador.

Sirve para revisar el efecto sin depender de capturas de pantalla: aplica el mismo
`cover` + anclaje inferior del fondo, las dos capas de cáusticas en modo `screen` con
su máscara vertical, el velo de profundidad y el logotipo.

Uso:  python scripts/preview-hero.py [ancho] [alto]
Salida: hero-piscina.png (fichero temporal, no se versiona)
"""

import io
import re
import sys
from pathlib import Path

import fitz
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Deben coincidir con .hero-water en assets/css/components.css
LAYERS = [  # (tamaño de tile, opacidad, desplazamiento inicial)
    (900, 0.13, (140, 70)),
    (620, 0.07, (-60, 210)),
]
MASK_STOPS = [(0.08, 0.0), (0.42, 0.35), (0.78, 1.0), (1.0, 1.0)]


def svg_png(path, width):
    svg = Path(path).read_text(encoding='utf-8')
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', svg).group(1).split()]
    scale = width / vb[2]
    doc = fitz.open('svg', svg.encode('utf-8'))
    pix = doc[0].get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=True)
    return Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGBA')


def vertical_mask(h, w):
    """Réplica del linear-gradient usado como mask-image."""
    ys = np.linspace(0, 1, h)
    stops = np.array([s[0] for s in MASK_STOPS])
    vals = np.array([s[1] for s in MASK_STOPS])
    return np.interp(ys, stops, vals)[:, None, None] * np.ones((1, w, 1))


def tiled(texture, size, offset, vw, vh):
    tile = texture.resize((size, size), Image.LANCZOS)
    canvas = Image.new('L', (vw, vh))
    for y in range(-size + offset[1] % size, vh + size, size):
        for x in range(-size + offset[0] % size, vw + size, size):
            canvas.paste(tile, (x, y))
    return np.asarray(canvas).astype(np.float32) / 255.0


def main():
    vw = int(sys.argv[1]) if len(sys.argv) > 1 else 1440
    vh = int(sys.argv[2]) if len(sys.argv) > 2 else 860
    hh = int(vh * 0.92)  # .hero { min-height: 92vh }

    # background-size: cover; background-position: center bottom
    bg = Image.open('assets/img/hero-bg.jpg').convert('RGB')
    scale = max(vw / bg.width, hh / bg.height)
    bg = bg.resize((int(bg.width * scale), int(bg.height * scale)), Image.LANCZOS)
    left = (bg.width - vw) // 2
    hero = bg.crop((left, bg.height - hh, left + vw, bg.height))

    # Cáusticas en modo screen, atenuadas por la máscara vertical
    base = np.asarray(hero).astype(np.float32) / 255.0
    texture = Image.open('assets/img/caustics.png').convert('L')
    mask = vertical_mask(hh, vw)
    for size, opacity, offset in LAYERS:
        layer = (tiled(texture, size, offset, vw, hh)[:, :, None] * opacity) * mask
        base = 1.0 - (1.0 - base) * (1.0 - layer)
    hero = Image.fromarray((np.clip(base, 0, 1) * 255).astype(np.uint8))

    # Velo de profundidad (.hero-sparkles). Se calcula con numpy en vez de dibujando
    # elipses/líneas una a una: así no aparecen bandas ni cortes que no existen en el
    # gradiente CSS real y que llevarían a "corregir" fallos inventados.
    yy, xx = np.mgrid[0:hh, 0:vw].astype(np.float32)
    r = np.sqrt(((xx - vw * 0.5) / (vw * 0.70)) ** 2 + ((yy - hh * 0.42) / (hh * 0.55)) ** 2)
    radial = np.clip(1.0 - r, 0.0, 1.0) ** 1.4 * 0.72
    top_fade = np.clip(1.0 - yy / (hh * 0.30), 0.0, 1.0) * 0.55
    alpha = np.clip(radial + top_fade, 0.0, 1.0)[:, :, None]

    navy = np.array([6, 14, 26], dtype=np.float32) / 255.0
    base = np.asarray(hero).astype(np.float32) / 255.0
    base = base * (1.0 - alpha) + navy * alpha
    hero = Image.fromarray((np.clip(base, 0, 1) * 255).astype(np.uint8))

    # Logotipo
    emblem = svg_png('assets/img/emblem.svg', 168)
    wordmark = svg_png('assets/img/wordmark.svg', 420)
    top = int(hh * 0.5 - 190)
    hero.paste(emblem, ((vw - emblem.width) // 2, top), emblem)
    hero.paste(wordmark, ((vw - wordmark.width) // 2, top + emblem.height + 30), wordmark)

    draw = ImageDraw.Draw(hero)
    try:
        font = ImageFont.truetype('arial.ttf', 15)
        bold = ImageFont.truetype('arialbd.ttf', 15)
    except OSError:
        font = bold = ImageFont.load_default()
    line = 'by Apavi Green  ·  Concesionario oficial, provincia de Santa Cruz de Tenerife'
    ly = top + emblem.height + 30 + wordmark.height + 22
    draw.text(((vw - draw.textlength(line, font=font)) // 2, ly), line,
              fill=(205, 212, 222), font=font)

    by = ly + 40
    draw.rounded_rectangle([vw // 2 - 300, by, vw // 2 - 20, by + 48], 8, fill=(232, 199, 126))
    draw.text((vw // 2 - 268, by + 16), 'Solicitar presupuesto gratis', fill=(10, 22, 40), font=bold)
    draw.rounded_rectangle([vw // 2 + 20, by, vw // 2 + 280, by + 48], 8,
                           fill=(38, 52, 72), outline=(120, 132, 150))
    draw.text((vw // 2 + 52, by + 16), 'Descubre la tecnología', fill=(255, 255, 255), font=bold)

    out = Path('hero-piscina.png')
    hero.save(out)
    print(f'{out}: {hero.width}x{hero.height}')


if __name__ == '__main__':
    main()
