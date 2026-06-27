import { apiRequest } from "./api.js";

const historyContainer = document.getElementById("history");

async function loadHistory() {
  if (!historyContainer) return;
  try {
    const history = await apiRequest("/history");
    historyContainer.innerHTML = history.map((item) => `
      <div class="glass card">
        <h3>${item.filename}</h3>
        <p>${new Date(item.created_at).toLocaleString()}</p>
        <small>${item.generated_types.join(", ")}</small>
      </div>
    `).join("") || "No revision history yet.";
  } catch (error) {
    historyContainer.textContent = error.message;
  }
}

loadHistory();
