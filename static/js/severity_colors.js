// severity_colors.js — dark mode aware
const SEVERITY_COLORS = {
  light: {
    low:       { bg: '#F0FDF4', text: '#16A34A', border: '#16A34A', label: 'Low' },
    moderate:  { bg: '#FFFBEB', text: '#D97706', border: '#D97706', label: 'Moderate' },
    urgent:    { bg: '#FFF7ED', text: '#EA580C', border: '#EA580C', label: 'Urgent' },
    emergency: { bg: '#FEF2F2', text: '#DC2626', border: '#DC2626', label: 'Emergency' },
  },
  dark: {
    low:       { bg: '#052e16', text: '#4ade80', border: '#16A34A', label: 'Low' },
    moderate:  { bg: '#2d1a00', text: '#fbbf24', border: '#D97706', label: 'Moderate' },
    urgent:    { bg: '#2d1500', text: '#fb923c', border: '#EA580C', label: 'Urgent' },
    emergency: { bg: '#2d0000', text: '#f87171', border: '#DC2626', label: 'Emergency' },
  }
};

function applySeverityColors() {
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  const palette = isDark ? SEVERITY_COLORS.dark : SEVERITY_COLORS.light;

  document.querySelectorAll('.severity-badge').forEach(badge => {
    const sev = badge.dataset.severity;
    if (palette[sev]) {
      const { bg, text, border, label } = palette[sev];
      badge.style.backgroundColor = bg;
      badge.style.color            = text;
      badge.style.border           = `1px solid ${border}`;
      badge.textContent            = label;
    }
  });
}

document.addEventListener('DOMContentLoaded', applySeverityColors);

// Re-apply when theme changes (the accessibility.js toggles data-theme)
const observer = new MutationObserver((mutations) => {
  mutations.forEach(m => {
    if (m.attributeName === 'data-theme') applySeverityColors();
  });
});
observer.observe(document.documentElement, { attributes: true });