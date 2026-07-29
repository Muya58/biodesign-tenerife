# Canonical header/footer snippet

No templating engine exists (static site, no build step), so the header and
footer below are copy-pasted verbatim into every page. This file is the
reference copy — it is not shipped as part of the site itself.

The nav links and the footer are pasted verbatim into every page. Pages
inside a subdirectory (e.g. `admin/`) need `../` prefixes on the asset and
link paths (e.g. `../assets/img/emblem.svg`, `../index.html`).

## Header

```html
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
```

## Footer

```html
<footer class="site-footer">
  <div class="exclusivity-badge">Concesionario oficial Bio.design &middot; Provincia de Santa Cruz de Tenerife</div>
  <p>Apavi Green &middot; Concesionario Oficial Bio.design S.p.A. para la provincia de Santa Cruz de Tenerife.</p>
  <p>
    <a href="aviso-legal.html">Aviso legal</a> &middot;
    <a href="privacidad.html">Privacidad</a> &middot;
    <a href="cookies.html">Cookies</a>
  </p>
</footer>
```
