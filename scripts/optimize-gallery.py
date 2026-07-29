"""Convert the selected catalogue PNGs into optimised JPGs for the gallery.

The raw PNGs in assets/img/catalogo-raw/ are a ~95MB working set extracted from
the official Bio.design catalogue PDF and are gitignored. Only the optimised
output of this script is committed and deployed.

Run from the repo root:  python scripts/optimize-gallery.py
"""

from PIL import Image
from pathlib import Path

RAW = Path('assets/img/catalogo-raw')
OUT = Path('assets/img/realizaciones')

# (source filename, output name) — categorised by inspecting each photo:
# "privada" = residential garden, "publica" = hotel, resort or spa.
SELECTION = [
    ('p04_0_1360x764.png',  'piscina-privada-01.jpg'),
    ('p29_0_1360x651.png',  'piscina-privada-02.jpg'),
    ('p14_3_1157x988.png',  'piscina-privada-03.jpg'),
    ('p17_2_1360x858.png',  'piscina-privada-04.jpg'),
    ('p06_0_1357x656.png',  'piscina-privada-05.jpg'),
    ('p27_0_1357x755.png',  'piscina-privada-06.jpg'),
    ('p11_0_1357x716.png',  'piscina-publica-01.jpg'),
    ('p12_1_1093x1263.png', 'piscina-publica-02.jpg'),
    ('p16_0_1070x1007.png', 'piscina-publica-03.jpg'),
    ('p09_0_1360x651.png',  'piscina-publica-04.jpg'),
    ('p25_0_1357x733.png',  'piscina-publica-05.jpg'),
    ('p30_1_1175x695.png',  'piscina-publica-06.jpg'),
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    total = 0
    for src_name, out_name in SELECTION:
        src = RAW / src_name
        if not src.exists():
            raise SystemExit(f'missing source image: {src}')
        img = Image.open(src).convert('RGB')
        img.thumbnail((1400, 1400), Image.LANCZOS)
        dest = OUT / out_name
        img.save(dest, 'JPEG', quality=82, optimize=True, progressive=True)
        kb = dest.stat().st_size // 1024
        total += kb
        print(f'{out_name:28} {img.width}x{img.height:<5} {kb} KB')
    print(f'\n{len(SELECTION)} images, {total} KB total')


if __name__ == '__main__':
    main()
