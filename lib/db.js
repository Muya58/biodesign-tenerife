import { createClient } from '@supabase/supabase-js';

let client;

export function getSupabaseClient() {
  if (!client) {
    client = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);
  }
  return client;
}

export async function insertLead(supabase, lead) {
  const { data, error } = await supabase
    .from('biodesign_leads')
    .insert({
      pool_type: lead.poolType,
      size_m2: lead.sizeM2 ? Number(lead.sizeM2) : null,
      location: lead.location,
      budget_range: lead.budgetRange || null,
      name: lead.name,
      phone: lead.phone,
      email: lead.email || null,
    })
    .select()
    .single();
  if (error) throw error;
  return data;
}
