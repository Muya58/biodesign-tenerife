// Rotation is pure CSS (see .hero-emblem in components.css). This only
// honours a runtime change of the reduced-motion preference.
const motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');

function applyMotionPreference() {
  const emblem = document.querySelector('.hero-emblem');
  if (!emblem) return;
  emblem.style.animationPlayState = motionQuery.matches ? 'paused' : 'running';
}

applyMotionPreference();
motionQuery.addEventListener('change', applyMotionPreference);
