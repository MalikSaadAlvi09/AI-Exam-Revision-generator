
document.addEventListener('DOMContentLoaded', async () => {
  const wrapper = document.getElementById('content-list');
  if (!wrapper) return;
  try {
    const data = await API.apiRequest(window.CONTENT_TYPE || '/summary');
    if (!data.items || !data.items.length) {
      wrapper.innerHTML = '<p class="text-slate-300">No generated content available yet. Upload notes to begin.</p>';
      return;
    }
    wrapper.innerHTML = data.items.map((item) => `
      <article class="glass-card rounded-xl p-4">
        <div class="text-sm text-slate-400 mb-2">${item.upload_filename} • ${new Date(item.created_at).toLocaleString()}</div>
        <pre class="whitespace-pre-wrap text-sm leading-6">${JSON.stringify(item.content, null, 2)}</pre>
      </article>`).join('');
  } catch (error) {
    wrapper.innerHTML = `<p>${error.message}</p>`;
  }
});
