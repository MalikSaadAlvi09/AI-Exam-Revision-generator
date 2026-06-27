function applyTheme(mode) {
  document.documentElement.dataset.theme = mode;
  localStorage.setItem('theme', mode);
}

document.addEventListener('DOMContentLoaded', () => {
  applyTheme(localStorage.getItem('theme') || 'dark');
  const toggles = document.querySelectorAll('[data-theme-toggle]');
  toggles.forEach((btn) => btn.addEventListener('click', () => {
    const next = (localStorage.getItem('theme') || 'dark') === 'dark' ? 'light' : 'dark';
    applyTheme(next);
  }));
});
