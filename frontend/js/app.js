document.addEventListener('DOMContentLoaded', () => {
  const registerForm = document.getElementById('register-form');
  const loginForm = document.getElementById('login-form');

  if (registerForm) {
    registerForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const formData = new FormData(registerForm);
      const payload = {
        full_name: formData.get('full_name'),
        email: formData.get('email'),
        password: formData.get('password'),
      };
      const data = await API.apiRequest('/register', { method: 'POST', body: JSON.stringify(payload) });
      localStorage.setItem('token', data.access_token);
      window.location.href = '/frontend/dashboard.html';
    });
  }

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const formData = new FormData(loginForm);
      const payload = { email: formData.get('email'), password: formData.get('password') };
      const data = await API.apiRequest('/login', { method: 'POST', body: JSON.stringify(payload) });
      localStorage.setItem('token', data.access_token);
      window.location.href = '/frontend/dashboard.html';
    });
  }
});
