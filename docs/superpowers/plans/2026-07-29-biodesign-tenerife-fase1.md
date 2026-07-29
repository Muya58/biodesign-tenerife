# Bio-Design Tenerife — Fase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the Fase 1 Spanish-language Bio-Design Tenerife website — a static multi-page site with a rotating-logo hero, a multi-step budget questionnaire, a serverless leads backend (Supabase + Resend), and a password-protected admin panel — as its own git project at `C:\Users\josep\biodesign-tenerife`.

**Architecture:** Static HTML/CSS/vanilla JS pages (no build step, no framework) sharing hand-copied header/footer markup, deployed on Vercel. A thin `api/` folder holds Node ESM serverless functions for lead capture, admin login, and admin lead listing. Pure logic (validation, session signing) is extracted into `lib/` modules so it can be unit-tested with Node's built-in test runner — no test framework dependency needed.

**Tech Stack:** HTML5, CSS3 (custom properties, no preprocessor), vanilla JS (ES modules in the browser via `<script type="module">`), Node.js ESM serverless functions on Vercel, `@supabase/supabase-js`, `resend`, Node's built-in `node:test` + `node:assert/strict`.

**Reference spec:** `docs/superpowers/specs/2026-07-29-biodesign-tenerife-design.md`

---

## File Structure

```
biodesign-tenerife/
├── package.json
├── vercel.json
├── .gitignore
├── .env.example
├── README.md
├── index.html
├── tecnologia.html
├── quienes-somos.html
├── realizaciones.html
├── cuestionario.html
├── contacto.html
├── aviso-legal.html
├── privacidad.html
├── cookies.html
├── admin/
│   └── index.html
├── assets/
│   ├── css/
│   │   ├── tokens.css
│   │   ├── main.css
│   │   └── components.css
│   ├── js/
│   │   ├── hero-logo.js
│   │   ├── cuestionario.js
│   │   └── admin.js
│   └── img/
│       ├── catalogo-raw/        (91 photos already extracted — present)
│       └── realizaciones/       (curated subset, created in Task 8)
├── lib/
│   ├── db.js
│   ├── email.js
│   ├── session.js
│   └── validators.js
├── api/
│   ├── leads.js
│   ├── admin-login.js
│   └── admin-leads.js
├── supabase/
│   └── schema.sql
└── tests/
    ├── validators.test.js
    ├── session.test.js
    ├── leads-handler.test.js
    └── smoke-pages.test.js
```

---

## Task 1: Project scaffolding

**Files:**
- Create: `package.json`
- Create: `.gitignore`
- Create: `.env.example`
- Create: `README.md`
- Create: `vercel.json`

- [ ] **Step 1: Create `package.json`**

```json
{
  "name": "biodesign-tenerife",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "test": "node --test tests/"
  },
  "dependencies": {
    "@supabase/supabase-js": "^2.45.0",
    "resend": "^4.0.0"
  }
}
```

- [ ] **Step 2: Create `.gitignore`**

```
node_modules/
.env
.env.local
.vercel
```

- [ ] **Step 3: Create `.env.example`**

```
SUPABASE_URL=
SUPABASE_SERVICE_KEY=
RESEND_API_KEY=
RESEND_FROM=notificaciones@biodesign-tenerife.com
NOTIFICATION_EMAIL=josepig1978@gmail.com
ADMIN_PASSWORD=
ADMIN_SESSION_SECRET=
TELEGRAM_BOT_TOKEN=
OPERATOR_TELEGRAM_CHAT_ID=
```

- [ ] **Step 4: Create `vercel.json`**

```json
{
  "functions": {
    "api/*.js": { "runtime": "nodejs20.x" }
  }
}
```

- [ ] **Step 5: Create `README.md`**

```markdown
# Bio-Design Tenerife

Sitio web del concesionario oficial de Bio.design en la provincia de Santa Cruz de Tenerife (Apavi Green).

## Desarrollo local

No hay build step para el frontend: abre cualquier `.html` directamente o sirve la carpeta con cualquier servidor estático.

Para las funciones serverless (`api/`), instala dependencias y usa `vercel dev`:

\`\`\`bash
npm install
npx vercel dev
\`\`\`

## Variables de entorno

Copia `.env.example` a `.env` y rellena:
- `SUPABASE_URL` / `SUPABASE_SERVICE_KEY` — proyecto Supabase existente (mismo que el chatbot de Apavi Green), tabla `biodesign_leads` (ver `supabase/schema.sql`).
- `RESEND_API_KEY` / `RESEND_FROM` / `NOTIFICATION_EMAIL` — notificación por email de cada lead nuevo.
- `ADMIN_PASSWORD` / `ADMIN_SESSION_SECRET` — acceso al panel `/admin`.
- `TELEGRAM_BOT_TOKEN` / `OPERATOR_TELEGRAM_CHAT_ID` — opcional, solo si quieres notificación por Telegram además de email.

## Tests

\`\`\`bash
npm test
\`\`\`
```

- [ ] **Step 6: Install dependencies**

Run: `cd "C:\Users\josep\biodesign-tenerife" && npm install`
Expected: `node_modules/` created, `package-lock.json` created, no errors.

- [ ] **Step 7: Commit**

```bash
git add package.json package-lock.json .gitignore .env.example README.md vercel.json
git commit -m "chore: project scaffolding"
```

---

## Task 2: Design tokens and base CSS

**Files:**
- Create: `assets/css/tokens.css`
- Create: `assets/css/main.css`
- Create: `assets/css/components.css`

- [ ] **Step 1: Create `assets/css/tokens.css`**

```css
:root {
  /* Bio-Design Tenerife palette — distinct from Apavi Green's green brand */
  --bd-navy-950: #060e1a;
  --bd-navy-900: #0a1628;
  --bd-navy-800: #142238;
  --bd-navy-700: #1e3350;
  --bd-sand-400: #e8c77e;
  --bd-sand-300: #f2d999;
  --bd-teal-400: #4fb8c4;
  --bd-white: #ffffff;
  --bd-ink-900: #12181f;

  --font-h: 'Poppins', sans-serif;
  --font-b: 'Inter', sans-serif;

  --r8: 8px;
  --r16: 16px;
  --r20: 20px;
  --r999: 999px;
}
```

- [ ] **Step 2: Create `assets/css/main.css`**

```css
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--bd-navy-950);
  color: rgba(255,255,255,.85);
  font-family: var(--font-b);
  line-height: 1.6;
}
h1, h2, h3 { font-family: var(--font-h); color: #fff; margin: 0 0 16px; letter-spacing: -.02em; }
h1 { font-size: clamp(32px, 5vw, 56px); font-weight: 800; }
h2 { font-size: clamp(24px, 3.5vw, 36px); font-weight: 700; }
p { margin: 0 0 16px; }
a { color: var(--bd-teal-400); text-decoration: none; }
img { max-width: 100%; display: block; }
.container { max-width: 1180px; margin: 0 auto; padding: 0 24px; }
section { padding: 80px 0; }

.site-header {
  position: sticky; top: 0; z-index: 50;
  display: flex; align-items: center; justify-content: space-between;
  padding: 16px 24px;
  background: rgba(6,14,26,.85);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid rgba(255,255,255,.06);
}
.site-header nav { display: flex; gap: 28px; align-items: center; }
.site-header nav a { color: rgba(255,255,255,.7); font-size: 14px; font-weight: 600; }
.site-header nav a:hover { color: #fff; }
.brand-lockup { display: flex; align-items: center; gap: 10px; }
.brand-lockup-text { font-family: var(--font-h); font-weight: 700; color: #fff; font-size: 18px; }
.brand-lockup-sub { font-size: 10px; color: rgba(255,255,255,.4); letter-spacing: .04em; }

.exclusivity-badge {
  display: inline-flex; align-items: center; gap: 6px;
  font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: .05em;
  color: var(--bd-navy-950);
  background: var(--bd-sand-400);
  padding: 5px 12px;
  border-radius: var(--r999);
}

.site-footer {
  padding: 48px 24px 32px;
  border-top: 1px solid rgba(255,255,255,.06);
  text-align: center;
  color: rgba(255,255,255,.4);
  font-size: 13px;
}
.site-footer .exclusivity-badge { margin-bottom: 16px; }

@media (max-width: 720px) {
  .site-header nav { display: none; }
  section { padding: 56px 0; }
}
```

- [ ] **Step 3: Create `assets/css/components.css`**

```css
.btn {
  display: inline-flex; align-items: center; justify-content: center;
  font-family: var(--font-h); font-weight: 700; font-size: 15px;
  padding: 13px 26px; border-radius: var(--r8);
  border: none; cursor: pointer; transition: background .2s, transform .1s;
}
.btn-primary { background: var(--bd-sand-400); color: var(--bd-navy-950); }
.btn-primary:hover { background: var(--bd-sand-300); }
.btn-ghost { background: rgba(255,255,255,.08); color: #fff; border: 1px solid rgba(255,255,255,.16); }
.btn-ghost:hover { background: rgba(255,255,255,.14); }

.card {
  background: rgba(255,255,255,.04);
  border: 1px solid rgba(255,255,255,.08);
  border-radius: var(--r16);
  padding: 32px;
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}
.gallery-item {
  border-radius: var(--r16);
  overflow: hidden;
  border: 1px solid rgba(255,255,255,.08);
}
.gallery-item img { aspect-ratio: 4/3; object-fit: cover; width: 100%; }

.gallery-filters { display: flex; gap: 10px; margin-bottom: 28px; }
.gallery-filter-btn {
  font-size: 13px; font-weight: 600; padding: 9px 18px; border-radius: var(--r999);
  border: 1px solid rgba(255,255,255,.14); background: transparent; color: rgba(255,255,255,.6);
  cursor: pointer; transition: all .15s;
}
.gallery-filter-btn.active, .gallery-filter-btn:hover { background: var(--bd-sand-400); color: var(--bd-navy-950); border-color: var(--bd-sand-400); }

.quiz-input {
  width: 100%;
  background: rgba(255,255,255,.06);
  border: 1px solid rgba(255,255,255,.12);
  border-radius: var(--r8);
  padding: 12px 16px;
  font-size: 15px;
  color: #fff;
  font-family: var(--font-b);
  transition: border-color .2s;
}
.quiz-input:focus { outline: none; border-color: var(--bd-sand-400); }
.quiz-input::placeholder { color: rgba(255,255,255,.25); }
.quiz-step h2 { margin-bottom: 20px; }
.quiz-step label { display: block; font-size: 14px; color: rgba(255,255,255,.7); margin-bottom: 6px; }
.quiz-success { text-align: center; padding: 20px; }
```

- [ ] **Step 4: Commit**

```bash
git add assets/css
git commit -m "feat: design tokens and base CSS for Bio-Design Tenerife"
```

---

## Task 3: Hero logo — SVG emblem and 3D rotation animation

The reference photo Josep shared shows a white emblem (a stylized wave/figure silhouette between two curved swoosh lines) above the "BIO.design" wordmark, on a navy background with gold sparkle bokeh. No official vector file exists (per spec), so this task hand-builds a faithful SVG approximation.

**Files:**
- Create: `assets/img/emblem.svg`
- Create: `assets/js/hero-logo.js`
- Modify: `assets/css/components.css` (append hero styles)

- [ ] **Step 1: Create the emblem SVG at `assets/img/emblem.svg`**

```svg
<svg viewBox="0 0 200 140" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Bio.design emblem">
  <path d="M10 55 C 50 5, 150 5, 190 55 C 150 40, 50 40, 10 55 Z" fill="#ffffff"/>
  <path d="M10 90 C 50 140, 150 140, 190 90 C 150 105, 50 105, 10 90 Z" fill="#ffffff"/>
  <g fill="#ffffff">
    <circle cx="100" cy="58" r="9"/>
    <path d="M100 68 C 92 78, 88 92, 92 108 L 100 100 L 108 108 C 112 92, 108 78, 100 68 Z"/>
    <path d="M92 78 L 70 92 M108 78 L 130 92" stroke="#ffffff" stroke-width="5" stroke-linecap="round"/>
  </g>
</svg>
```

- [ ] **Step 2: Append hero styles to `assets/css/components.css`**

```css
.hero {
  position: relative;
  min-height: 92vh;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  text-align: center;
  overflow: hidden;
  background: radial-gradient(ellipse at 50% 30%, var(--bd-navy-800) 0%, var(--bd-navy-950) 70%);
}
.hero-sparkles {
  position: absolute; inset: 0;
  background-image:
    radial-gradient(2px 2px at 20% 85%, var(--bd-sand-400), transparent),
    radial-gradient(2px 2px at 35% 92%, var(--bd-sand-300), transparent),
    radial-gradient(1.5px 1.5px at 50% 80%, var(--bd-sand-400), transparent),
    radial-gradient(2px 2px at 65% 90%, var(--bd-sand-300), transparent),
    radial-gradient(1.5px 1.5px at 80% 83%, var(--bd-sand-400), transparent),
    radial-gradient(2px 2px at 90% 88%, var(--bd-sand-300), transparent),
    radial-gradient(1px 1px at 15% 20%, rgba(79,184,196,.6), transparent),
    radial-gradient(1px 1px at 70% 15%, rgba(79,184,196,.6), transparent),
    radial-gradient(1px 1px at 45% 10%, rgba(79,184,196,.6), transparent);
  background-repeat: no-repeat;
  opacity: .8;
  pointer-events: none;
}
.hero-emblem-stage {
  perspective: 800px;
  width: 120px; height: 84px;
  margin-bottom: 28px;
  z-index: 1;
}
.hero-emblem {
  width: 100%; height: 100%;
  animation: hero-spin 6s linear infinite;
  transform-style: preserve-3d;
}
@keyframes hero-spin {
  from { transform: rotateY(0deg); }
  to   { transform: rotateY(360deg); }
}
.hero-wordmark {
  font-family: var(--font-h); font-weight: 800;
  font-size: clamp(40px, 7vw, 72px);
  color: #fff; letter-spacing: -.01em;
  z-index: 1;
}
.hero-wordmark .dot { color: var(--bd-sand-400); }
.hero-by-line {
  z-index: 1;
  font-size: 14px; font-weight: 600; letter-spacing: .04em;
  color: rgba(255,255,255,.5);
  margin-top: 4px;
}
.hero-by-line strong { color: rgba(255,255,255,.8); }
.hero-cta-row { z-index: 1; display: flex; gap: 14px; margin-top: 32px; }

@media (prefers-reduced-motion: reduce) {
  .hero-emblem { animation: none; }
}
```

- [ ] **Step 3: Create `assets/js/hero-logo.js`**

The emblem is referenced as a plain `<img>` in the page markup (see Task 5) so it works when opening the HTML directly from disk — a `fetch()` of a local SVG would be blocked by the `file://` origin policy. This script only handles the reduced-motion preference, since the rotation itself is pure CSS.

```js
// Rotation is pure CSS (see .hero-emblem in components.css). This only
// honours a runtime change of the reduced-motion preference.
const motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');

function applyMotionPreference() {
  const emblem = document.querySelector('.hero-emblem');
  if (!emblem) return;
  emblem.style.animationPlayState = motionQuery.matches ? 'paused' : 'running';
}

applyMotionPreference();
motionQuery.addEventListener('change', applyMotionPreference);
```

- [ ] **Step 4: Commit**

```bash
git add assets/img/emblem.svg assets/js/hero-logo.js assets/css/components.css
git commit -m "feat: rotating hero emblem (SVG + CSS 3D animation)"
```

---

## Task 4: Shared header/footer markup (reference block)

No templating engine exists (static site, no build step), so header/footer are copy-pasted into every page — same convention already used across Apavi Green's site. This task defines the canonical markup once; every later page task pastes it verbatim.

**Files:**
- Create: `docs/superpowers/plans/_header-footer-snippet.md` (reference only, not shipped)

- [ ] **Step 1: Write the canonical header markup to the reference snippet file**

```markdown
## Header (paste into every page, adjust nav `aria-current`/active class per page)

\`\`\`html
<header class="site-header">
  <a href="index.html" class="brand-lockup">
    <img src="assets/img/emblem.svg" alt="Bio.design" width="28" height="20">
    <div>
      <div class="brand-lockup-text">BIO.design</div>
      <div class="brand-lockup-sub">by Apavi Green &middot; Sta. Cruz de Tenerife</div>
    </div>
  </a>
  <nav>
    <a href="tecnologia.html">Tecnología</a>
    <a href="quienes-somos.html">Quiénes somos</a>
    <a href="realizaciones.html">Realizaciones</a>
    <a href="contacto.html">Contacto</a>
    <a href="cuestionario.html" class="btn btn-primary" style="padding:9px 18px;font-size:13px;">Pide presupuesto</a>
  </nav>
</header>
\`\`\`

## Footer (paste into every page)

\`\`\`html
<footer class="site-footer">
  <div class="exclusivity-badge">Concesionario oficial Bio.design &middot; Provincia de Santa Cruz de Tenerife</div>
  <p>Apavi Green &middot; Concesionario Oficial Bio.design S.p.A. para la provincia de Santa Cruz de Tenerife.</p>
  <p>
    <a href="aviso-legal.html">Aviso legal</a> &middot;
    <a href="privacidad.html">Privacidad</a> &middot;
    <a href="cookies.html">Cookies</a>
  </p>
</footer>
\`\`\`
```

- [ ] **Step 2: Commit**

```bash
git add docs/superpowers/plans/_header-footer-snippet.md
git commit -m "docs: canonical header/footer snippet for static pages"
```

---

## Task 5: Home page (`index.html`)

**Files:**
- Create: `index.html`

- [ ] **Step 1: Create `index.html`**

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bio.design Tenerife &mdash; Piscinas de Arena | Concesionario Oficial</title>
  <meta name="description" content="Concesionario oficial de Bio.design en la provincia de Santa Cruz de Tenerife. Piscinas de arena a medida, tecnolog\u00eda italiana con m\u00e1s de 40 a\u00f1os de experiencia.">
  <link rel="canonical" href="https://biodesign-tenerife.com/index.html">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/tokens.css">
  <link rel="stylesheet" href="assets/css/main.css">
  <link rel="stylesheet" href="assets/css/components.css">
</head>
<body>

  <header class="site-header">
    <a href="index.html" class="brand-lockup">
      <img src="assets/img/emblem.svg" alt="Bio.design" width="28" height="20">
      <div>
        <div class="brand-lockup-text">BIO.design</div>
        <div class="brand-lockup-sub">by Apavi Green &middot; Sta. Cruz de Tenerife</div>
      </div>
    </a>
    <nav>
      <a href="tecnologia.html">Tecnología</a>
      <a href="quienes-somos.html">Quiénes somos</a>
      <a href="realizaciones.html">Realizaciones</a>
      <a href="contacto.html">Contacto</a>
      <a href="cuestionario.html" class="btn btn-primary" style="padding:9px 18px;font-size:13px;">Pide presupuesto</a>
    </nav>
  </header>

  <section class="hero">
    <div class="hero-sparkles"></div>
    <div class="hero-emblem-stage">
      <img class="hero-emblem" src="assets/img/emblem.svg" alt="Emblema Bio.design" width="120" height="84">
    </div>
    <h1 class="hero-wordmark">BIO<span class="dot">.</span>design</h1>
    <p class="hero-by-line">by <strong>Apavi Green</strong> &middot; Concesionario oficial, provincia de Santa Cruz de Tenerife</p>
    <div class="hero-cta-row">
      <a href="cuestionario.html" class="btn btn-primary">Solicitar presupuesto gratis</a>
      <a href="tecnologia.html" class="btn btn-ghost">Descubre la tecnología</a>
    </div>
  </section>

  <section>
    <div class="container">
      <h2>La piscina más emocionante que jamás haya existido</h2>
      <p>Un espacio acuático que puede adornar cualquier ambiente, formado según las necesidades de tu jardín y sin estructuras prefabricadas. Bio.design lleva más de 40 años perfeccionando la piscina de arena, y ahora está disponible en la provincia de Santa Cruz de Tenerife de la mano de Apavi Green.</p>
      <div class="gallery-grid">
        <div class="card">
          <h3>Personalización total</h3>
          <p>Cada piscina Bio.design es única: formas orgánicas, entradas graduales y acabados en cuarzo y arena natural.</p>
        </div>
        <div class="card">
          <h3>Integración con el jardín</h3>
          <p>Perfecta armonía con el paisaje, sin bordes artificiales ni hormigón visible.</p>
        </div>
        <div class="card">
          <h3>Eco-compatible</h3>
          <p>Premiada por su sostenibilidad: menor consumo de agua y energía a lo largo de todo su ciclo de vida.</p>
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="container card" style="text-align:center;">
      <h2>¿Interesado en una piscina Bio.design en Tenerife?</h2>
      <p>Configura tu piscina ideal y recibe un presupuesto gratuito de Apavi Green, concesionario oficial en la provincia de Santa Cruz de Tenerife.</p>
      <a href="cuestionario.html" class="btn btn-primary">Configura tu piscina</a>
    </div>
  </section>

  <footer class="site-footer">
    <div class="exclusivity-badge">Concesionario oficial Bio.design &middot; Provincia de Santa Cruz de Tenerife</div>
    <p>Apavi Green &middot; Concesionario Oficial Bio.design S.p.A. para la provincia de Santa Cruz de Tenerife.</p>
    <p>
      <a href="aviso-legal.html">Aviso legal</a> &middot;
      <a href="privacidad.html">Privacidad</a> &middot;
      <a href="cookies.html">Cookies</a>
    </p>
  </footer>

  <script type="module" src="assets/js/hero-logo.js"></script>
</body>
</html>
```

- [ ] **Step 2: Commit**

```bash
git add index.html
git commit -m "feat: home page with rotating hero"
```

---

## Task 6: Technology page (`tecnologia.html`)

**Files:**
- Create: `tecnologia.html`

- [ ] **Step 1: Create `tecnologia.html`** using the Task 4 header/footer snippet plus this main content, following the exact `<head>` block pattern from Task 5 (same CSS/font links, `<title>La Tecnología Bio.design | Bio.design Tenerife</title>`, canonical `https://biodesign-tenerife.com/tecnologia.html`):

```html
  <section style="padding-top:56px;">
    <div class="container">
      <h1>La Tecnología Bio.design</h1>
      <p>Descubre qué hace única a una piscina de arena Bio.design frente a una piscina tradicional de hormigón armado.</p>
      <div class="gallery-grid">
        <div class="card">
          <h3>Revestimientos personalizables</h3>
          <p>Todos los revestimientos son personalizables con mezclas de guijarros, arena y cuarzo, logrando un efecto único y natural que imita el fondo de una playa real.</p>
        </div>
        <div class="card">
          <h3>Juntas de dilatación sinuosas</h3>
          <p>Las líneas sinuosas del revestimiento reducen el estrés mecánico y previenen grietas, además de embellecer el espejo de agua con efectos cromáticos naturales.</p>
        </div>
        <div class="card">
          <h3>Tecnología patentada</h3>
          <p>Un sistema de construcción brevettado y en constante evolución que permite que cada piscina Bio.design sea única, personalizable y eco-compatible.</p>
        </div>
        <div class="card">
          <h3>Protección Microban&reg; SilverShield&reg;</h3>
          <p>Bio.design es socio de Microban International: un sistema de revestimiento con resinas antibacterianas que mantiene la piscina más limpia y fresca durante más tiempo.</p>
        </div>
      </div>
    </div>
  </section>
  <section>
    <div class="container card" style="text-align:center;">
      <h2>¿Quieres ver esta tecnología en tu jardín?</h2>
      <a href="cuestionario.html" class="btn btn-primary">Solicitar presupuesto gratis</a>
    </div>
  </section>
```

- [ ] **Step 2: Commit**

```bash
git add tecnologia.html
git commit -m "feat: technology page"
```

---

## Task 7: About / official dealer page (`quienes-somos.html`)

**Files:**
- Create: `quienes-somos.html`

- [ ] **Step 1: Create `quienes-somos.html`** (same head pattern, `<title>Quiénes Somos | Bio.design Tenerife</title>`, canonical `.../quienes-somos.html`) with this main content:

```html
  <section style="padding-top:56px;">
    <div class="container">
      <h1>Concesionario Oficial Bio.design en Tenerife</h1>
      <div class="exclusivity-badge" style="margin-bottom:24px;">Exclusivo para la provincia de Santa Cruz de Tenerife</div>
      <p>Apavi Green es el <strong>concesionario oficial de Bio.design S.p.A.</strong> para la <strong>provincia de Santa Cruz de Tenerife</strong>. Esta concesión nos autoriza a diseñar, instalar y dar mantenimiento a piscinas de arena Bio.design exclusivamente dentro de esta provincia, con la garantía y el respaldo técnico directo del fabricante italiano.</p>
      <p><strong>Importante:</strong> nuestra concesión oficial cubre únicamente la provincia de Santa Cruz de Tenerife. Para instalaciones en otras provincias o islas, Bio.design cuenta con otros concesionarios autorizados.</p>
      <h2>Bio.design: 40 años dando forma al agua</h2>
      <p>Bio.design S.p.A. nace en Milán en 1980 y es hoy una empresa líder en el mercado de fuentes monumentales, lagos artificiales y piscinas de arena, con un departamento de investigación y desarrollo propio y una red internacional de concesionarios autorizados.</p>
    </div>
  </section>
```

- [ ] **Step 2: Commit**

```bash
git add quienes-somos.html
git commit -m "feat: quienes somos page with territorial exclusivity notice"
```

---

## Task 8: Curate catalog photos and build the gallery page

**Files:**
- Create: `assets/img/realizaciones/` (curated, renamed copies)
- Create: `realizaciones.html`

- [ ] **Step 1: Inspect and select images**

Run: `ls assets/img/catalogo-raw | head -20` and open a sample of the largest files (already reviewed during brainstorming: `p04_0_1360x764.png`, `p11_0_1357x716.png`, `p12_1_1093x1263.png`, `p14_3_1157x988.png`, `p16_0_1070x1007.png` are confirmed real pool photography). Select at least 12 images with clear pool shots (skip logos/text-only pages, skip anything under 600px wide) and note the source filenames.

- [ ] **Step 2: Copy and rename the selected images into `assets/img/realizaciones/`**

```bash
mkdir -p assets/img/realizaciones
cp assets/img/catalogo-raw/p04_0_1360x764.png assets/img/realizaciones/piscina-privada-01.png
cp assets/img/catalogo-raw/p11_0_1357x716.png assets/img/realizaciones/piscina-privada-02.png
cp assets/img/catalogo-raw/p12_1_1093x1263.png assets/img/realizaciones/piscina-publica-01.png
cp assets/img/catalogo-raw/p14_3_1157x988.png assets/img/realizaciones/piscina-privada-03.png
cp assets/img/catalogo-raw/p16_0_1070x1007.png assets/img/realizaciones/piscina-privada-04.png
```
(continue for the rest of the selected set from Step 1, alternating `piscina-privada-NN` / `piscina-publica-NN` based on what each photo actually shows — a residential backyard vs. a hotel/resort setting)

- [ ] **Step 3: Create `realizaciones.html`** (same head pattern, `<title>Realizaciones | Bio.design Tenerife</title>`) with this main content:

```html
  <section style="padding-top:56px;">
    <div class="container">
      <h1>Realizaciones Bio.design</h1>
      <p>Una selección de piscinas de arena Bio.design instaladas en todo el mundo. Calidad, naturalidad y belleza, integrando productos naturales con las mejores tecnologías.</p>
      <div class="gallery-filters">
        <button class="gallery-filter-btn active" data-filter="all">Todas</button>
        <button class="gallery-filter-btn" data-filter="privada">Piscina privada</button>
        <button class="gallery-filter-btn" data-filter="publica">Piscina pública</button>
      </div>
      <div class="gallery-grid" id="galleryGrid">
        <div class="gallery-item" data-category="privada"><img src="assets/img/realizaciones/piscina-privada-01.png" alt="Piscina de arena Bio.design privada" loading="lazy"></div>
        <div class="gallery-item" data-category="privada"><img src="assets/img/realizaciones/piscina-privada-02.png" alt="Piscina de arena Bio.design privada" loading="lazy"></div>
        <div class="gallery-item" data-category="publica"><img src="assets/img/realizaciones/piscina-publica-01.png" alt="Piscina de arena Bio.design pública" loading="lazy"></div>
        <div class="gallery-item" data-category="privada"><img src="assets/img/realizaciones/piscina-privada-03.png" alt="Piscina de arena Bio.design privada" loading="lazy"></div>
        <div class="gallery-item" data-category="privada"><img src="assets/img/realizaciones/piscina-privada-04.png" alt="Piscina de arena Bio.design privada" loading="lazy"></div>
      </div>
    </div>
  </section>
  <script>
    document.querySelectorAll('.gallery-filter-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.gallery-filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const filter = btn.dataset.filter;
        document.querySelectorAll('.gallery-item').forEach(item => {
          item.style.display = (filter === 'all' || item.dataset.category === filter) ? '' : 'none';
        });
      });
    });
  </script>
```

- [ ] **Step 4: Commit**

```bash
git add assets/img/realizaciones realizaciones.html
git commit -m "feat: realizaciones gallery with curated catalog photos"
```

---

## Task 9: Contact page (`contacto.html`)

**Files:**
- Create: `contacto.html`

- [ ] **Step 1: Create `contacto.html`** (same head pattern, `<title>Contacto | Bio.design Tenerife</title>`) with this main content:

```html
  <section style="padding-top:56px;">
    <div class="container">
      <h1>Contacta con nosotros</h1>
      <div class="exclusivity-badge" style="margin-bottom:24px;">Atendemos exclusivamente la provincia de Santa Cruz de Tenerife</div>
      <div class="card">
        <p>¿Tienes un proyecto en mente? Escríbenos y te responderemos en menos de 24 horas.</p>
        <p><strong>Teléfono / WhatsApp:</strong> <a href="tel:+34600000000">+34 600 000 000</a></p>
        <p><strong>Email:</strong> <a href="mailto:info@biodesign-tenerife.com">info@biodesign-tenerife.com</a></p>
        <a href="cuestionario.html" class="btn btn-primary">Solicitar presupuesto</a>
      </div>
    </div>
  </section>
```

- [ ] **Step 2: Commit**

```bash
git add contacto.html
git commit -m "feat: contact page"
```

---

## Task 10: Legal pages

**Files:**
- Create: `aviso-legal.html`
- Create: `privacidad.html`
- Create: `cookies.html`

- [ ] **Step 1: Read the existing Apavi Green legal pages for boilerplate structure**

Run: `cat "C:\Users\josep\Apavi Green\Apavi Green\aviso-legal.html"` and `cat "C:\Users\josep\Apavi Green\Apavi Green\privacidad.html"` and `cat "C:\Users\josep\Apavi Green\Apavi Green\cookies.html"` — reuse their section structure (identidad del responsable, objeto, propiedad intelectual / tratamiento de datos / política de cookies), replacing every "Apavi Green" identity/domain reference with "Bio.design Tenerife (Apavi Green)" and the placeholder domain `biodesign-tenerife.com`.

- [ ] **Step 2: Create `aviso-legal.html`, `privacidad.html`, `cookies.html`** using the Task 4 header/footer and the Task 5 head pattern (titles: "Aviso Legal", "Política de Privacidad", "Política de Cookies" — each ` | Bio.design Tenerife`), adapting the Apavi Green boilerplate content per Step 1 to reference Bio.design Tenerife / Apavi Green as data controller and the placeholder domain.

- [ ] **Step 3: Commit**

```bash
git add aviso-legal.html privacidad.html cookies.html
git commit -m "feat: legal pages (aviso legal, privacidad, cookies)"
```

---

## Task 11: Questionnaire validation logic (TDD)

Pure validation logic lives in `lib/validators.js` so both the frontend (UX feedback) and the backend (security boundary — never trust the client) can each call it, without needing a bundler to share code between browser and Node.

**Files:**
- Create: `lib/validators.js`
- Test: `tests/validators.test.js`

- [ ] **Step 1: Write the failing test**

```js
// tests/validators.test.js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { validateLead } from '../lib/validators.js';

test('accepts a complete valid lead', () => {
  const result = validateLead({
    poolType: 'privada',
    sizeM2: '40',
    location: 'La Laguna, Tenerife',
    budgetRange: '15000-25000',
    name: 'Ana García',
    phone: '+34600123456',
    email: 'ana@example.com',
    privacyAccepted: true,
  });
  assert.equal(result.valid, true);
  assert.deepEqual(result.errors, {});
});

test('rejects missing required fields', () => {
  const result = validateLead({});
  assert.equal(result.valid, false);
  assert.ok(result.errors.name);
  assert.ok(result.errors.phone);
  assert.ok(result.errors.privacyAccepted);
});

test('rejects an invalid email when provided', () => {
  const result = validateLead({
    poolType: 'privada', sizeM2: '40', location: 'X', budgetRange: '15000-25000',
    name: 'Ana', phone: '+34600123456', email: 'not-an-email', privacyAccepted: true,
  });
  assert.equal(result.valid, false);
  assert.ok(result.errors.email);
});

test('rejects when privacy policy is not accepted', () => {
  const result = validateLead({
    poolType: 'privada', sizeM2: '40', location: 'X', budgetRange: '15000-25000',
    name: 'Ana', phone: '+34600123456', email: 'ana@example.com', privacyAccepted: false,
  });
  assert.equal(result.valid, false);
  assert.equal(result.errors.privacyAccepted, 'Debes aceptar la política de privacidad.');
});
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `node --test tests/validators.test.js`
Expected: FAIL — `Cannot find module '../lib/validators.js'`

- [ ] **Step 3: Write the implementation**

```js
// lib/validators.js
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const PHONE_RE = /^\+?[0-9\s-]{7,15}$/;

export function validateLead(payload = {}) {
  const errors = {};

  if (!payload.name || !String(payload.name).trim()) {
    errors.name = 'El nombre es obligatorio.';
  }
  if (!payload.phone || !PHONE_RE.test(String(payload.phone).trim())) {
    errors.phone = 'Introduce un teléfono válido.';
  }
  if (payload.email && !EMAIL_RE.test(String(payload.email).trim())) {
    errors.email = 'Introduce un email válido.';
  }
  if (!payload.poolType) {
    errors.poolType = 'Selecciona el tipo de piscina.';
  }
  if (!payload.location || !String(payload.location).trim()) {
    errors.location = 'Indica la ubicación aproximada.';
  }
  if (payload.privacyAccepted !== true) {
    errors.privacyAccepted = 'Debes aceptar la política de privacidad.';
  }

  return { valid: Object.keys(errors).length === 0, errors };
}
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `node --test tests/validators.test.js`
Expected: PASS — 4 tests passing.

- [ ] **Step 5: Commit**

```bash
git add lib/validators.js tests/validators.test.js
git commit -m "feat: lead validation logic with tests"
```

---

## Task 12: Questionnaire frontend (`cuestionario.html` + `assets/js/cuestionario.js`)

**Files:**
- Create: `cuestionario.html`
- Create: `assets/js/cuestionario.js`

- [ ] **Step 1: Create `assets/js/cuestionario.js`**

```js
const STEPS = ['poolType', 'details', 'contact'];
let currentStep = 0;
const state = { poolType: '', sizeM2: '', location: '', budgetRange: '', name: '', phone: '', email: '', privacyAccepted: false };

function showStep(index) {
  document.querySelectorAll('.quiz-step').forEach((el, i) => {
    el.style.display = i === index ? '' : 'none';
  });
  document.getElementById('quizProgress').style.width = `${((index + 1) / STEPS.length) * 100}%`;
  document.getElementById('prevBtn').style.visibility = index === 0 ? 'hidden' : 'visible';
  document.getElementById('nextBtn').textContent = index === STEPS.length - 1 ? 'Enviar' : 'Siguiente';
}

function collectStepInputs() {
  document.querySelectorAll('[data-field]').forEach(el => {
    if (el.type === 'checkbox') state[el.dataset.field] = el.checked;
    else if (el.type === 'radio') { if (el.checked) state[el.dataset.field] = el.value; }
    else state[el.dataset.field] = el.value;
  });
}

async function submitLead() {
  const res = await fetch('/api/leads', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(state),
  });
  const data = await res.json();
  const form = document.getElementById('quizForm');
  if (res.ok) {
    form.innerHTML = '<div class="quiz-success"><h2>¡Gracias, ' + state.name + '!</h2><p>Hemos recibido tu solicitud. Un técnico de Apavi Green se pondrá en contacto contigo en menos de 24 horas.</p></div>';
  } else {
    alert(Object.values(data.errors || { general: 'No se pudo enviar el formulario. Inténtalo de nuevo.' }).join('\n'));
  }
}

document.getElementById('nextBtn').addEventListener('click', () => {
  collectStepInputs();
  if (currentStep < STEPS.length - 1) {
    currentStep += 1;
    showStep(currentStep);
  } else {
    submitLead();
  }
});

document.getElementById('prevBtn').addEventListener('click', () => {
  if (currentStep > 0) {
    currentStep -= 1;
    showStep(currentStep);
  }
});

showStep(currentStep);
```

- [ ] **Step 2: Create `cuestionario.html`** (same head pattern, `<title>Solicita tu presupuesto | Bio.design Tenerife</title>`, `<meta name="robots" content="noindex">`) with this body (replaces the standard header/footer with the focused quiz chrome, following the same minimal-topbar convention Apavi Green already uses on its own `cuestionario.html`):

```html
<body>
<div class="quiz-page" style="min-height:100vh; display:flex; flex-direction:column;">
  <div style="padding:20px 24px; display:flex; align-items:center; justify-content:space-between; border-bottom:1px solid rgba(255,255,255,.06);">
    <a href="index.html" class="brand-lockup">
      <img src="assets/img/emblem.svg" alt="Bio.design" width="24" height="17">
      <span class="brand-lockup-text">BIO.design</span>
    </a>
    <a href="index.html" style="font-size:13px;color:rgba(255,255,255,.4);">&larr; Volver al inicio</a>
  </div>
  <div style="height:3px; background:rgba(255,255,255,.08);">
    <div id="quizProgress" style="height:100%; background:var(--bd-sand-400); border-radius:2px; transition:width .4s ease; width:0%;"></div>
  </div>
  <div style="flex:1; display:flex; align-items:center; justify-content:center; padding:48px 20px;">
    <form id="quizForm" class="card" style="max-width:640px; width:100%;" onsubmit="return false;">

      <div class="quiz-step">
        <h2>¿Qué tipo de piscina buscas?</h2>
        <label><input type="radio" name="poolType" data-field="poolType" value="privada" checked> Piscina privada (vivienda particular)</label><br>
        <label><input type="radio" name="poolType" data-field="poolType" value="publica"> Piscina pública (hotel, urbanización, negocio)</label>
      </div>

      <div class="quiz-step" style="display:none;">
        <h2>Cuéntanos más</h2>
        <label>Tamaño aproximado (m&sup2;)<br><input type="number" data-field="sizeM2" class="quiz-input" placeholder="Ej. 40"></label><br><br>
        <label>Ubicación (municipio, Tenerife)<br><input type="text" data-field="location" class="quiz-input" placeholder="Ej. La Laguna"></label><br><br>
        <label>Presupuesto orientativo<br>
          <select data-field="budgetRange" class="quiz-input">
            <option value="15000-25000">15.000&euro; - 25.000&euro;</option>
            <option value="25000-40000">25.000&euro; - 40.000&euro;</option>
            <option value="40000+">Más de 40.000&euro;</option>
          </select>
        </label>
      </div>

      <div class="quiz-step" style="display:none;">
        <h2>Tus datos de contacto</h2>
        <label>Nombre<br><input type="text" data-field="name" class="quiz-input" required></label><br><br>
        <label>Teléfono<br><input type="tel" data-field="phone" class="quiz-input" required></label><br><br>
        <label>Email<br><input type="email" data-field="email" class="quiz-input"></label><br><br>
        <label><input type="checkbox" data-field="privacyAccepted"> He leído y acepto la <a href="privacidad.html">política de privacidad</a></label>
      </div>

      <div style="display:flex; gap:12px; margin-top:24px;">
        <button type="button" id="prevBtn" class="btn btn-ghost">Anterior</button>
        <button type="button" id="nextBtn" class="btn btn-primary">Siguiente</button>
      </div>
    </form>
  </div>
</div>
<script src="assets/js/cuestionario.js"></script>
</body>
</html>
```

- [ ] **Step 3: Commit**

```bash
git add cuestionario.html assets/js/cuestionario.js
git commit -m "feat: multi-step questionnaire frontend"
```

---

## Task 13: Supabase schema

**Files:**
- Create: `supabase/schema.sql`

- [ ] **Step 1: Create `supabase/schema.sql`**

```sql
create table if not exists biodesign_leads (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  status text not null default 'nuevo' check (status in ('nuevo', 'contactado', 'cerrado')),
  pool_type text not null,
  size_m2 numeric,
  location text not null,
  budget_range text,
  name text not null,
  phone text not null,
  email text
);

create index if not exists biodesign_leads_created_at_idx on biodesign_leads (created_at desc);
```

- [ ] **Step 2: Manual step for Josep (cannot be automated from this session — no Supabase credentials available here)**

Note in the plan: Josep must open the Supabase SQL editor for the existing project (same one used by the Apavi Green chatbot) and run the contents of `supabase/schema.sql` once, then provide `SUPABASE_URL` and `SUPABASE_SERVICE_KEY` as environment variables (Task 16).

- [ ] **Step 3: Commit**

```bash
git add supabase/schema.sql
git commit -m "feat: biodesign_leads Supabase schema"
```

---

## Task 14: Leads backend — db/email libs and API handler (TDD)

**Files:**
- Create: `lib/db.js`
- Create: `lib/email.js`
- Create: `api/leads.js`
- Test: `tests/leads-handler.test.js`

- [ ] **Step 1: Create `lib/db.js`**

```js
import { createClient } from '@supabase/supabase-js';

let client;

export function getSupabaseClient() {
  if (!client) {
    client = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);
  }
  return client;
}

export async function insertLead(supabase, lead) {
  const { data, error } = await supabase
    .from('biodesign_leads')
    .insert({
      pool_type: lead.poolType,
      size_m2: lead.sizeM2 ? Number(lead.sizeM2) : null,
      location: lead.location,
      budget_range: lead.budgetRange || null,
      name: lead.name,
      phone: lead.phone,
      email: lead.email || null,
    })
    .select()
    .single();
  if (error) throw error;
  return data;
}
```

- [ ] **Step 2: Create `lib/email.js`**

```js
import { Resend } from 'resend';

export async function sendLeadNotification(lead) {
  if (!process.env.RESEND_API_KEY) return { skipped: true };
  const resend = new Resend(process.env.RESEND_API_KEY);
  return resend.emails.send({
    from: process.env.RESEND_FROM,
    to: process.env.NOTIFICATION_EMAIL,
    subject: `Nuevo lead Bio.design Tenerife: ${lead.name}`,
    text: `Nombre: ${lead.name}\nTeléfono: ${lead.phone}\nEmail: ${lead.email || '-'}\nTipo: ${lead.poolType}\nUbicación: ${lead.location}\nPresupuesto: ${lead.budgetRange || '-'}`,
  });
}

export async function sendTelegramNotification(lead) {
  if (!process.env.TELEGRAM_BOT_TOKEN || !process.env.OPERATOR_TELEGRAM_CHAT_ID) return { skipped: true };
  const url = `https://api.telegram.org/bot${process.env.TELEGRAM_BOT_TOKEN}/sendMessage`;
  const text = `Nuevo lead Bio.design Tenerife\nNombre: ${lead.name}\nTeléfono: ${lead.phone}\nUbicación: ${lead.location}`;
  return fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ chat_id: process.env.OPERATOR_TELEGRAM_CHAT_ID, text }),
  });
}
```

- [ ] **Step 3: Write the failing test for the handler logic**

```js
// tests/leads-handler.test.js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { buildLeadResponse } from '../api/leads.js';

test('returns 400 with field errors for an invalid payload', async () => {
  const result = await buildLeadResponse({}, {
    insertLead: async () => { throw new Error('should not be called'); },
    sendLeadNotification: async () => {},
    sendTelegramNotification: async () => {},
  });
  assert.equal(result.status, 400);
  assert.ok(result.body.errors.name);
});

test('returns 200 and inserts + notifies for a valid payload', async () => {
  const validPayload = {
    poolType: 'privada', sizeM2: '40', location: 'La Laguna', budgetRange: '15000-25000',
    name: 'Ana', phone: '+34600123456', email: 'ana@example.com', privacyAccepted: true,
  };
  let inserted = null;
  let notified = false;
  const result = await buildLeadResponse(validPayload, {
    insertLead: async (lead) => { inserted = lead; return { id: 'abc123', ...lead }; },
    sendLeadNotification: async () => { notified = true; },
    sendTelegramNotification: async () => {},
  });
  assert.equal(result.status, 200);
  assert.equal(result.body.ok, true);
  assert.equal(inserted.name, 'Ana');
  assert.equal(notified, true);
});
```

- [ ] **Step 4: Run the test to verify it fails**

Run: `node --test tests/leads-handler.test.js`
Expected: FAIL — `api/leads.js` does not yet exist / does not export `buildLeadResponse`.

- [ ] **Step 5: Create `api/leads.js`**

```js
import { validateLead } from '../lib/validators.js';
import { getSupabaseClient, insertLead as insertLeadImpl } from '../lib/db.js';
import { sendLeadNotification as sendEmailImpl, sendTelegramNotification as sendTelegramImpl } from '../lib/email.js';

export async function buildLeadResponse(payload, deps) {
  const { valid, errors } = validateLead(payload);
  if (!valid) {
    return { status: 400, body: { ok: false, errors } };
  }

  const saved = await deps.insertLead(payload);
  await deps.sendLeadNotification(payload);
  await deps.sendTelegramNotification(payload);

  return { status: 200, body: { ok: true, id: saved.id } };
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.status(405).json({ ok: false, errors: { general: 'Método no permitido' } });
    return;
  }

  const supabase = getSupabaseClient();
  const { status, body } = await buildLeadResponse(req.body, {
    insertLead: (lead) => insertLeadImpl(supabase, lead),
    sendLeadNotification: sendEmailImpl,
    sendTelegramNotification: sendTelegramImpl,
  });
  res.status(status).json(body);
}
```

- [ ] **Step 6: Run the test to verify it passes**

Run: `node --test tests/leads-handler.test.js`
Expected: PASS — 2 tests passing.

- [ ] **Step 7: Commit**

```bash
git add lib/db.js lib/email.js api/leads.js tests/leads-handler.test.js
git commit -m "feat: leads API endpoint with Supabase insert and notifications"
```

---

## Task 15: Admin session signing (TDD)

**Files:**
- Create: `lib/session.js`
- Test: `tests/session.test.js`

- [ ] **Step 1: Write the failing test**

```js
// tests/session.test.js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { signSession, verifySession } from '../lib/session.js';

const SECRET = 'test-secret-value';

test('a freshly signed session verifies successfully', () => {
  const token = signSession(SECRET, 3600);
  assert.equal(verifySession(token, SECRET), true);
});

test('a tampered token fails verification', () => {
  const token = signSession(SECRET, 3600);
  const tampered = token.slice(0, -1) + (token.slice(-1) === 'a' ? 'b' : 'a');
  assert.equal(verifySession(tampered, SECRET), false);
});

test('an expired token fails verification', () => {
  const token = signSession(SECRET, -10);
  assert.equal(verifySession(token, SECRET), false);
});

test('a token signed with a different secret fails verification', () => {
  const token = signSession(SECRET, 3600);
  assert.equal(verifySession(token, 'wrong-secret'), false);
});
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `node --test tests/session.test.js`
Expected: FAIL — `Cannot find module '../lib/session.js'`

- [ ] **Step 3: Write the implementation**

```js
// lib/session.js
import crypto from 'node:crypto';

export function signSession(secret, ttlSeconds) {
  const expiresAt = Date.now() + ttlSeconds * 1000;
  const payload = String(expiresAt);
  const signature = crypto.createHmac('sha256', secret).update(payload).digest('hex');
  return `${payload}.${signature}`;
}

export function verifySession(token, secret) {
  if (!token || typeof token !== 'string' || !token.includes('.')) return false;
  const [payload, signature] = token.split('.');
  const expectedSignature = crypto.createHmac('sha256', secret).update(payload).digest('hex');

  const sigBuffer = Buffer.from(signature || '', 'hex');
  const expectedBuffer = Buffer.from(expectedSignature, 'hex');
  if (sigBuffer.length !== expectedBuffer.length || !crypto.timingSafeEqual(sigBuffer, expectedBuffer)) {
    return false;
  }

  const expiresAt = Number(payload);
  return Number.isFinite(expiresAt) && Date.now() < expiresAt;
}
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `node --test tests/session.test.js`
Expected: PASS — 4 tests passing.

- [ ] **Step 5: Commit**

```bash
git add lib/session.js tests/session.test.js
git commit -m "feat: HMAC-signed admin session tokens with tests"
```

---

## Task 16: Admin login and leads-listing API endpoints

**Files:**
- Create: `api/admin-login.js`
- Create: `api/admin-leads.js`

- [ ] **Step 1: Create `api/admin-login.js`**

The length check before `timingSafeEqual` is required because that function throws on mismatched buffer lengths. Comparing lengths first leaks only the password length, which is acceptable here.

```js
import crypto from 'node:crypto';
import { signSession } from '../lib/session.js';

const SESSION_TTL_SECONDS = 60 * 60 * 8; // 8 hours

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.status(405).json({ ok: false });
    return;
  }

  const { password } = req.body || {};
  const expected = Buffer.from(process.env.ADMIN_PASSWORD || '');
  const provided = Buffer.from(String(password || ''));

  const isValid = expected.length > 0
    && provided.length === expected.length
    && crypto.timingSafeEqual(provided, expected);

  if (!isValid) {
    res.status(401).json({ ok: false, error: 'Contraseña incorrecta' });
    return;
  }

  const token = signSession(process.env.ADMIN_SESSION_SECRET, SESSION_TTL_SECONDS);
  res.setHeader('Set-Cookie', `bd_admin_session=${token}; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=${SESSION_TTL_SECONDS}`);
  res.status(200).json({ ok: true });
}
```

- [ ] **Step 2: Create `api/admin-leads.js`**

```js
import { verifySession } from '../lib/session.js';
import { getSupabaseClient } from '../lib/db.js';

function getCookie(req, name) {
  const header = req.headers.cookie || '';
  const match = header.split(';').map(p => p.trim()).find(p => p.startsWith(`${name}=`));
  return match ? match.slice(name.length + 1) : null;
}

export default async function handler(req, res) {
  const token = getCookie(req, 'bd_admin_session');
  if (!verifySession(token, process.env.ADMIN_SESSION_SECRET)) {
    res.status(401).json({ ok: false, error: 'No autenticado' });
    return;
  }

  if (req.method === 'GET') {
    const supabase = getSupabaseClient();
    const { data, error } = await supabase
      .from('biodesign_leads')
      .select('*')
      .order('created_at', { ascending: false });
    if (error) {
      res.status(500).json({ ok: false, error: error.message });
      return;
    }
    res.status(200).json({ ok: true, leads: data });
    return;
  }

  if (req.method === 'PATCH') {
    const { id, status } = req.body || {};
    const supabase = getSupabaseClient();
    const { error } = await supabase.from('biodesign_leads').update({ status }).eq('id', id);
    if (error) {
      res.status(500).json({ ok: false, error: error.message });
      return;
    }
    res.status(200).json({ ok: true });
    return;
  }

  res.status(405).json({ ok: false });
}
```

- [ ] **Step 3: Commit**

```bash
git add api/admin-login.js api/admin-leads.js
git commit -m "feat: admin login and leads-listing API endpoints"
```

---

## Task 17: Admin panel frontend (`admin/index.html` + `assets/js/admin.js`)

**Files:**
- Create: `admin/index.html`
- Create: `assets/js/admin.js`

- [ ] **Step 1: Create `assets/js/admin.js`**

```js
async function loadLeads() {
  const res = await fetch('/api/admin-leads');
  if (res.status === 401) {
    document.getElementById('loginView').style.display = '';
    document.getElementById('leadsView').style.display = 'none';
    return;
  }
  const data = await res.json();
  renderLeads(data.leads);
  document.getElementById('loginView').style.display = 'none';
  document.getElementById('leadsView').style.display = '';
}

function renderLeads(leads) {
  const tbody = document.getElementById('leadsBody');
  tbody.innerHTML = leads.map(lead => `
    <tr>
      <td>${new Date(lead.created_at).toLocaleString('es-ES')}</td>
      <td>${lead.name}</td>
      <td>${lead.phone}</td>
      <td>${lead.email || '-'}</td>
      <td>${lead.pool_type}</td>
      <td>${lead.location}</td>
      <td>
        <select data-id="${lead.id}" class="status-select">
          <option value="nuevo" ${lead.status === 'nuevo' ? 'selected' : ''}>Nuevo</option>
          <option value="contactado" ${lead.status === 'contactado' ? 'selected' : ''}>Contactado</option>
          <option value="cerrado" ${lead.status === 'cerrado' ? 'selected' : ''}>Cerrado</option>
        </select>
      </td>
    </tr>
  `).join('');

  tbody.querySelectorAll('.status-select').forEach(select => {
    select.addEventListener('change', async () => {
      await fetch('/api/admin-leads', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: select.dataset.id, status: select.value }),
      });
    });
  });
}

document.getElementById('loginForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const password = document.getElementById('passwordInput').value;
  const res = await fetch('/api/admin-login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ password }),
  });
  if (res.ok) {
    loadLeads();
  } else {
    document.getElementById('loginError').textContent = 'Contraseña incorrecta';
  }
});

loadLeads();
```

- [ ] **Step 2: Create `admin/index.html`**

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Panel de leads | Bio.design Tenerife</title>
  <meta name="robots" content="noindex">
  <link rel="stylesheet" href="../assets/css/tokens.css">
  <link rel="stylesheet" href="../assets/css/main.css">
  <link rel="stylesheet" href="../assets/css/components.css">
</head>
<body>
  <div class="container" style="padding-top:48px;">
    <h1>Panel de leads</h1>

    <div id="loginView" class="card" style="max-width:360px;">
      <form id="loginForm">
        <label>Contraseña<br><input type="password" id="passwordInput" class="quiz-input" required></label>
        <p id="loginError" style="color:#e88;"></p>
        <button type="submit" class="btn btn-primary">Entrar</button>
      </form>
    </div>

    <div id="leadsView" style="display:none;">
      <table style="width:100%; border-collapse:collapse;">
        <thead>
          <tr style="text-align:left; border-bottom:1px solid rgba(255,255,255,.1);">
            <th>Fecha</th><th>Nombre</th><th>Teléfono</th><th>Email</th><th>Tipo</th><th>Ubicación</th><th>Estado</th>
          </tr>
        </thead>
        <tbody id="leadsBody"></tbody>
      </table>
    </div>
  </div>
  <script src="../assets/js/admin.js"></script>
</body>
</html>
```

- [ ] **Step 3: Commit**

```bash
git add admin/index.html assets/js/admin.js
git commit -m "feat: admin panel frontend"
```

---

## Task 18: Static-page smoke tests

Lightweight regression guard: every shipped HTML page must contain the territorial exclusivity notice and a canonical tag, so a future edit can't silently drop them.

**Files:**
- Test: `tests/smoke-pages.test.js`

- [ ] **Step 1: Write the test**

```js
// tests/smoke-pages.test.js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

const PUBLIC_PAGES = [
  'index.html', 'tecnologia.html', 'quienes-somos.html',
  'realizaciones.html', 'contacto.html',
];

for (const page of PUBLIC_PAGES) {
  test(`${page} contains the territorial exclusivity badge`, () => {
    const html = fs.readFileSync(page, 'utf8');
    assert.ok(html.includes('Santa Cruz de Tenerife'), `${page} is missing the exclusivity notice`);
  });

  test(`${page} has a canonical link tag`, () => {
    const html = fs.readFileSync(page, 'utf8');
    assert.ok(html.includes('rel="canonical"'), `${page} is missing a canonical tag`);
  });
}

test('quienes-somos.html explicitly states the concession does not cover other provinces', () => {
  const html = fs.readFileSync('quienes-somos.html', 'utf8');
  assert.ok(html.includes('otras provincias'), 'missing the other-provinces disclaimer');
});
```

- [ ] **Step 2: Run the test to verify current pages pass**

Run: `node --test tests/smoke-pages.test.js`
Expected: PASS — confirms Tasks 5-9 already satisfy these invariants. If any page fails, fix that page's content (don't weaken the test) before proceeding.

- [ ] **Step 3: Commit**

```bash
git add tests/smoke-pages.test.js
git commit -m "test: smoke tests guarding exclusivity notice and canonical tags"
```

---

## Task 19: Final full test run and manual verification

**Files:** none (verification only)

- [ ] **Step 1: Run the full test suite**

Run: `npm test`
Expected: all tests in `tests/` pass (validators, session, leads-handler, smoke-pages).

- [ ] **Step 2: Manual browser verification**

Open `index.html` directly in a browser (or serve the folder) and confirm:
- The hero emblem rotates continuously and the sparkle background is visible.
- Navigation reaches every page without 404s.
- `cuestionario.html` steps through all 3 steps and shows the success state (requires `vercel dev` running locally with a real or temporary Supabase project for the actual submit to succeed — otherwise confirm the step navigation and validation errors work, and note the submit step needs the deployed backend to fully verify).
- The exclusivity badge is visible in the footer and header sub-line on every page.

- [ ] **Step 3: Commit any fixes found during manual verification, then do a final status check**

Run: `git status`
Expected: clean working tree, all work committed.

---

## Task 20: Deployment notes for Josep (manual, outside this session)

Document remaining manual steps Josep must do himself (no credentials available in this session):

1. Run `supabase/schema.sql` in the Supabase SQL editor for the existing project used by the Apavi Green chatbot.
2. Register the real domain and connect it in the Vercel project settings once created.
3. Create a new Vercel project pointing at this repo, and set the environment variables from `.env.example` (`SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `RESEND_API_KEY`, `RESEND_FROM`, `NOTIFICATION_EMAIL`, `ADMIN_PASSWORD`, `ADMIN_SESSION_SECRET`, and optionally `TELEGRAM_BOT_TOKEN` / `OPERATOR_TELEGRAM_CHAT_ID`).
4. Push this repo to a new GitHub repository and connect it to the Vercel project for auto-deploys.
5. Swap the placeholder `biodesign-tenerife.com` canonical URLs in every page's `<head>` for the real domain once registered.

This task has no code steps — it is a checklist for Josep to execute once he has the relevant account access.
