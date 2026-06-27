import { apiRequest, uploadFile } from "./api.js";

const uploadInput = document.getElementById("upload_file");
const uploadBtn = document.getElementById("upload_btn");
const generateBtn = document.getElementById("generate_btn");
const pastedText = document.getElementById("pasted_text");
const output = document.getElementById("output");

let uploadId = null;

uploadBtn?.addEventListener("click", async () => {
  const file = uploadInput.files?.[0];
  if (!file) {
    output.textContent = "Select a file first.";
    return;
  }

  try {
    const result = await uploadFile(file);
    uploadId = result.upload_id;
    output.textContent = `Uploaded ${result.filename}. Upload ID: ${uploadId}`;
  } catch (error) {
    output.textContent = error.message;
  }
});

generateBtn?.addEventListener("click", async () => {
  try {
    const body = uploadId
      ? { upload_id: uploadId }
      : { raw_text: pastedText.value };

    const result = await apiRequest("/generate", {
      method: "POST",
      body: JSON.stringify(body),
    });

    localStorage.setItem("latestUploadId", String(result.upload_id));
    localStorage.setItem("latestOutputs", JSON.stringify(result.outputs));
    output.textContent = JSON.stringify(result.outputs, null, 2);
  } catch (error) {
    output.textContent = error.message;
  }
});
