
async function loadProfile() {
  const data = await API.apiRequest('/profile');
  const form = document.getElementById('profile-form');
  form.full_name.value = data.full_name;
  form.dark_mode.checked = data.dark_mode;
}

document.addEventListener('DOMContentLoaded', async () => {
  const form = document.getElementById('profile-form');
  const status = document.getElementById('profile-status');
  if (!form) return;
  await loadProfile();
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const payload = { full_name: form.full_name.value, dark_mode: form.dark_mode.checked };
    await API.apiRequest('/profile', { method: 'PUT', body: JSON.stringify(payload) });
    status.textContent = 'Profile updated successfully.';
  });
});
