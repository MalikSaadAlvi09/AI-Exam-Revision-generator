document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('file-input');
  const form = document.getElementById('upload-form');
  const status = document.getElementById('upload-status');

  if (!form || !input) return;

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const file = input.files[0];
    if (!file) return;

    const body = new FormData();
    body.append('file', file);

    status.textContent = 'Uploading and extracting content...';

    const token = localStorage.getItem('token') || '';
    const response = await fetch(`${API.API_BASE}/upload`, {
      method: 'POST',
      body,
      headers: { Authorization: 'Bearer ' + token },
    });

    if (!response.ok) {
      const error = await response.json();
      status.textContent = error.detail || 'Upload failed';
      return;
    }

    const data = await response.json();
    localStorage.setItem('latestUploadId', data.upload_id);
    status.textContent = `Uploaded ${data.filename}. Generating revision assets...`;

    await API.apiRequest('/generate', {
      method: 'POST',
      body: JSON.stringify({ upload_id: data.upload_id }),
    });

    status.textContent = 'Generation complete. Open dashboard to review outputs.';
  });
});
