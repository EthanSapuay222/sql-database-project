// Dashboard Charts and Initialization

document.addEventListener('DOMContentLoaded', function() {
  // Update status display
  const userIdDisplay = document.getElementById("user-id-display");
  if (userIdDisplay) {
    userIdDisplay.innerHTML = `<span class="font-bold">Status:</span> Dashboard Ready`;
  }

  const accentColor = "#6dd9e8";
  const accentColorDark = "#3aa4b0";
  const labels = ["Item 1", "Item 2", "Item 3", "Item 4"];

  // Category Distribution Pie Chart
  const pieCtx = document.getElementById("categoryDistributionChart");
  if (pieCtx) {
    new Chart(pieCtx.getContext("2d"), {
      type: "doughnut",
      data: {
        labels: ["Item 1: 62.5%", "Item 2: 25%", "Item 3: 12.5%"],
        datasets: [
          {
            data: [5, 2, 1],
            backgroundColor: [accentColor, accentColorDark, "#99e0e8"],
            hoverOffset: 16,
            borderWidth: 2,
            borderColor: "#ffffff",
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: "bottom",
            labels: {
              color: "#374151",
              font: {
                size: 14,
              },
            },
          },
          tooltip: {
            callbacks: {
              label: function (context) {
                let label = context.label || "";
                if (label) {
                  label += ": ";
                }
                label += context.raw;
                return label;
              },
            },
          },
        },
      },
    });
  }

  // Land Sightings Chart
  const landCtx = document.getElementById("landSightingsChart");
  if (landCtx) {
    new Chart(landCtx.getContext("2d"), {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Sightings",
            data: [10, 15, 25, 30],
            backgroundColor: accentColor,
            borderColor: accentColorDark,
            borderWidth: 1,
            borderRadius: 6,
            barPercentage: 0.8,
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            max: 30,
            grid: { color: "rgba(200, 200, 200, 0.2)" },
          },
          x: {
            grid: { display: false },
          },
        },
        plugins: {
          legend: { display: false },
          title: { display: false },
        },
      },
    });
  }

  // Water Sightings Chart
  const waterCtx = document.getElementById("waterSightingsChart");
  if (waterCtx) {
    new Chart(waterCtx.getContext("2d"), {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Sightings",
            data: [8, 12, 16, 20],
            backgroundColor: accentColor,
            borderColor: accentColorDark,
            borderWidth: 1,
            borderRadius: 6,
            barPercentage: 0.8,
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            max: 20,
            grid: { color: "rgba(200, 200, 200, 0.2)" },
          },
          x: {
            grid: { display: false },
          },
        },
        plugins: {
          legend: { display: false },
          title: { display: false },
        },
      },
    });
  }
});
