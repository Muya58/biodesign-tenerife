"""Extraer el logo oficial Bio.design como SVG desde el catálogo en PDF.

La portada del catálogo trae el logotipo en vectores (no rasterizado), así que se
pueden recuperar las curvas exactas del emblema y de cada letra del wordmark en
lugar de aproximarlos con una fuente parecida.

Uso:  python scripts/extract-logo.py
Salida: assets/img/emblem.svg y assets/img/wordmark.svg
"""

import fitz
from pathlib import Path

PDF = Path(r'C:\Users\josep\Apavi Green\CATALOGO Fotografico Biodesign.pdf')
OUT = Path('assets/img')

# Índices de los trazados en la página 1 (obtenidos inspeccionando get_drawings()).
EMBLEM = [13]
WORDMARK = [24, 14, 15, 20, 21, 22, 16, 17, 18, 19, 23, 25]


def items_to_path(items):
    """Convierte los items de un drawing de PyMuPDF en datos de path SVG."""
    parts = []
    cursor = None
    for item in items:
        op = item[0]
        if op == 'l':
            p1, p2 = item[1], item[2]
            if cursor != (p1.x, p1.y):
                parts.append(f'M{p1.x:.2f},{p1.y:.2f}')
            parts.append(f'L{p2.x:.2f},{p2.y:.2f}')
            cursor = (p2.x, p2.y)
        elif op == 'c':
            p1, p2, p3, p4 = item[1], item[2], item[3], item[4]
            if cursor != (p1.x, p1.y):
                parts.append(f'M{p1.x:.2f},{p1.y:.2f}')
            parts.append(
                f'C{p2.x:.2f},{p2.y:.2f} {p3.x:.2f},{p3.y:.2f} {p4.x:.2f},{p4.y:.2f}'
            )
            cursor = (p4.x, p4.y)
        elif op == 're':
            r = item[1]
            parts.append(
                f'M{r.x0:.2f},{r.y0:.2f} H{r.x1:.2f} V{r.y1:.2f} H{r.x0:.2f} Z'
            )
            cursor = None
        elif op == 'qu':
            q = item[1]
            parts.append(
                f'M{q.ul.x:.2f},{q.ul.y:.2f} L{q.ur.x:.2f},{q.ur.y:.2f} '
                f'L{q.lr.x:.2f},{q.lr.y:.2f} L{q.ll.x:.2f},{q.ll.y:.2f} Z'
            )
            cursor = None
    return ' '.join(parts)


def build_svg(drawings, indices, label):
    subset = [drawings[i] for i in indices]

    x0 = min(d['rect'].x0 for d in subset)
    y0 = min(d['rect'].y0 for d in subset)
    x1 = max(d['rect'].x1 for d in subset)
    y1 = max(d['rect'].y1 for d in subset)
    w, h = x1 - x0, y1 - y0

    paths = []
    for d in subset:
        data = items_to_path(d['items'])
        if not data:
            continue
        rule = ' fill-rule="evenodd"' if d.get('even_odd') else ''
        paths.append(f'  <path d="{data} Z" fill="#ffffff"{rule}/>')

    body = '\n'.join(paths)
    # Blanco explícito en lugar de currentColor: los SVG se incrustan con <img>, y ahí
    # currentColor no hereda del CSS de la página (y algunos motores lo resuelven a
    # negro). Todo el sitio va sobre azul oscuro, así que el blanco es siempre correcto.
    # Para un fondo claro habría que generar una variante con otro color.
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="{x0:.2f} {y0:.2f} {w:.2f} {h:.2f}" '
        f'role="img" aria-label="{label}">\n{body}\n</svg>\n'
    )


def main():
    doc = fitz.open(PDF)
    drawings = doc[0].get_drawings()
    OUT.mkdir(parents=True, exist_ok=True)

    for name, indices, label in [
        ('emblem.svg', EMBLEM, 'Emblema Bio.design'),
        ('wordmark.svg', WORDMARK, 'Bio.design'),
    ]:
        svg = build_svg(drawings, indices, label)
        (OUT / name).write_text(svg, encoding='utf-8')
        print(f'{name}: {len(svg)} bytes, {svg.count("<path")} paths')


if __name__ == '__main__':
    main()
