"""Generar una textura de cáusticas de agua que repite sin costuras.

Las cáusticas son las líneas de luz que la superficie ondulada del agua proyecta en el
fondo de una piscina. Se aproximan sumando ondas sinusoidales con frecuencias enteras
(lo que garantiza que la textura sea tileable) y quedándose con las crestas.

La animación NO se hace aquí: la textura es estática y el CSS la mueve con transforms,
que van por GPU. Animar un feTurbulence de SVG en cada frame sería mucho más costoso,
sobre todo en móvil.

Uso:  python scripts/make-caustics.py
Salida: assets/img/caustics.png (escala de grises sobre negro, para modo 'screen')
"""

import numpy as np
from PIL import Image
from pathlib import Path

OUT = Path('assets/img/caustics.png')
SIZE = 512          # lado del tile

# Vectores de onda (kx, ky, amplitud, fase). Al ser enteros, cada onda completa un
# número exacto de ciclos en el tile y el resultado repite sin costura. Se reparten en
# muchas direcciones distintas para que no aparezcan rayas diagonales.
WAVES = [
    ( 2,  1, 1.00, 0.0),
    ( 1, -2, 0.95, 1.7),
    (-2,  2, 0.80, 3.1),
    ( 3,  1, 0.70, 0.6),
    (-1,  3, 0.65, 2.4),
    ( 3, -3, 0.55, 4.2),
    ( 4,  2, 0.45, 1.1),
    (-3, -2, 0.42, 5.0),
    ( 2, -5, 0.35, 2.9),
    ( 5,  3, 0.30, 0.3),
    (-4,  5, 0.26, 3.8),
    ( 6, -2, 0.22, 1.5),
    ( 7,  4, 0.16, 4.7),
    (-6, -5, 0.14, 2.1),
]


def wave_field(size, waves):
    """Campo escalar suave y periódico en ambos ejes."""
    u = np.linspace(0, 2 * np.pi, size, endpoint=False)
    x, y = np.meshgrid(u, u)
    field = np.zeros((size, size), dtype=np.float64)
    total = 0.0
    for kx, ky, amp, phase in waves:
        field += amp * np.sin(kx * x + ky * y + phase)
        total += amp
    return field / total


def main():
    field = wave_field(SIZE, WAVES)

    # Las crestas (valores cerca de cero del campo) se convierten en líneas brillantes.
    ridges = np.clip(1.0 - np.abs(field), 0.0, 1.0) ** 22  # exponente alto => líneas finas

    # Un segundo juego con las fases desplazadas da los cruces típicos de las cáusticas.
    field2 = wave_field(SIZE, [(kx, ky, a, ph + 2.2) for kx, ky, a, ph in WAVES])
    ridges2 = np.clip(1.0 - np.abs(field2), 0.0, 1.0) ** 26

    caustics = np.clip(ridges + 0.55 * ridges2, 0.0, 1.0)
    caustics = caustics / caustics.max()

    img = Image.fromarray((caustics * 255).astype(np.uint8), mode='L')
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, optimize=True)

    kb = OUT.stat().st_size // 1024
    print(f'{OUT}: {SIZE}x{SIZE} — {kb} KB, brillo medio {caustics.mean()*100:.1f}%')


if __name__ == '__main__':
    main()
