import { apiRequest } from "./api.js";

const authForm = document.getElementById("auth-form");
const modeSwitcher = document.getElementById("mode-switch");
const statusText = document.getElementById("status");

if (authForm) {
  let mode = "login";

  modeSwitcher?.addEventListener("click", () => {
    mode = mode === "login" ? "register" : "login";
    modeSwitcher.textContent = mode === "login" ? "Create account" : "Use login";
    authForm.querySelector("button").textContent = mode === "login" ? "Login" : "Register";
    document.getElementById("full_name_row").style.display = mode === "register" ? "block" : "none";
  });

  authForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const fullName = document.getElementById("full_name").value;

    const payload = mode === "register"
      ? { email, password, full_name: fullName }
      : { email, password };

    try {
      const data = await apiRequest(`/${mode}`, {
        method: "POST",
        body: JSON.stringify(payload),
      });
      localStorage.setItem("token", data.access_token);
      window.location.href = "upload.html";
    } catch (error) {
      statusText.textContent = error.message;
    }
  });
}
