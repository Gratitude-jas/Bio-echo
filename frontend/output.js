window.addEventListener("DOMContentLoaded", () => {
  const resultData = JSON.parse(localStorage.getItem("bioecho_result"));

  // Display basic results
  document.getElementById("results").innerHTML = `
    <strong>Filename:</strong> ${resultData.filename}<br>
    <strong>Parkinson Detected:</strong> ${resultData.parkinson_detected ? "✅ Yes" : "❌ No"}<br>
    <strong>Confidence:</strong> ${Math.round(resultData.confidence * 100)}%<br>
    <strong>Features:</strong>
    <ul>${Object.entries(resultData.features).map(([k, v]) => `<li>${k}: ${v.toFixed(4)}</li>`).join("")}</ul>
  `;

  // Radar chart
  const radarLabels = Object.keys(resultData.features);
  const radarValues = Object.values(resultData.features);

  new Chart(document.getElementById("radarChart"), {
    type: "radar",
    data: {
      labels: radarLabels,
      datasets: [{
        label: "Voice Biomarkers",
        data: radarValues,
        backgroundColor: "rgba(0, 201, 255, 0.2)",
        borderColor: "#00c9ff",
        pointBackgroundColor: "#00c9ff"
      }]
    },
    options: {
      scales: {
        r: {
          suggestedMin: 0,
          suggestedMax: Math.max(...radarValues) * 1.2
        }
      }
    }
  });

  // SHAP bar chart
  const shapData = resultData.feature_importance || {};
  const shapLabels = Object.keys(shapData);
  const shapValues = Object.values(shapData);

  console.log("SHAP feature_importance:", shapData);
  console.log("SHAP Labels:", shapLabels);
  console.log("SHAP Values:", shapValues);

  const shapCanvas = document.getElementById("shapChart");

  if (!shapCanvas) {
    console.error("❌ Canvas element with id 'shapChart' not found in HTML.");
  } else if (shapLabels.length > 0) {
    new Chart(shapCanvas, {
      type: "bar",
      data: {
        labels: shapLabels,
        datasets: [{
          label: "SHAP Value",
          data: shapValues,
          backgroundColor: shapValues.map(v =>
            v === 0 ? "rgba(200, 200, 200, 0.4)" :
            v > 0 ? "rgba(0, 201, 255, 0.6)" :
                    "rgba(255, 99, 132, 0.6)"
          ),
          borderColor: shapValues.map(v =>
            v === 0 ? "#ccc" :
            v > 0 ? "#00c9ff" :
                    "#ff6384"
          ),
          borderWidth: 1
        }]
      },
      options: {
        plugins: {
          title: {
            display: true,
            text: "Feature Impact on Prediction"
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: "SHAP Value"
            }
          }
        }
      }
    });
  } else {
    console.warn("⚠️ SHAP data missing — chart skipped.");
  }

  // Download PDF
  const downloadBtn = document.getElementById("downloadReport");
  console.log("Button found:", downloadBtn);

  downloadBtn.addEventListener("click", () => {
    console.log("Download button clicked ✅");
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    doc.setFontSize(16);
    doc.text("BioEcho Prediction Report", 20, 20);

    doc.setFontSize(12);
    doc.text(`Filename: ${resultData.filename}`, 20, 35);
    doc.text(`Timestamp: ${new Date().toLocaleString()}`, 20, 45);
    doc.text(`Parkinson Detected: ${resultData.parkinson_detected ? "Yes" : "No"}`, 20, 55);
    doc.text(`Confidence: ${Math.round(resultData.confidence * 100)}%`, 20, 65);

    doc.text("Extracted Features:", 20, 80);
    let y = 90;
    Object.entries(resultData.features).forEach(([k, v]) => {
      doc.text(`${k}: ${v.toFixed(4)}`, 25, y);
      y += 8;
    });

    if (resultData.feature_importance && Object.keys(resultData.feature_importance).length > 0) {
      doc.text("SHAP Feature Impact:", 20, y + 10);
      y += 20;
      Object.entries(resultData.feature_importance).forEach(([k, v]) => {
        doc.text(`${k}: ${v.toFixed(4)}`, 25, y);
        y += 8;
      });
    }

    doc.save(`BioEcho_Report_${resultData.filename}.pdf`);
  });
});