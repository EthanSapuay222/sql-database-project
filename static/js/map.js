document.addEventListener("DOMContentLoaded", () => {
  const closePopupBtn = document.getElementById("close-popup");
  const viewDetailsBtn = document.getElementById("view-details-btn");
  const goBackBtn = document.getElementById("go-back-btn");
  const severityFilter = document.getElementById("severity-filter");
  const dashboardCityName = document.getElementById("dashboard-city-name");

  const mapView = document.getElementById("map-view-app");
  const dashboardView = document.getElementById("dashboard-view-app");

  const BATANGAS_LGUS = [
    // CITIES (5)
    {
      city: "Batangas City",
      lat: 13.7562,
      lon: 121.0573,
      severity: "Critical",
      total: 4,
    },
    { city: "Calaca", lat: 13.9303, lon: 120.8128, severity: "Low", total: 40 },
    {
      city: "Lipa City",
      lat: 13.9483,
      lon: 121.1683,
      severity: "High",
      total: 7,
    },
    {
      city: "Santo Tomas",
      lat: 14.08,
      lon: 121.14,
      severity: "Medium",
      total: 15,
    },
    {
      city: "Tanauan City",
      lat: 14.0844,
      lon: 121.1492,
      severity: "Critical",
      total: 5,
    },
    // MUNICIPALITIES (29)
    {
      city: "Agoncillo",
      lat: 13.9342,
      lon: 120.9283,
      severity: "Low",
      total: 45,
    },
    {
      city: "Alitagtag",
      lat: 13.8653,
      lon: 121.0047,
      severity: "Low",
      total: 38,
    },
    {
      city: "Balayan",
      lat: 13.9442,
      lon: 120.7336,
      severity: "Medium",
      total: 18,
    },
    {
      city: "Balete",
      lat: 14.0167,
      lon: 121.0833,
      severity: "Low",
      total: 35,
    },
    {
      city: "Bauan",
      lat: 13.7925,
      lon: 121.0078,
      severity: "High",
      total: 8,
    },
    {
      city: "Calatagan",
      lat: 13.8322,
      lon: 120.6275,
      severity: "Low",
      total: 50,
    },
    {
      city: "Cuenca",
      lat: 13.9167,
      lon: 121.05,
      severity: "Medium",
      total: 12,
    },
    {
      city: "Ibaan",
      lat: 13.8211,
      lon: 121.1444,
      severity: "Low",
      total: 25,
    },
    {
      city: "Laurel",
      lat: 14.05,
      lon: 120.9333,
      severity: "Medium",
      total: 16,
    },
    {
      city: "Lemery",
      lat: 13.9011,
      lon: 120.8928,
      severity: "Medium",
      total: 10,
    },
    {
      city: "Lian",
      lat: 13.9875,
      lon: 120.6558,
      severity: "Low",
      total: 42,
    },
    { city: "Lobo", lat: 13.6267, lon: 121.2142, severity: "High", total: 6 },
    {
      city: "Mabini",
      lat: 13.7639,
      lon: 120.9417,
      severity: "Critical",
      total: 2,
    },
    {
      city: "Malvar",
      lat: 14.0322,
      lon: 121.155,
      severity: "Low",
      total: 30,
    },
    {
      city: "Mataasnakahoy",
      lat: 14.0203,
      lon: 121.1111,
      severity: "Medium",
      total: 14,
    },
    {
      city: "Nasugbu",
      lat: 14.0722,
      lon: 120.6358,
      severity: "High",
      total: 9,
    },
    {
      city: "Padre Garcia",
      lat: 13.8967,
      lon: 121.2339,
      severity: "Low",
      total: 28,
    },
    {
      city: "Rosario",
      lat: 13.8589,
      lon: 121.2339,
      severity: "Medium",
      total: 20,
    },
    {
      city: "San Jose",
      lat: 13.8825,
      lon: 121.1067,
      severity: "Low",
      total: 32,
    },
    {
      city: "San Juan",
      lat: 13.8167,
      lon: 121.3833,
      severity: "Critical",
      total: 3,
    },
    {
      city: "San Luis",
      lat: 13.8561,
      lon: 120.9389,
      severity: "Medium",
      total: 11,
    },
    {
      city: "San Nicolas",
      lat: 13.9458,
      lon: 120.9633,
      severity: "High",
      total: 7,
    },
    {
      city: "San Pascual",
      lat: 13.8058,
      lon: 120.9828,
      severity: "Medium",
      total: 13,
    },
    {
      city: "Santa Teresita",
      lat: 13.85,
      lon: 120.9833,
      severity: "Low",
      total: 33,
    },
    { city: "Taal", lat: 13.8767, lon: 120.9233, severity: "High", total: 8 },
    {
      city: "Talisay",
      lat: 14.095,
      lon: 121.0142,
      severity: "Low",
      total: 29,
    },
    {
      city: "Taysan",
      lat: 13.7667,
      lon: 121.1714,
      severity: "Medium",
      total: 17,
    },
    {
      city: "Tingloy",
      lat: 13.7333,
      lon: 120.8667,
      severity: "Low",
      total: 36,
    },
    { city: "Tuy", lat: 14.0167, lon: 120.75, severity: "Low", total: 31 },
  ];
  const SEVERITY_DISPLAY = {
    Critical: { color: "#D92D2D", icon: "!" },
    High: { color: "#E0790B", icon: "▲" },
    Medium: { color: "#F7BE00", icon: "●" },
    Low: { color: "#00A8A8", icon: "○" },
  };

  const BATANGAS_CENTER = [13.8595, 120.978];
  const INITIAL_ZOOM = 10;
  let map;
  let markerGroup = new L.LayerGroup();

  function initializeMap() {
    map = L.map("map-container").setView(BATANGAS_CENTER, INITIAL_ZOOM);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution:
        '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(map);

    markerGroup.addTo(map);

    plotAllMarkers();
  }

  function getCustomIcon(severity) {
    const display = SEVERITY_DISPLAY[severity];
    return new L.Icon.Glyph({
      prefix: "",
      glyph: display.icon,
      iconUrl: "https://unpkg.com/leaflet/dist/images/marker-icon.png",
      iconRetinaUrl:
        "https://unpkg.com/leaflet/dist/images/marker-icon-2x.png",
      shadowUrl: "https://unpkg.com/leaflet/dist/images/marker-shadow.png",
      markerColor: display.color,
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowSize: [41, 41],
    });
  }

  function plotAllMarkers() {
    BATANGAS_LGUS.forEach((lgu) => {
      const markerIcon = getCustomIcon(lgu.severity);

      const marker = L.marker([lgu.lat, lgu.lon], { icon: markerIcon })
        .bindPopup(createPopupContent(lgu))
        .on("click", () => {
          dashboardCityName.textContent = lgu.city;
        });
      marker.severity = lgu.severity;

      markerGroup.addLayer(marker);
    });
  }

  function createPopupContent(lgu) {
    const display = SEVERITY_DISPLAY[lgu.severity];
    return `
      <div class="p-2">
          <h4 class="font-bold text-lg">${lgu.city}</h4>
          <p class="text-xs text-gray-500 border-b pb-1">Batangas Province</p>
          <p class="mt-2 text-sm text-gray-700">Total Reports: <span class="font-bold">${lgu.total}</span></p>
          <p class="text-sm">
              Severity: 
              <span class="font-bold" style="color: ${display.color};">
                  ${display.icon} ${lgu.severity}
              </span>
          </p>
          <button 
              onclick="showDashboard('${lgu.city}')"
              class="mt-3 w-full bg-green-500 hover:bg-green-600 text-white font-semibold py-1.5 px-3 rounded-lg text-sm transition duration-200"
          >
              View Details →
          </button>
      </div>
    `;
  }

  window.showDashboard = (cityName) => {
    dashboardCityName.textContent = cityName;
    mapView.style.display = "none";
    dashboardView.style.display = "block";
    map.closePopup();
    window.scrollTo(0, 0);
  };

  function applyFilter(selectedSeverity) {
    markerGroup.eachLayer((layer) => {
      if (layer instanceof L.Marker) {
        if (selectedSeverity === "All" || layer.severity === selectedSeverity) {
          layer.setOpacity(1.0);
          layer.getElement().style.display = "block";
        } else {
          layer.setOpacity(0.1);
          layer.getElement().style.display = "none";
        }
      }
    });
  }

  severityFilter.addEventListener("change", (e) => {
    applyFilter(e.target.value);
  });

  goBackBtn.addEventListener("click", () => {
    dashboardView.style.display = "none";
    mapView.style.display = "block";
    map.invalidateSize();
    window.scrollTo(0, 0);
  });

  initializeMap();
  applyFilter(severityFilter.value);
});
