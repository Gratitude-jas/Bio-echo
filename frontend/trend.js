const history = JSON.parse(localStorage.getItem("bioecho_history")) || [];
const featureSelect = document.getElementById("featureSelect");
const chartCanvas = document.getElementById("trendChart");

const allFeatures = Object.keys(history[0]?.features || {});
allFeatures.forEach(f => {
  const option = document.createElement("option");
  option.value = f;
  option.textContent = f;
  featureSelect.appendChild(option);
});

let chart;

function renderChart(featureName) {
  const timestamps = history.map(h => h.timestamp || "—");
  const values = history.map(h => h.features[featureName]);

  if (chart) chart.destroy();

  chart = new Chart(chartCanvas, {
    type: "line",
    data: {
      labels: timestamps,
      datasets: [{
        label: `${featureName} over time`,
        data: values,
        fill: false,
        borderColor: "#00c9ff",
        backgroundColor: "rgba(0, 201, 255, 0.2)",
        tension: 0.3,
        pointRadius: 4
      }]
    },
    options: {
      plugins: {
        title: {
          display: true,
          text: `Tracking ${featureName} across sessions`
        }
      },
      scales: {
        x: {
          title: {
            display: true,
            text: "Timestamp"
          }
        },
        y: {
          title: {
            display: true,
            text: "Feature Value"
          },
          beginAtZero: false
        }
      }
    }
  });
}

featureSelect.addEventListener("change", () => {
  renderChart(featureSelect.value);
});

// Initial render
if (allFeatures.length > 0) {
  featureSelect.value = allFeatures[0];
  renderChart(allFeatures[0]);
}