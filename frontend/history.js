const history = JSON.parse(localStorage.getItem("bioecho_history")) || [];

const tableBody = document.querySelector("#historyTable tbody");

history.forEach((entry, index) => {
  const row = document.createElement("tr");

  row.innerHTML = `
    <td>${entry.filename}</td>
    <td>${entry.parkinson_detected ? "✅ Yes" : "❌ No"}</td>
    <td>${Math.round(entry.confidence * 100)}%</td>
    <td>${entry.timestamp || "—"}</td>
    <td><button onclick="viewResult(${index})">🔍 View</button></td>
  `;

  tableBody.appendChild(row);
});

function viewResult(index) {
  const selected = history[index];
  localStorage.setItem("bioecho_result", JSON.stringify(selected));
  window.location.href = "output.html";
}