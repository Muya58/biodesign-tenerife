const STEPS = ['poolType', 'details', 'contact'];
let currentStep = 0;
const state = { poolType: '', sizeM2: '', location: '', budgetRange: '', name: '', phone: '', email: '', privacyAccepted: false };

function showStep(index) {
  document.querySelectorAll('.quiz-step').forEach((el, i) => {
    el.style.display = i === index ? '' : 'none';
  });
  document.getElementById('quizProgress').style.width = `${((index + 1) / STEPS.length) * 100}%`;
  document.getElementById('prevBtn').style.visibility = index === 0 ? 'hidden' : 'visible';
  document.getElementById('nextBtn').textContent = index === STEPS.length - 1 ? 'Enviar' : 'Siguiente';
}

function collectStepInputs() {
  document.querySelectorAll('[data-field]').forEach(el => {
    if (el.type === 'checkbox') state[el.dataset.field] = el.checked;
    else if (el.type === 'radio') { if (el.checked) state[el.dataset.field] = el.value; }
    else state[el.dataset.field] = el.value;
  });
}

async function submitLead() {
  const res = await fetch('/api/leads', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(state),
  });
  const data = await res.json();
  const form = document.getElementById('quizForm');
  if (res.ok) {
    // Build the success view with text nodes so the user's own input is never
    // interpreted as markup.
    form.innerHTML = '';
    const wrap = document.createElement('div');
    wrap.className = 'quiz-success';
    const h = document.createElement('h2');
    h.textContent = `¡Gracias, ${state.name}!`;
    const p = document.createElement('p');
    p.textContent = 'Hemos recibido tu solicitud. Un técnico de Apavi Green se pondrá en contacto contigo en menos de 24 horas.';
    wrap.append(h, p);
    form.append(wrap);
  } else {
    alert(Object.values(data.errors || { general: 'No se pudo enviar el formulario. Inténtalo de nuevo.' }).join('\n'));
  }
}

document.getElementById('nextBtn').addEventListener('click', () => {
  collectStepInputs();
  if (currentStep < STEPS.length - 1) {
    currentStep += 1;
    showStep(currentStep);
  } else {
    submitLead();
  }
});

document.getElementById('prevBtn').addEventListener('click', () => {
  if (currentStep > 0) {
    currentStep -= 1;
    showStep(currentStep);
  }
});

showStep(currentStep);
