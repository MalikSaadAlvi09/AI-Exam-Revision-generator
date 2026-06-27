const API_BASE = localStorage.getItem('apiBase') || 'http://localhost:8000';

function authHeaders() {
  const token = localStorage.getItem('token');
  if (!token) return {};
  return { Authorization: 'Bearer ' + token };
}

async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
      ...authHeaders(),
    },
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(error.detail || 'Request failed');
  }
  return response.json();
}

window.API = { apiRequest, API_BASE };
