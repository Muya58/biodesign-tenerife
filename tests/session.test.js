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
