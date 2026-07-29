const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const PHONE_RE = /^\+?[0-9\s-]{7,15}$/;

export function validateLead(payload = {}) {
  const errors = {};

  if (!payload.name || !String(payload.name).trim()) {
    errors.name = 'El nombre es obligatorio.';
  }
  if (!payload.phone || !PHONE_RE.test(String(payload.phone).trim())) {
    errors.phone = 'Introduce un teléfono válido.';
  }
  if (payload.email && !EMAIL_RE.test(String(payload.email).trim())) {
    errors.email = 'Introduce un email válido.';
  }
  if (!payload.poolType) {
    errors.poolType = 'Selecciona el tipo de piscina.';
  }
  if (!payload.location || !String(payload.location).trim()) {
    errors.location = 'Indica la ubicación aproximada.';
  }
  if (payload.privacyAccepted !== true) {
    errors.privacyAccepted = 'Debes aceptar la política de privacidad.';
  }

  return { valid: Object.keys(errors).length === 0, errors };
}
