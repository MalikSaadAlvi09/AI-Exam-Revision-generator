async function loadProfile() {
  const profile = await API.apiRequest('/profile');
  const target = document.getElementById('welcome');
  if (target) target.textContent = `Welcome back, ${profile.full_name}`;
}

async function loadHistory() {
  const history = await API.apiRequest('/history');
  const list = document.getElementById('history-list');
  if (!list) return;
  list.innerHTML = history.slice(0, 8).map((entry) => `
    <li class="p-3 rounded-xl glass-card flex items-center justify-between">
      <span>${entry.upload_filename}</span>
      <span class="badge">${entry.content_type}</span>
    </li>
  `).join('');
}

async function drawStats() {
  const mcqs = await API.apiRequest('/mcqs');
  const flashcards = await API.apiRequest('/flashcards');
  const summary = await API.apiRequest('/summary');
  const ctx = document.getElementById('statsChart');
  if (!ctx || !window.Chart) return;
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['MCQs', 'Flashcards', 'Summaries'],
      datasets: [{
        label: 'Generated Sets',
        data: [mcqs.items.length, flashcards.items.length, summary.items.length],
        backgroundColor: ['#06b6d4', '#8b5cf6', '#22d3ee'],
        borderRadius: 8,
      }],
    },
  });
}

document.addEventListener('DOMContentLoaded', async () => {
  await Promise.allSettled([loadProfile(), loadHistory(), drawStats()]);
});
