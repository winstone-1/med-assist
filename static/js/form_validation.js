// form_validation.js
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('symptomForm');
  if (!form) return;

  form.addEventListener('change', () => {
    const existing = form.querySelector('.validation-alert');
    if (existing) existing.remove();
  });

  form.addEventListener('submit', e => {
    const inputs     = form.querySelectorAll('input[type=checkbox], input[type=radio]');
    const hasChecked = [...inputs].some(i => i.checked);

    if (inputs.length > 0 && !hasChecked) {
      e.preventDefault();
      const alert = document.createElement('div');
      alert.className = 'alert alert-warning validation-alert mt-2';
      alert.textContent = 'Please select at least one option before continuing.';
      form.prepend(alert);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  });
});