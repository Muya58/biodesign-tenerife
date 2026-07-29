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
