# Bio-Design Tenerife — Sitio web del concesionario oficial (Fase 1)

**Fecha:** 2026-07-29
**Repositorio:** `C:\Users\josep\biodesign-tenerife` (git independiente)
**Cliente:** Apavi Green, concesionario oficial de Bio.design S.p.A. en la provincia de Santa Cruz de Tenerife

## Contexto

Apavi Green es ahora concesionario oficial de Bio.design, fabricante italiano de piscinas de arena (fundado en Milán en 1980, +40 años de experiencia). Se necesita una web propia (dominio y proyecto separados de la web verde de Apavi Green) que presente Bio.design a clientes de Tenerife, tomando como referencia visual y estructural `https://bio.design/es/`, dejando explícito que la concesión de Apavi Green es **exclusiva de la provincia de Santa Cruz de Tenerife**.

Este spec cubre **Fase 1**: el sitio completo en español + backend de leads + panel de administración. La traducción a inglés y alemán (`/en/`, `/de/`) es una **Fase 2** con spec propia, posterior a validar el contenido en español.

## Fuentes de referencia usadas

- `https://bio.design/es/` — estructura de navegación y secciones (navegado en vivo para este spec).
- `C:\Users\josep\Apavi Green\CATALOGO Fotografico Biodesign.pdf` — catálogo oficial (86 páginas). Se extrajeron 91 fotos reales en alta resolución vía PyMuPDF (pdftoppm no disponible en el sistema) a `assets/img/catalogo-raw/` en este proyecto, pendientes de curar/renombrar antes de usarlas en `realizaciones.html`.
- Foto de referencia del hero (logo Bio.design sobre fondo azul con destellos dorados) proporcionada por Josep en el chat — sirve de referencia visual para la animación del hero; no es un archivo de marca oficial.
- Patrones reutilizados de `C:\Users\josep\Apavi Green\Apavi Green\` (tokens CSS, estructura de `cuestionario.html`, convención de `_partials`) — solo como convención de código, **no** se comparte diseño visual con la web verde de Apavi Green.

## Alcance Fase 1

Sitio estático multi-página en español + backend serverless mínimo para capturar leads del cuestionario, con panel de administración protegido.

### Páginas

| Página | Contenido |
|---|---|
| `index.html` | Hero animado + secciones: personalización, integración con el jardín, eco-compatibilidad, protección Microban, CTA a cuestionario |
| `tecnologia.html` | La Tecnología Bio.design: revestimientos, juntas de dilatación, patente, Microban SilverShield |
| `quienes-somos.html` | Apavi Green como concesionario oficial + historia de Bio.design (Milán, 1980, +40 años) + **aviso de exclusividad territorial** |
| `realizaciones.html` | Galería de fotos reales del catálogo, filtrable por Piscina privada / Piscina pública |
| `cuestionario.html` | Configurador/presupuesto multi-paso (tipo de piscina, tamaño aproximado, ubicación, presupuesto, datos de contacto) |
| `contacto.html` | Formulario de contacto + datos + mapa/zona de cobertura (solo Santa Cruz de Tenerife) |
| `aviso-legal.html`, `privacidad.html`, `cookies.html` | Legal, adaptando boilerplate de Apavi Green a la nueva entidad/dominio |
| `admin/index.html` | Panel de leads protegido por contraseña |

### Aviso de exclusividad territorial

El texto "Concesionario Oficial Bio.design — Provincia de Santa Cruz de Tenerife" (o equivalente) debe aparecer en:
- Footer de **todas** las páginas.
- Badge visible junto al logo en la cabecera.
- Sección destacada en `quienes-somos.html` y `contacto.html`.

No debe sugerirse en ningún texto o imagen que la concesión cubre Canarias entera ni otras provincias.

## Hero / animación del logo

- Fondo azul noche con partículas doradas/arena tipo bokeh (referencia: foto proporcionada por Josep), en una versión más contenida (el emblema no ocupa toda la pantalla, es de tamaño pequeño-mediano).
- El emblema (símbolo estilizado de ola/persona) gira sobre su eje en bucle infinito usando transformaciones CSS 3D (`rotateY`), sin librerías 3D pesadas (nada de Three.js) para mantener buen rendimiento en móvil.
- Jerarquía visual debajo del emblema: wordmark **"BIO.design"**, y debajo, más pequeño, **"by Apavi Green"**.

### Limitaciones conocidas (a resolver si Josep consigue los archivos oficiales)

1. **Logo:** no se dispone del archivo vectorial oficial de Bio-Design (SVG/AI/EPS). Se reconstruirá el emblema como SVG a partir de la foto de referencia, fiel visualmente pero no idéntico al original.
2. **Tipografía:** "BIO.design" usa una fuente custom del fabricante que no está disponible. Se aproximará con una Google Font similar (geométrica, redondeada).

Si en el futuro Josep obtiene el brand kit oficial de Bio.design (logo vectorial + fuente), ambos elementos se sustituyen directamente sin rediseñar el resto del sitio.

## Cuestionario + backend de leads + panel

- **Frontend:** cuestionario multi-paso adaptado del patrón ya usado en `cuestionario.html` de Apavi Green (misma UX: barra de progreso, tarjetas por paso, pills de selección), con paleta propia de Bio.design.
- **Backend:** funciones serverless en Vercel (`api/leads.js` o similar) que insertan cada envío en una tabla nueva `biodesign_leads` en el proyecto Supabase que Josep ya usa para el chatbot de Apavi Green (se reutiliza la cuenta existente, no se crea infraestructura nueva).
- **Notificaciones:** email vía Resend (cuenta ya existente) al correo de Josep; Telegram opcional reutilizando el bot `@ApaviGreenBot` ya operativo, si Josep lo confirma en el plan de implementación.
- **Panel `/admin`:** login simple por contraseña (variable de entorno), lista de leads con estado (nuevo / contactado / cerrado), sin gestión de usuarios múltiple en esta fase.

## Multi-idioma (preparación para Fase 2)

Fase 1 se construye solo en español, pero la arquitectura de carpetas y componentes se diseña para que Fase 2 pueda añadir `/en/` y `/de/` como copias de la estructura de páginas con hreflang, sin reescribir CSS/JS ni el backend de leads.

## Stack técnico y despliegue

- HTML/CSS/JS estático (sin framework ni build step) + funciones serverless de Vercel para el backend mínimo.
- Mismo hosting (Vercel) que ya usa `platform/` en el monorepo Nehunaya Flow.
- Base de datos: Supabase (proyecto existente, tabla nueva).
- Email: Resend (cuenta existente).
- Variables de entorno para credenciales (Supabase, Resend, Telegram) — nunca en el código fuente.
- Repositorio Git independiente en `C:\Users\josep\biodesign-tenerife`, deploy propio en Vercel con su propio dominio (a definir por Josep).

## Fuera de alcance (Fase 1)

- Traducciones a inglés/alemán (Fase 2).
- Gestión de usuarios múltiples en el panel de administración.
- Integración de pagos o firma de contratos online.
- Logo/tipografía oficiales de fábrica (se usan aproximaciones hasta que Josep consiga el brand kit).
