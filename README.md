# Bio-Design Tenerife

Sitio web del concesionario oficial de Bio.design en la provincia de Santa Cruz de Tenerife (Apavi Green).

## Desarrollo local

No hay build step para el frontend: abre cualquier `.html` directamente o sirve la carpeta con cualquier servidor estático.

Para las funciones serverless (`api/`), instala dependencias y usa `vercel dev`:

```bash
npm install
npx vercel dev
```

## Variables de entorno

Copia `.env.example` a `.env` y rellena:
- `SUPABASE_URL` / `SUPABASE_SERVICE_KEY` — proyecto Supabase existente (mismo que el chatbot de Apavi Green), tabla `biodesign_leads` (ver `supabase/schema.sql`).
- `RESEND_API_KEY` / `RESEND_FROM` / `NOTIFICATION_EMAIL` — notificación por email de cada lead nuevo.
- `ADMIN_PASSWORD` / `ADMIN_SESSION_SECRET` — acceso al panel `/admin`.
- `TELEGRAM_BOT_TOKEN` / `OPERATOR_TELEGRAM_CHAT_ID` — opcional, solo si quieres notificación por Telegram además de email.

## Tests

```bash
npm test
```
