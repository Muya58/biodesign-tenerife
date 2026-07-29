import { verifySession } from '../lib/session.js';
import { getSupabaseClient } from '../lib/db.js';

function getCookie(req, name) {
  const header = req.headers.cookie || '';
  const match = header.split(';').map(p => p.trim()).find(p => p.startsWith(`${name}=`));
  return match ? match.slice(name.length + 1) : null;
}

export default async function handler(req, res) {
  const token = getCookie(req, 'bd_admin_session');
  if (!verifySession(token, process.env.ADMIN_SESSION_SECRET)) {
    res.status(401).json({ ok: false, error: 'No autenticado' });
    return;
  }

  if (req.method === 'GET') {
    const supabase = getSupabaseClient();
    const { data, error } = await supabase
      .from('biodesign_leads')
      .select('*')
      .order('created_at', { ascending: false });
    if (error) {
      res.status(500).json({ ok: false, error: error.message });
      return;
    }
    res.status(200).json({ ok: true, leads: data });
    return;
  }

  if (req.method === 'PATCH') {
    const { id, status } = req.body || {};
    const supabase = getSupabaseClient();
    const { error } = await supabase.from('biodesign_leads').update({ status }).eq('id', id);
    if (error) {
      res.status(500).json({ ok: false, error: error.message });
      return;
    }
    res.status(200).json({ ok: true });
    return;
  }

  res.status(405).json({ ok: false });
}
