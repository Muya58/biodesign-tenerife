"""Sustituir el wordmark en texto por el logotipo oficial vectorizado en todas las páginas.

Antes el header y el hero escribían "BIO.design" con Poppins (una aproximación).
Ahora usan `assets/img/wordmark.svg`, extraído del catálogo oficial, para que las
letras sean exactamente las de la marca.

Uso:  python scripts/apply-official-logo.py
"""

from pathlib import Path

# Proporciones reales de los SVG extraídos (ver scripts/extract-logo.py).
EMBLEM_RATIO = 190.05 / 111.43   # 1.706
WORDMARK_RATIO = 359.24 / 108.93  # 3.298

# El emblema del header pasa de 28x20 (proporción inventada) a 28x16 (la real).
OLD_HEADER_EMBLEM = '<img src="{p}assets/img/emblem.svg" alt="Bio.design" width="28" height="20">'
NEW_HEADER_EMBLEM = '<img src="{p}assets/img/emblem.svg" alt="" width="28" height="16">'

OLD_HEADER_TEXT = '<div class="brand-lockup-text">BIO.design</div>'
NEW_HEADER_TEXT = (
    '<img class="brand-lockup-text" src="{p}assets/img/wordmark.svg" '
    'alt="Bio.design" width="108" height="33">'
)

# El hero: el <h1> deja de ser texto y pasa a contener el wordmark oficial.
# El alt conserva el texto para SEO y lectores de pantalla.
OLD_HERO = '''<h1 class="hero-wordmark">BIO<span class="dot">.</span>design</h1>'''
NEW_HERO = '''<h1 class="hero-wordmark"><img src="assets/img/wordmark.svg" alt="Bio.design" width="420" height="127"></h1>'''

# El cuestionario usa un lockup reducido con el wordmark en un <span>.
OLD_QUIZ_EMBLEM = '<img src="assets/img/emblem.svg" alt="Bio.design" width="24" height="17">'
NEW_QUIZ_EMBLEM = '<img src="assets/img/emblem.svg" alt="" width="24" height="14">'
OLD_QUIZ_TEXT = '<span class="brand-lockup-text">BIO.design</span>'
NEW_QUIZ_TEXT = (
    '<img class="brand-lockup-text" src="assets/img/wordmark.svg" '
    'alt="Bio.design" width="108" height="33">'
)


def main():
    changed = []
    for path in sorted(Path('.').glob('*.html')) + [Path('admin/index.html')]:
        if not path.exists():
            continue
        html = path.read_text(encoding='utf-8')
        original = html
        prefix = '../' if path.parent.name == 'admin' else ''

        html = html.replace(OLD_HEADER_EMBLEM.format(p=prefix), NEW_HEADER_EMBLEM.format(p=prefix))
        html = html.replace(OLD_HEADER_TEXT, NEW_HEADER_TEXT.format(p=prefix))
        html = html.replace(OLD_HERO, NEW_HERO)
        html = html.replace(OLD_QUIZ_EMBLEM, NEW_QUIZ_EMBLEM)
        html = html.replace(OLD_QUIZ_TEXT, NEW_QUIZ_TEXT)

        if html != original:
            path.write_text(html, encoding='utf-8')
            changed.append(str(path))

    print(f'ratios: emblema {EMBLEM_RATIO:.3f}, wordmark {WORDMARK_RATIO:.3f}')
    for c in changed:
        print('actualizado:', c)
    print(f'{len(changed)} ficheros')


if __name__ == '__main__':
    main()
