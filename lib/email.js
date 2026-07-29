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
