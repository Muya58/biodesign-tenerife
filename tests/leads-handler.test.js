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
