/**
 * Capturas de página completa con emulación real de dispositivo.
 *
 * Por qué no basta `chrome --headless --screenshot`:
 *   - En Windows el headless fija el ancho mínimo de ventana en 500px e ignora
 *     `--window-size` por debajo: maqueta a 500 y recorta la imagen al ancho pedido,
 *     lo que simula recortes de texto que en el navegador real no existen.
 *   - Solo captura el viewport, no la página entera.
 *
 * Aquí se habla el protocolo DevTools directamente (Node 22+ trae WebSocket global),
 * con Emulation.setDeviceMetricsOverride para emular el móvil de verdad y
 * captureBeyondViewport para la página completa.
 *
 * Uso:  node scripts/screenshots.mjs <carpeta-salida> [puerto-servidor]
 * Requiere un servidor estático sirviendo la raíz del proyecto.
 */

import { spawn } from 'node:child_process';
import fs from 'node:fs/promises';
import path from 'node:path';

const OUT = process.argv[2] || 'capturas';
const PORT = process.argv[3] || '4173';
const BASE = `http://localhost:${PORT}`;
const CDP_PORT = 9333;

const PAGES = ['index', 'quienes-somos', 'tecnologia', 'realizaciones', 'contacto', 'cuestionario'];
const DEVICES = [
  { name: 'escritorio', width: 1440, height: 900, scale: 1, mobile: false },
  { name: 'movil', width: 390, height: 844, scale: 2, mobile: true },
];

const CHROME_CANDIDATES = [
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
];

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function findChrome() {
  for (const candidate of CHROME_CANDIDATES) {
    try {
      await fs.access(candidate);
      return candidate;
    } catch {}
  }
  throw new Error('No encuentro Chrome ni Edge');
}

/** Cliente CDP mínimo sobre el WebSocket nativo de Node. */
class CDP {
  constructor(ws) {
    this.ws = ws;
    this.id = 0;
    this.pending = new Map();
    this.ws.addEventListener('message', (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.id && this.pending.has(msg.id)) {
        const { resolve, reject } = this.pending.get(msg.id);
        this.pending.delete(msg.id);
        msg.error ? reject(new Error(msg.error.message)) : resolve(msg.result);
      }
    });
  }

  static async connect(url) {
    const ws = new WebSocket(url);
    await new Promise((resolve, reject) => {
      ws.addEventListener('open', resolve, { once: true });
      ws.addEventListener('error', reject, { once: true });
    });
    return new CDP(ws);
  }

  send(method, params = {}) {
    const id = ++this.id;
    this.ws.send(JSON.stringify({ id, method, params }));
    return new Promise((resolve, reject) => this.pending.set(id, { resolve, reject }));
  }
}

async function waitForServer() {
  for (let i = 0; i < 20; i++) {
    try {
      const res = await fetch(`${BASE}/index.html`);
      if (res.ok) return;
    } catch {}
    await sleep(400);
  }
  throw new Error(`No hay servidor en ${BASE}`);
}

async function main() {
  await waitForServer();
  await fs.mkdir(OUT, { recursive: true });
  const chrome = await findChrome();

  const proc = spawn(chrome, [
    '--headless=new',
    '--disable-gpu',
    `--remote-debugging-port=${CDP_PORT}`,
    '--no-first-run',
    '--user-data-dir=' + path.join(OUT, '.chrome-profile'),
    'about:blank',
  ], { stdio: 'ignore' });

  let wsUrl;
  for (let i = 0; i < 30; i++) {
    try {
      const res = await fetch(`http://127.0.0.1:${CDP_PORT}/json/version`);
      wsUrl = (await res.json()).webSocketDebuggerUrl;
      if (wsUrl) break;
    } catch {}
    await sleep(400);
  }
  if (!wsUrl) {
    proc.kill();
    throw new Error('Chrome no expuso el puerto de depuración');
  }

  const browser = await CDP.connect(wsUrl);
  const { targetId } = await browser.send('Target.createTarget', { url: 'about:blank' });
  const tabWs = `ws://127.0.0.1:${CDP_PORT}/devtools/page/${targetId}`;
  const page = await CDP.connect(tabWs);
  await page.send('Page.enable');

  let count = 0;
  for (const device of DEVICES) {
    console.log(`${device.name} (${device.width}x${device.height}, dpr ${device.scale}):`);
    await page.send('Emulation.setDeviceMetricsOverride', {
      width: device.width,
      height: device.height,
      deviceScaleFactor: device.scale,
      mobile: device.mobile,
    });

    for (const name of PAGES) {
      await page.send('Page.navigate', { url: `${BASE}/${name}.html` });
      await sleep(2200); // fuentes, imágenes y lazy-loading

      // Forzar la carga de las imágenes lazy: si no, salen huecos en la captura.
      await page.send('Runtime.evaluate', {
        expression: `[...document.images].forEach(i => i.loading = 'eager');`,
      });
      await sleep(1200);

      const { data } = await page.send('Page.captureScreenshot', {
        format: 'png',
        captureBeyondViewport: true,
      });
      const file = path.join(OUT, `${name}-${device.name}.png`);
      await fs.writeFile(file, Buffer.from(data, 'base64'));
      const kb = Math.round((await fs.stat(file)).size / 1024);
      console.log(`  ${name.padEnd(16)} ${kb} KB`);
      count++;
    }
  }

  await browser.send('Target.closeTarget', { targetId });
  proc.kill();
  console.log(`\nListo: ${count} capturas en ${OUT}/`);
}

main().catch((err) => {
  console.error('ERROR:', err.message);
  process.exit(1);
});
