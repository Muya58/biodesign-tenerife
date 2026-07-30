"""Componer una vista fija de una página interior: cabecera a sangre + bloques foto/texto.

Replica el CSS real (.page-hero y .feature-split) para poder revisar el resultado sin
depender de capturas de pantalla del navegador.

Uso:  python scripts/preview-page.py quienes-somos [ancho]
Salida: preview-<pagina>.png (temporal, no se versiona)
"""

import sys
import textwrap
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

CONTAINER_MAX = 1180
CONTAINER_PAD = 24
SAND = (232, 199, 126)
NAVY = (6, 14, 26)
CARD_BG = (13, 26, 45)

CONTENIDO = {
    'quienes-somos': {
        'eyebrow': 'NUESTRA CONCESIÓN',
        'h1': 'Concesionario Oficial\nBio.design en Tenerife',
        'sub': 'Diseñamos, instalamos y mantenemos piscinas de arena Bio.design con el '
               'respaldo técnico directo del fabricante italiano.',
        'badge': 'EXCLUSIVO PARA LA PROVINCIA DE SANTA CRUZ DE TENERIFE',
        'splits': [
            ('assets/img/realizaciones/piscina-privada-03.jpg', False,
             'Autorizados por el fabricante',
             'Apavi Green es el concesionario oficial de Bio.design S.p.A. para la '
             'provincia de Santa Cruz de Tenerife, con la garantía y el respaldo '
             'técnico directo del fabricante italiano.'),
            ('assets/img/realizaciones/piscina-publica-01.jpg', True,
             'Bio.design: 40 años dando forma al agua',
             'Nace en Milán en 1980 y es hoy líder en fuentes monumentales, lagos '
             'artificiales y piscinas de arena, con I+D propio y una red '
             'internacional de concesionarios.'),
        ],
    },
    'tecnologia': {
        'eyebrow': 'LA TECNOLOGÍA', 'h1': 'La Tecnología Bio.design',
        'sub': 'Descubre qué hace única a una piscina de arena Bio.design frente a una '
               'piscina tradicional de hormigón armado.',
        'badge': None, 'splits': [],
    },
    'realizaciones': {
        'eyebrow': 'REALIZACIONES', 'h1': 'Realizaciones Bio.design',
        'sub': 'Calidad, naturalidad y belleza, integrando productos naturales con las '
               'mejores tecnologías.',
        'badge': None, 'splits': [],
    },
    'contacto': {
        'eyebrow': 'HABLEMOS', 'h1': 'Contacta con nosotros',
        'sub': '¿Tienes un proyecto en mente? Te respondemos en menos de 24 horas.',
        'badge': None, 'splits': [],
    },
}


def font(size, bold=False):
    for name in (('arialbd.ttf', 'ariblk.ttf') if bold else ('arial.ttf',)):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def cover(img, w, h):
    scale = max(w / img.width, h / img.height)
    img = img.resize((max(1, int(img.width * scale)), max(1, int(img.height * scale))), Image.LANCZOS)
    left = (img.width - w) // 2
    top = (img.height - h) // 2
    return img.crop((left, top, left + w, top + h))


def draw_hero(canvas, y, vw, page, data):
    """Replica .page-hero: foto cover + degradado inferior + antetítulo, h1 y subtítulo."""
    hh = int(min(max(280, vw * 0.38), 440))
    photo = cover(Image.open(f'assets/img/heros/{page}.jpg').convert('RGB'), vw, hh)

    # Degradado de legibilidad (linear-gradient to top)
    arr = np.asarray(photo).astype(np.float32) / 255.0
    ys = np.linspace(0, 1, hh)  # 0 = arriba
    alpha = np.interp(1 - ys, [0, .38, .70, 1.0], [.92, .62, .20, .35])[:, None, None]
    arr = arr * (1 - alpha) + (np.array(NAVY, dtype=np.float32) / 255.0) * alpha
    photo = Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8))
    canvas.paste(photo, (0, y))

    d = ImageDraw.Draw(canvas)
    cw = min(CONTAINER_MAX, vw) - CONTAINER_PAD * 2
    x = (vw - cw) // 2
    bottom = y + hh - 44

    lines = data['sub'] and textwrap.wrap(data['sub'], width=max(30, int(cw / 9.2)))[:3]
    f_sub = font(17)
    sub_h = len(lines) * 26
    f_h1 = font(int(min(max(30, vw * 0.038), 52)), bold=True)
    h1_lines = data['h1'].split('\n')
    h1_h = len(h1_lines) * int(f_h1.size * 1.22)

    cursor = bottom - sub_h - h1_h - 34
    d.text((x, cursor), data['eyebrow'], font=font(12, bold=True), fill=SAND)
    cursor += 30
    for ln in h1_lines:
        d.text((x, cursor), ln, font=f_h1, fill=(255, 255, 255))
        cursor += int(f_h1.size * 1.22)
    cursor += 8
    for ln in lines:
        d.text((x, cursor), ln, font=f_sub, fill=(214, 220, 228))
        cursor += 26
    return y + hh


def draw_badge(canvas, y, vw, text):
    d = ImageDraw.Draw(canvas)
    cw = min(CONTAINER_MAX, vw) - CONTAINER_PAD * 2
    x = (vw - cw) // 2
    f = font(11, bold=True)
    w = int(d.textlength(text, font=f)) + 26
    d.rounded_rectangle([x, y + 40, x + w, y + 40 + 26], 13, fill=SAND)
    d.text((x + 13, y + 40 + 7), text, font=f, fill=NAVY)
    return y + 40 + 26


def draw_split(canvas, y, vw, src, reverse, title, body):
    """Replica .feature-split: foto 4/3 y tarjeta de texto solapada 56px."""
    d = ImageDraw.Draw(canvas)
    cw = min(CONTAINER_MAX, vw) - CONTAINER_PAD * 2
    x0 = (vw - cw) // 2
    big, small = int(cw * 1.05 / 2), int(cw * 0.95 / 2)
    media_w = big
    media_h = int(media_w * 3 / 4)

    if not reverse:
        media_x, body_x, body_w = x0, x0 + big - 56, small + 56
    else:
        media_x, body_x, body_w = x0 + small, x0, small + 56

    photo = cover(Image.open(src).convert('RGB'), media_w, media_h)
    canvas.paste(photo, (media_x, y))

    f_t, f_b = font(25, bold=True), font(15)
    wrapped = textwrap.wrap(body, width=max(28, int((body_w - 72) / 7.6)))
    card_h = 36 * 2 + 38 + len(wrapped) * 25
    card_y = y + (media_h - card_h) // 2
    d.rounded_rectangle([body_x, card_y, body_x + body_w, card_y + card_h], 16,
                        fill=CARD_BG, outline=(38, 52, 72))
    ty = card_y + 36
    d.text((body_x + 36, ty), title, font=f_t, fill=(255, 255, 255))
    ty += 38
    for ln in wrapped:
        d.text((body_x + 36, ty), ln, font=f_b, fill=(206, 213, 222))
        ty += 25
    return y + media_h


def main():
    page = sys.argv[1] if len(sys.argv) > 1 else 'quienes-somos'
    vw = int(sys.argv[2]) if len(sys.argv) > 2 else 1280
    data = CONTENIDO[page]

    # Alto estimado: nav + cabecera + badge + cada bloque (foto 4/3 + separación).
    media_h = int((min(CONTAINER_MAX, vw) - CONTAINER_PAD * 2) * 1.05 / 2 * 3 / 4)
    height = 84 + 440 + (66 if data['badge'] else 0) + len(data['splits']) * (media_h + 56) + 120
    canvas = Image.new('RGB', (vw, height), NAVY)

    # Barra de navegación simplificada, solo para dar contexto
    d = ImageDraw.Draw(canvas)
    d.rectangle([0, 0, vw, 84], fill=(8, 18, 32))
    d.line([(0, 84), (vw, 84)], fill=(28, 40, 58))
    wm = Image.open('assets/img/wordmark.svg') if False else None
    d.text((28, 32), 'BIO.design', font=font(19, bold=True), fill=(255, 255, 255))
    d.text((28, 55), 'by Apavi Green · Sta. Cruz de Tenerife', font=font(10), fill=(130, 140, 155))
    for i, item in enumerate(['Tecnología', 'Quiénes somos', 'Realizaciones', 'Contacto']):
        d.text((vw - 560 + i * 118, 38), item, font=font(13, bold=True), fill=(175, 183, 194))

    y = draw_hero(canvas, 84, vw, page, data)
    if data['badge']:
        y = draw_badge(canvas, y, vw, data['badge'])
    for src, reverse, title, body in data['splits']:
        y = draw_split(canvas, y + 56, vw, src, reverse, title, body)

    canvas = canvas.crop((0, 0, vw, min(height, y + 60)))
    out = Path(f'preview-{page}.png')
    canvas.save(out)
    print(f'{out}: {canvas.width}x{canvas.height}')


if __name__ == '__main__':
    main()
