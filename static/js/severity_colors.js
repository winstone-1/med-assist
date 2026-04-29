// severity_colors.js
const SEVERITY_COLORS = {
  low:       { bg: '#F0FDF4', text: '#16A34A', border: '#16A34A', label: 'Low' },
  moderate:  { bg: '#FFFBEB', text: '#D97706', border: '#D97706', label: 'Moderate' },
  urgent:    { bg: '#FFF7ED', text: '#EA580C', border: '#EA580C', label: 'Urgent' },
  emergency: { bg: '#FEF2F2', text: '#DC2626', border: '#DC2626', label: 'Emergency' },
};

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.severity-badge').forEach(badge => {
    const sev = badge.dataset.severity;
    if (SEVERITY_COLORS[sev]) {
      const { bg, text, border, label } = SEVERITY_COLORS[sev];
      badge.style.backgroundColor = bg;
      badge.style.color            = text;
      badge.style.border           = `1px solid ${border}`;
      badge.textContent             = label;
    }
  });
});