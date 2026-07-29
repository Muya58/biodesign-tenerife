function escapeHtml(value) {
  if (value === null || value === undefined) return '';
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

async function loadLeads() {
  const res = await fetch('/api/admin-leads');
  if (res.status === 401) {
    document.getElementById('loginView').style.display = '';
    document.getElementById('leadsView').style.display = 'none';
    return;
  }
  const data = await res.json();
  renderLeads(data.leads);
  document.getElementById('loginView').style.display = 'none';
  document.getElementById('leadsView').style.display = '';
}

function renderLeads(leads) {
  const tbody = document.getElementById('leadsBody');
  tbody.innerHTML = leads.map(lead => `
    <tr>
      <td>${escapeHtml(new Date(lead.created_at).toLocaleString('es-ES'))}</td>
      <td>${escapeHtml(lead.name)}</td>
      <td>${escapeHtml(lead.phone)}</td>
      <td>${escapeHtml(lead.email) || '-'}</td>
      <td>${escapeHtml(lead.pool_type)}</td>
      <td>${escapeHtml(lead.location)}</td>
      <td>
        <select data-id="${escapeHtml(lead.id)}" class="status-select">
          <option value="nuevo" ${lead.status === 'nuevo' ? 'selected' : ''}>Nuevo</option>
          <option value="contactado" ${lead.status === 'contactado' ? 'selected' : ''}>Contactado</option>
          <option value="cerrado" ${lead.status === 'cerrado' ? 'selected' : ''}>Cerrado</option>
        </select>
      </td>
    </tr>
  `).join('');

  tbody.querySelectorAll('.status-select').forEach(select => {
    select.addEventListener('change', async () => {
      await fetch('/api/admin-leads', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: select.dataset.id, status: select.value }),
      });
    });
  });
}

document.getElementById('loginForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const password = document.getElementById('passwordInput').value;
  const res = await fetch('/api/admin-login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ password }),
  });
  if (res.ok) {
    loadLeads();
  } else {
    document.getElementById('loginError').textContent = 'Contraseña incorrecta';
  }
});

loadLeads();
