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
