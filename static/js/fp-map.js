
 // Displays environmental report markers on a Leaflet map

(function() {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMap);
  } else {
    initMap();
  }

  function initMap() {
    var mapContainer = document.getElementById('fp-map-container');
    if (!mapContainer) {
      console.log('FP Map: Container not found');
      return;
    }

    console.log('FP Map: Initializing...');

    var SEVERITY_COLORS = {
      Low: '#4CAF50',
      Medium: '#FF9800',
      High: '#F44336',
      Critical: '#D92D2D'
    };

    var SEVERITY_ICONS = {
      Low: '🟢',
      Medium: '🟠',
      High: '🔴',
      Critical: '⚠️'
    };

    var fpMap = L.map('fp-map-container').setView([13.8595, 120.978], 10);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(fpMap);

    function calculateSeverity(reports) {
      if (!reports || reports.length === 0) return 'Low';
      
      var weights = { Critical: 4, High: 3, Medium: 2, Low: 1 };
      var total = 0;
      for (var i = 0; i < reports.length; i++) {
        total += (weights[reports[i].severity] || 1);
      }
      var avg = total / reports.length;
      
      if (avg >= 3.5) return 'Critical';
      if (avg >= 2.5) return 'High';
      if (avg >= 1.5) return 'Medium';
      return 'Low';
    }

    // Fetch locations and reports
    Promise.all([
      fetch('/api/locations').then(function(r) { return r.json(); }),
      fetch('/api/reports').then(function(r) { return r.json(); })
    ])
    .then(function(results) {
      var locations = results[0];
      var reports = results[1];
      
      console.log('FP Map: Locations loaded:', locations.data ? locations.data.length : 0);
      console.log('FP Map: Reports loaded:', reports.data ? reports.data.length : 0);

      if (!locations.success || !locations.data) {
        console.log('FP Map: No location data');
        return;
      }

      // Group reports by location_id
      var reportsByLoc = {};
      if (reports.success && reports.data) {
        for (var i = 0; i < reports.data.length; i++) {
          var r = reports.data[i];
          var locId = r.location ? r.location.location_id : null;
          if (locId) {
            if (!reportsByLoc[locId]) reportsByLoc[locId] = [];
            reportsByLoc[locId].push(r);
          }
        }
      }

      console.log('FP Map: Reports grouped by location:', Object.keys(reportsByLoc).length, 'locations have reports');

      // Add markers
      for (var j = 0; j < locations.data.length; j++) {
        var loc = locations.data[j];
        if (!loc.latitude || !loc.longitude) continue;

        var lat = parseFloat(loc.latitude);
        var lon = parseFloat(loc.longitude);
        if (isNaN(lat) || isNaN(lon)) continue;

        var locReports = reportsByLoc[loc.location_id] || [];
        var severity = calculateSeverity(locReports);
        var color = SEVERITY_COLORS[severity];
        var icon = SEVERITY_ICONS[severity];

        var pinHtml = '<div style="width:24px;height:24px;border-radius:50%;background-color:' + color + ';border:2px solid white;box-shadow:0 2px 5px rgba(0,0,0,0.3);"></div>';

        var markerIcon = L.divIcon({
          className: '',
          html: pinHtml,
          iconSize: [24, 24],
          iconAnchor: [12, 24],
          popupAnchor: [0, -20]
        });

        var popup = '<div style="padding:8px;">' +
          '<h4 style="font-weight:bold;font-size:16px;margin:0 0 4px 0;">' + loc.city_name + '</h4>' +
          '<p style="font-size:12px;color:#666;margin:0 0 8px 0;border-bottom:1px solid #eee;padding-bottom:4px;">Batangas Province</p>' +
          '<p style="font-size:14px;margin:4px 0;">Total Reports: <strong>' + locReports.length + '</strong></p>' +
          '<p style="font-size:14px;margin:4px 0;">Severity: <strong style="color:' + color + ';">' + icon + ' ' + severity + '</strong></p>' +
          '</div>';

        L.marker([lat, lon], { icon: markerIcon })
          .bindPopup(popup)
          .addTo(fpMap);
      }

      console.log('FP Map: Markers added');
    })
    .catch(function(err) {
      console.error('FP Map Error:', err);
    });
  }
})();
