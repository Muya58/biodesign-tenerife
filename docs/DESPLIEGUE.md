# Despliegue — Bio.design Tenerife (Fase 1)

Pasos que debe hacer Josep con sus propias cuentas. Ninguno se pudo automatizar
desde la sesión de desarrollo porque requieren credenciales.

## 1. Base de datos (Supabase)

Abre el editor SQL del proyecto Supabase que ya usas para el chatbot de Apavi Green
y ejecuta el contenido de [`supabase/schema.sql`](../supabase/schema.sql) una sola vez.
Crea la tabla `biodesign_leads` y su índice.

Después, copia de la configuración del proyecto:
- `SUPABASE_URL`
- `SUPABASE_SERVICE_KEY` (la *service role key*, no la anon key — el backend necesita
  escribir saltándose RLS)

## 2. Repositorio en GitHub

```bash
gh repo create biodesign-tenerife --private --source=. --remote=origin --push
```

La rama de trabajo es `feat/fase1`. Fusiónala a `master` cuando valides el resultado.

## 3. Proyecto en Vercel

1. Importa el repositorio de GitHub como proyecto nuevo en Vercel.
2. Framework preset: **Other** (sitio estático, sin build step).
3. Root directory: la raíz del repositorio.
4. Configura las variables de entorno (pestaña Settings → Environment Variables),
   tomando los nombres de [`.env.example`](../.env.example):

| Variable | Valor |
|---|---|
| `SUPABASE_URL` | del paso 1 |
| `SUPABASE_SERVICE_KEY` | del paso 1 |
| `RESEND_API_KEY` | tu clave de Resend (la misma cuenta del chatbot) |
| `RESEND_FROM` | remitente verificado en Resend para el nuevo dominio |
| `NOTIFICATION_EMAIL` | dónde quieres recibir los avisos de lead |
| `ADMIN_PASSWORD` | contraseña del panel `/admin` — elige una larga |
| `ADMIN_SESSION_SECRET` | cadena aleatoria larga, ej. `openssl rand -hex 32` |
| `TELEGRAM_BOT_TOKEN` | *opcional* — solo si quieres aviso por Telegram |
| `OPERATOR_TELEGRAM_CHAT_ID` | *opcional* — chat(s) que reciben el aviso |

Si dejas las dos variables de Telegram vacías, el aviso por Telegram simplemente
se omite; el email sigue funcionando.

## 4. Dominio

1. Registra el dominio definitivo (a decidir; el código usa `biodesign-tenerife.com`
   como marcador de posición).
2. Conéctalo en Vercel → Settings → Domains.
3. Verifica el dominio en Resend para poder enviar desde él.
4. **Sustituye el dominio marcador** en las etiquetas `<link rel="canonical">` de todas
   las páginas y en los textos legales:

```bash
grep -rl "biodesign-tenerife.com" --include="*.html" .
```

## 5. Comprobación posterior al despliegue

- [ ] Envía un lead de prueba desde `/cuestionario.html`
- [ ] Confirma que aparece en la tabla `biodesign_leads` de Supabase
- [ ] Confirma que llega el email de aviso
- [ ] Entra en `/admin` con `ADMIN_PASSWORD` y comprueba que ves el lead
- [ ] Cambia el estado del lead a "contactado" y recarga para ver que persiste

## Pendiente / recomendaciones

Cosas fuera del alcance de Fase 1 que conviene valorar antes o poco después del lanzamiento:

- **Logo y tipografía oficiales.** El emblema del hero es una reconstrucción en SVG
  hecha a partir de la foto de referencia, y el wordmark usa Poppins como aproximación.
  Si consigues el brand kit oficial de Bio.design (SVG del logo + archivos de fuente),
  se sustituyen sin tocar el resto del sitio.
- **`robots.txt` y `sitemap.xml`.** No están incluidos en Fase 1. Recomendable añadirlos
  antes de pedir indexación en Google Search Console.
- **Datos de contacto propios.** Ahora mismo `contacto.html` usa el teléfono y el email
  de Apavi Green (`+34 654 795 518`, `web@apavigreen.com`). Si Bio.design Tenerife
  tendrá línea o buzón propios, actualízalos.
- **Política de cookies.** Está redactada para el estado actual del sitio: sin cookies
  propias y sin analítica. Si añades Google Analytics, Meta Pixel o similar, hay que
  actualizar `cookies.html` **y** añadir un banner de consentimiento antes de activarlos.
- **Fase 2: inglés y alemán.** La estructura está preparada para añadir `/en/` y `/de/`
  con `hreflang`, según lo acordado en la spec.
