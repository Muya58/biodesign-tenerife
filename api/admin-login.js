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
