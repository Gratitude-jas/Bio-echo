document.getElementById("uploadForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const fileInput = document.getElementById("fileInput");
  const status = document.getElementById("status");

  if (!fileInput.files[0]) {
    status.innerText = "❌ Please select a file.";
    return;
  }

  status.innerText = "🔄 Extracting biomarkers…";

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  fetch("http://127.0.0.1:8000/upload/", {
    method: "POST",
    body: formData
  })
    .then(res => {
      if (!res.ok) throw new Error("Upload failed");
      return res.json();
    })
    .then(data => {
      localStorage.setItem("bioecho_result", JSON.stringify(data));
      window.location.href = "output.html";
    })
    .catch(err => {
      status.innerText = "❌ Upload failed. Check backend or CORS.";
      console.error("Error:", err);
    });
});