document.addEventListener("DOMContentLoaded", () => {
  const closePopupBtn = document.getElementById("close-popup");
  const viewDetailsBtn = document.getElementById("view-details-btn");
  const goBackBtn = document.getElementById("go-back-btn");
  const severityFilter = document.getElementById("severity-filter");
  const dashboardCityName = document.getElementById("dashboard-city-name");

  const mapView = document.getElementById("map-view-app");
  const dashboardView = document.getElementById("dashboard-view-app");

  let BATANGAS_LGUS = []; // Will be loaded from API

  const SEVERITY_DISPLAY = {
    Low: { color: "#4CAF50", icon: "🟢" },
    Medium: { color: "#FF9800", icon: "🟠" },
    High: { color: "#F44336", icon: "🔴" },
    Critical: { color: "#D92D2D", icon: "!" },
  };

  const BATANGAS_CENTER = [13.8595, 120.978];
  const INITIAL_ZOOM = 10;
  let map;
  let markerGroup = new L.LayerGroup();

  // Load locations from API
  async function loadLocations() {
    try {
      const response = await fetch('/api/locations');
      const result = await response.json();
      
      if (result.success && result.data) {
        BATANGAS_LGUS = result.data.map(location => ({
          city: location.city_name,
          lat: parseFloat(location.latitude),
          lon: parseFloat(location.longitude),
          severity: location.severity_level,
          total: location.total_reports || 0,
          location_id: location.location_id
        }));
        
        plotAllMarkers();
      }
    } catch (error) {
      console.error('Error loading locations:', error);
    }
  }

  function initializeMap() {
    map = L.map("map-container").setView(BATANGAS_CENTER, INITIAL_ZOOM);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution:
        '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(map);

    markerGroup.addTo(map);

    // Load locations from database
    loadLocations();
  }

  function getCustomIcon(severity) {
    const display = SEVERITY_DISPLAY[severity];

    // Use a DivIcon to render a simple, color-coded pin
    const color = display ? display.color : "#3f51b5"; // default blue
    const html = `
      <div class="severity-pin" style="background-color: ${color}">
        <span class="severity-pin__dot"></span>
      </div>
    `;
    return L.divIcon({
      className: "severity-pin-wrapper",
      html,
      iconSize: [30, 30],
      iconAnchor: [15, 30],
      popupAnchor: [0, -28],
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
