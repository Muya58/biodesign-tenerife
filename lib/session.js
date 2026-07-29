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
