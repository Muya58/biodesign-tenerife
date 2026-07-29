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
