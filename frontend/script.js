// ...existing code...
let mediaRecorder;
let audioChunks = [];

document.addEventListener("DOMContentLoaded", () => {
  const recordBtn = document.getElementById("recordBtn");
  const stopBtn = document.getElementById("stopBtn");
  const uploadBtn = document.getElementById("uploadBtn");
  const fileInput = document.getElementById("fileInput");
  const status = document.getElementById("status");
  const result = document.getElementById("result");

  function displayResult(data) {
    status.innerText = "✅ Upload complete.";
    result.innerHTML = `
      <strong>Filename:</strong> ${data.filename}<br>
      <strong>Parkinson Detected:</strong> ${data.parkinson_detected ? "✅ Yes" : "❌ No"}<br>
      <strong>Confidence:</strong> ${Math.round((data.confidence || 0) * 100)}%<br>
      <strong>Features:</strong>
      <ul>
        ${Object.entries(data.features || {})
          .map(([key, value]) => `<li>${key}: ${Number(value).toFixed(4)}</li>`)
          .join("")}
      </ul>
    `;
  }

  // Record / Stop handlers (unchanged logic, explicit button types prevent implicit submit)
  recordBtn.addEventListener("click", async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream);
      audioChunks = [];

      mediaRecorder.ondataavailable = e => audioChunks.push(e.data);

      mediaRecorder.onstop = async () => {
        const blob = new Blob(audioChunks, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append("file", blob, "voice.wav");

        status.innerText = "Uploading recorded voice...";

        try {
          const response = await fetch("http://127.0.0.1:8000/upload/", {
            method: "POST",
            body: formData
          });

          if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
          }

          const resultData = await response.json();
          displayResult(resultData);
        } catch (error) {
          console.error("Upload failed:", error);
          status.innerText = "❌ Upload failed.";
        }
      };

      mediaRecorder.start();
      recordBtn.disabled = true;
      stopBtn.disabled = false;
      status.innerText = "🎙️ Recording...";
    } catch (err) {
      console.error("Microphone access denied:", err);
      status.innerText = "⚠️ Microphone access denied.";
    }
  });

  stopBtn.addEventListener("click", () => {
    if (mediaRecorder && mediaRecorder.state === "recording") {
      mediaRecorder.stop();
      stopBtn.disabled = true;
      recordBtn.disabled = false;
    }
  });

  // Upload file — explicit listener + preventDefault (defensive)
  uploadBtn.addEventListener("click", async (event) => {
    event.preventDefault(); // defensive: button is type="button", but keeps behavior safe
    const file = fileInput.files[0];
    if (!file) {
      status.innerText = "⚠️ Please select a .wav file before uploading.";
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    status.innerText = "⏳ Uploading file...";

    try {
      const response = await fetch("http://127.0.0.1:8000/upload/", {
        method: "POST",
        body: formData
      });

      if (!response.ok) throw new Error(`Server error: ${response.status}`);

      const resultData = await response.json();
      displayResult(resultData);
      fileInput.value = "";
    } catch (error) {
      console.error("Upload failed:", error);
      status.innerText = "❌ Upload failed. Check backend or CORS.";
    }
  });
});
// ...existing code...